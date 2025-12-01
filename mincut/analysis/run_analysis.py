import copy
import os
import sys
from pathlib import Path

# Add parent directory to path for relative imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data.generate_dataset import save_graphs
from algorithms.stoer_wagner.stoer_wagner_cpp import stoer_wagner
from algorithms.karger.karger_cpp import karger_min_cut

# Configuration flags
TRIALS = 100
NUM_GRAPHS = 100
REGENERATE_GRAPHS = False

# Set up paths relative to project root (two levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
GRAPHS_DIR = PROJECT_ROOT / 'graphs'
RESULTS_DIR = PROJECT_ROOT / 'results'
os.makedirs(GRAPHS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Analysis execution flags
RUN_BASIC_ANALYSIS = False           
RUN_TRIALS_IMPACT_ANALYSIS = False   
RUN_SIZE_IMPACT_ANALYSIS = False
RUN_KARGER_100_VS_THEORY = False     

def read_graphs(filename):
    """Read graphs from file."""
    graphs = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        if lines[i].strip() == '---':
            i += 1
            continue
        
        num_vertices = int(lines[i].strip())
        i += 1
        
        graph = []
        for _ in range(num_vertices):
            row = list(map(int, lines[i].strip().split()))
            graph.append(row)
            i += 1
        
        graphs.append(graph)
    
    return graphs

def analyze_graphs(graph_type):
    """Analyze graphs of given type and return error percentages."""
    filename = GRAPHS_DIR / f'{graph_type}_graphs.txt'
    
    # Generate or load graphs
    if REGENERATE_GRAPHS:
        save_graphs(f'{graph_type}_graphs.txt', num_graphs=NUM_GRAPHS, min_vertices=50, max_vertices=500, graph_type=graph_type, output_dir=GRAPHS_DIR)
    
    # Read graphs
    graphs = read_graphs(str(filename))
    
    sw_values = []
    karger_values = []
    errors = []
    
    with open(RESULTS_DIR / f'{graph_type}_analysis.txt', 'w') as f:
        f.write(f"{graph_type.upper()} GRAPHS ANALYSIS\n")
        f.write("=" * 50 + "\n\n")
        
        for idx, graph in enumerate(graphs):
            # Run both algorithms
            G_sw = copy.deepcopy(graph)
            sw_result = stoer_wagner(G_sw)
            
            G_k = copy.deepcopy(graph)
            karger_result = karger_min_cut(G_k, trials=TRIALS)
            
            error = abs(sw_result - karger_result) / sw_result * 100 if sw_result > 0 else 0
            errors.append(error)
            
            sw_values.append(sw_result)
            karger_values.append(karger_result)
            
            f.write(f"Graph {idx + 1}: SW={sw_result}, Karger={karger_result}, Error={error:.2f}%\n")
            print(f"{graph_type} Graph {idx + 1}: Error={error:.2f}%")
        
        avg_error = sum(errors) / len(errors) if errors else 0
        f.write(f"\nAverage Error: {avg_error:.2f}%\n")
    
    # Create bar graph comparing algorithms for this type
    import matplotlib.pyplot as plt
    x = range(len(sw_values))
    plt.figure(figsize=(14, 5))
    plt.bar([i - 0.2 for i in x], sw_values, 0.4, label='Stoer-Wagner', alpha=0.8)
    plt.bar([i + 0.2 for i in x], karger_values, 0.4, label='Karger', alpha=0.8)
    plt.xlabel('Graph')
    plt.ylabel('Min-Cut Value')
    plt.title(f'{graph_type.upper()}: Stoer-Wagner vs Karger')
    #plot lables once every 5 only not everything
    plt.xticks([i for i in x if (i+1) % 5 == 0], [i+1 for i in x if (i+1) % 5 == 0])
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / f'{graph_type}_comparison.png')
    plt.close()
    
    return avg_error



def check_graph_files_exist():
    """Check if all required graph files exist."""
    types = ['random', 'sparse', 'dense']
    required_files = [GRAPHS_DIR / f'{gtype}_graphs.txt' for gtype in types]
    
    for filepath in required_files:
        if not filepath.exists():
            return False, filepath
    
    return True, None


def analyze_trials_impact():
    """Analyze impact of different trial counts on error rate."""
    import matplotlib.pyplot as plt
    
    trial_counts = [10, 50, 100,150,200]
    types = ['random', 'sparse', 'dense']
    results = {}
    
    # Store results for each graph type
    for graph_type in types:
        results[graph_type] = {'trials': [], 'avg_errors': []}
    
    print("\n" + "="*60)
    print("ANALYZING IMPACT OF TRIAL COUNT ON ERROR RATE")
    print("="*60)
    
    # Test each trial count
    generatedgraphs = {}
    for graph_type in types:
            filename = GRAPHS_DIR / f'{graph_type}_graphs.txt'
            generatedgraphs[graph_type] = read_graphs(str(filename))

    #precomputing stoer_wagner
    stoer_results_bytype = {}
    print(f"Precomputing for stoer-wagner\n")
    stoer_results_bytype['random'] = [stoer_wagner(copy.deepcopy(G)) for G in generatedgraphs['random']]
    stoer_results_bytype['sparse'] = [stoer_wagner(copy.deepcopy(G)) for G in generatedgraphs['sparse']]

    stoer_results_bytype['dense'] = [stoer_wagner(copy.deepcopy(G)) for G in generatedgraphs['dense']]


    for num_trials in trial_counts:
        print(f"\nTesting with {num_trials} trials...")
        
        for graph_type in generatedgraphs:
            graphs =generatedgraphs[graph_type]
            
            errors = []
            for idx, graph in enumerate(graphs):
                sw_result = stoer_results_bytype[graph_type][idx]
                karger_result = karger_min_cut(copy.deepcopy(graph), trials=num_trials)
                
                error = abs(sw_result - karger_result) / sw_result * 100 if sw_result > 0 else 0
                errors.append(error)
            
            avg_error = sum(errors) / len(errors) if errors else 0
            results[graph_type]['trials'].append(num_trials)
            results[graph_type]['avg_errors'].append(avg_error)
            
            print(f"  {graph_type.upper()}: {num_trials} trials -> Avg Error: {avg_error:.2f}%")
    
    # Create line plot showing error trend
    plt.figure(figsize=(10, 6))
    
    colors = {'random': 'blue', 'sparse': 'orange', 'dense': 'red'}
    markers = {'random': 'o', 'sparse': 's', 'dense': '^'}
    
    for graph_type in types:
        plt.plot(results[graph_type]['trials'], 
                results[graph_type]['avg_errors'],
                marker=markers[graph_type],
                label=graph_type.capitalize(),
                color=colors[graph_type],
                linewidth=2,
                markersize=8)
    
    plt.xlabel('Number of Trials', fontsize=12)
    plt.ylabel('Average Error %', fontsize=12)
    plt.title('Error Rate vs Trial Count', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'trials_impact_analysis.png', dpi=150)
    plt.close()
    
    print(f"\nGraph saved to {RESULTS_DIR / 'trials_impact_analysis.png'}")
    
    # Write results to file
    with open(RESULTS_DIR / 'trials_analysis.txt', 'w') as f:
        f.write("TRIAL COUNT IMPACT ANALYSIS\n")
        f.write("="*60 + "\n\n")
        
        for graph_type in types:
            f.write(f"\n{graph_type.upper()} GRAPHS:\n")
            f.write("-"*40 + "\n")
            
            for trials, avg_err in zip(results[graph_type]['trials'], 
                                       results[graph_type]['avg_errors']):
                f.write(f"Trials: {trials:3d}  ->  Avg Error: {avg_err:6.2f}%\n")
    
    print("Results saved to " + str(RESULTS_DIR / 'trials_analysis.txt'))
    
    return results


def analyze_graph_sizes(small_size=20, medium_size=50, large_size=100, num_graphs=15,trials_for_krager=100):
    """
    Analyze error rates for different graph sizes.
    
    Parameters:
        small_size: Max vertices for small graphs
        medium_size: Max vertices for medium graphs
        large_size: Max vertices for large graphs
        num_graphs: Number of graphs per size category
    """
    import matplotlib.pyplot as plt
    
    sizes = {'Small': small_size, 'Medium': medium_size, 'Large': large_size}
    results = {}
    
    print("\n" + "="*60)
    print("ANALYZING ERROR RATE BY GRAPH SIZE")
    print("="*60)
    
    # Generate and test graphs of each size
    for size_name, max_vertices in sizes.items():
        print(f"\nGenerating {num_graphs} {size_name} graphs (max {max_vertices} vertices)...")
        
        # Generate graphs of this size
        filename = GRAPHS_DIR / f'temp_{size_name.lower()}.txt'
        save_graphs(f'temp_{size_name.lower()}.txt', num_graphs=num_graphs, 
                   min_vertices=max_vertices//2, max_vertices=max_vertices, 
                   graph_type='random', output_dir=GRAPHS_DIR)
        
        # Read generated graphs
        graphs = read_graphs(str(filename))
        
        errors = []
        sw_values = []
        karger_values = []
        
        # Test each graph
        for idx, graph in enumerate(graphs):
            sw_result = stoer_wagner(copy.deepcopy(graph))
            karger_result = karger_min_cut(copy.deepcopy(graph), trials=trials_for_krager)
            
            error = abs(sw_result - karger_result) / sw_result * 100 if sw_result > 0 else 0
            errors.append(error)
            sw_values.append(sw_result)
            karger_values.append(karger_result)
        
        avg_error = sum(errors) / len(errors) if errors else 0
        results[size_name] = {'avg_error': avg_error, 'sw': sw_values, 'karger': karger_values}
        
        print(f"{size_name}: Average Error = {avg_error:.2f}%")
    
    # Create bar graph comparing error rates
    plt.figure(figsize=(10, 6))
    size_names = list(results.keys())
    avg_errors = [results[s]['avg_error'] for s in size_names]
    
    colors = ['green', 'orange', 'red']
    bars = plt.bar(size_names, avg_errors, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    
    # Add value labels on bars
    for bar, error in zip(bars, avg_errors):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{error:.2f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.ylabel('Average Error %', fontsize=12)
    plt.xlabel('Graph Size', fontsize=12)
    plt.title('Karger Error Rate vs Graph Size (Stoer-Wagner)', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'size_impact_comparison.png', dpi=150)
    plt.close()
    
    print(f"\nGraph saved to {RESULTS_DIR / 'size_impact_comparison.png'}")
    
    # Write results to file
    with open(RESULTS_DIR / 'size_analysis.txt', 'w') as f:
        f.write("GRAPH SIZE IMPACT ANALYSIS\n")
        f.write("="*60 + "\n\n")
        
        for size_name in size_names:
            avg_err = results[size_name]['avg_error']
            f.write(f"{size_name} Graphs:\n")
            f.write(f"  Average Error: {avg_err:.2f}%\n\n")
    
    print("Results saved to " + str(RESULTS_DIR / 'size_analysis.txt'))
    
    return results


def karger_100_vs_theory():
    """
    Compare Karger with 100 trials vs theoretical n^2*log(n) trials.
    Measure both accuracy and runtime.
    """
    import matplotlib.pyplot as plt
    import time
    import math
    
    print("\n" + "="*60)
    print("KARGER: 100 TRIALS VS THEORETICAL n²log(n) TRIALS")
    print("="*60)
    
    # Generate test graphs of varying sizes
    graph_sizes = [75,90,105,120,135,150]
    num_graphs_per_size = 50
    
    results = {
        'sizes': [],
        'karger_100_time': [],
        'karger_theory_time': [],
        'karger_100_error': [],
        'karger_theory_error': [],
        'theoretical_trials': []
    }
    
    for size in graph_sizes:
        print(f"\nTesting graphs with {size} vertices...")
        
        # Calculate theoretical trial count
        n_squared_log_n = int((size * size) * math.log(size))
        results['theoretical_trials'].append(n_squared_log_n)
        
        print(f"  Theoretical trials: {n_squared_log_n}")
        print(f"  100 trials vs {n_squared_log_n} trials")
        
        # Generate small test set for this size
        temp_filename = GRAPHS_DIR / f'temp_karger_compare_{size}.txt'
        save_graphs(f'temp_karger_compare_{size}.txt', num_graphs=num_graphs_per_size,
                   min_vertices=size, max_vertices=size, graph_type='random', output_dir=GRAPHS_DIR)
        
        graphs = read_graphs(str(temp_filename))
        
        # Track metrics
        karger_100_times = []
        karger_theory_times = []
        karger_100_errors = []
        karger_theory_errors = []
        
        for idx, graph in enumerate(graphs):
            # Get ground truth from Stoer-Wagner
            sw_result = stoer_wagner(copy.deepcopy(graph))
            
            # Test Karger with 100 trials
            start_time = time.time()
            karger_100_result = karger_min_cut(copy.deepcopy(graph), trials=100)
            karger_100_time = time.time() - start_time
            karger_100_times.append(karger_100_time)
            
            karger_100_error = abs(karger_100_result - sw_result) / sw_result * 100 if sw_result > 0 else 0
            karger_100_errors.append(karger_100_error)
            
            # Test Karger with theoretical trials
            start_time = time.time()
            karger_theory_result = karger_min_cut(copy.deepcopy(graph), trials=n_squared_log_n)
            karger_theory_time = time.time() - start_time
            karger_theory_times.append(karger_theory_time)
            
            karger_theory_error = abs(karger_theory_result - sw_result) / sw_result * 100 if sw_result > 0 else 0
            karger_theory_errors.append(karger_theory_error)
            
            print(f"    Graph {idx+1}: 100 trials={karger_100_error:.2f}% error in {karger_100_time:.3f}s, "
                  f"Theory={karger_theory_error:.2f}% error in {karger_theory_time:.3f}s")
        
        # Store averages
        results['sizes'].append(size)
        results['karger_100_time'].append(sum(karger_100_times) / len(karger_100_times))
        results['karger_theory_time'].append(sum(karger_theory_times) / len(karger_theory_times))
        results['karger_100_error'].append(sum(karger_100_errors) / len(karger_100_errors))
        results['karger_theory_error'].append(sum(karger_theory_errors) / len(karger_theory_errors))
    
    # Plot 1: Time comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.plot(results['sizes'], results['karger_100_time'], 'o-', label='100 Trials', 
             linewidth=2, markersize=8, color='blue')
    ax1.plot(results['sizes'], results['karger_theory_time'], 's-', label=r'$n^2\log(n)$ Trials', 
             linewidth=2, markersize=8, color='red')
    ax1.set_xlabel('Graph Size (vertices)', fontsize=12)
    ax1.set_ylabel('Average Time (seconds)', fontsize=12)
    ax1.set_title('Runtime Comparison', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Accuracy comparison
    ax2.plot(results['sizes'], results['karger_100_error'], 'o-', label='100 Trials', 
             linewidth=2, markersize=8, color='blue')
    ax2.plot(results['sizes'], results['karger_theory_error'], 's-', label=r'$n^2\log(n)$ Trials', 
             linewidth=2, markersize=8, color='red')
    ax2.set_xlabel('Graph Size (vertices)', fontsize=12)
    ax2.set_ylabel('Average Error (%)', fontsize=12)
    ax2.set_title('Accuracy Comparison', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'karger_100_vs_theory.png', dpi=150)
    plt.close()
    
    print(f"\nGraphs saved to {RESULTS_DIR / 'karger_100_vs_theory.png'}")
    
    # Write detailed results to file
    with open(RESULTS_DIR / 'karger_100_vs_theory.txt', 'w') as f:
        f.write("KARGER: 100 TRIALS VS THEORETICAL n²log(n) TRIALS\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"{'Size':<8} {'Theory Trials':<15} {'100T Time(s)':<15} {'Theory Time(s)':<15} "
                f"{'100T Error%':<12} {'Theory Error%':<12}\n")
        f.write("-"*90 + "\n")
        
        for i, size in enumerate(results['sizes']):
            f.write(f"{size:<8} {results['theoretical_trials'][i]:<15} "
                   f"{results['karger_100_time'][i]:<15.3f} {results['karger_theory_time'][i]:<15.3f} "
                   f"{results['karger_100_error'][i]:<12.2f} {results['karger_theory_error'][i]:<12.2f}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("SUMMARY:\n")
        f.write(f"Average speedup (100 trials vs theory): {sum(results['karger_theory_time'])/sum(results['karger_100_time']):.2f}x\n")
        f.write(f"Average error difference: {sum(results['karger_100_error'])/len(results['karger_100_error']) - sum(results['karger_theory_error'])/len(results['karger_theory_error']):.2f}%\n")
    
    print("Results saved to " + str(RESULTS_DIR / 'karger_100_vs_theory.txt'))
    
    return results


def plot_comparison():
    """Plot average error comparison."""
    import matplotlib.pyplot as plt
    
    types = ['random', 'sparse', 'dense']
    errors = []
    
    for graph_type in types:
        with open(RESULTS_DIR / f'{graph_type}_analysis.txt', 'r') as f:
            for line in f:
                if 'Average Error:' in line:
                    avg_err = float(line.split(':')[1].strip().replace('%', ''))
                    errors.append(avg_err)
    
    plt.figure(figsize=(8, 5))
    plt.bar(types, errors, color=['blue', 'orange', 'red'], alpha=0.7)
    plt.ylabel('Average Error %')
    plt.title('Karger vs Stoer-Wagner: Average Error by Graph Type')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'overall_comparison.png')
    print("Graph saved to " + str(RESULTS_DIR / 'overall_comparison.png'))

if __name__ == "__main__":
    # Check if graph files exist when REGENERATE_GRAPHS is False
    if not REGENERATE_GRAPHS:
        files_exist, missing_file = check_graph_files_exist()
        if not files_exist:
            print(f"ERROR: Graph dataset not found at {missing_file}")
            print("Set REGENERATE_GRAPHS = True and try again to generate new graphs.")
            exit(1)
        print("Using existing graphs from graphs/ folder...")
    else:
        print("Regenerating graphs...")
    
    # Basic analysis: Random, Sparse, Dense graphs
    if RUN_BASIC_ANALYSIS:
        print("\n" + "="*60)
        print("BASIC ANALYSIS: Random/Sparse/Dense Graphs")
        print("="*60)
        
        print("\nAnalyzing Random Graphs...")
        analyze_graphs('random')
        
        print("\nAnalyzing Sparse Graphs...")
        analyze_graphs('sparse')
        
        print("\nAnalyzing Dense Graphs...")
        analyze_graphs('dense')
        
        print("\nPlotting overall comparison...")
        plot_comparison()
    
    # Trial count impact analysis
    if RUN_TRIALS_IMPACT_ANALYSIS:
        print("\n" + "="*60)
        analyze_trials_impact()
    
    # Graph size impact analysis
    if RUN_SIZE_IMPACT_ANALYSIS:
        print("\n" + "="*60)
        analyze_graph_sizes(small_size=50, medium_size=250, large_size=500, num_graphs=50)
    
    # Karger 100 vs theoretical trials comparison
    if RUN_KARGER_100_VS_THEORY:
        print("\n" + "="*60)
        karger_100_vs_theory()
    
    print("\n" + "="*60)
    print("All enabled analyses complete!")
    print("="*60)
