import subprocess
import os
import time
import psutil
from generate_dataset import generate_graph

os.makedirs('results', exist_ok=True)

def run_karger(exe_name, V, E, edges, trials=100):
    """Run a Karger C++ binary and measure time + memory."""
    input_data = f"{V} {E} {trials}\n" + "\n".join(f"{s} {d}" for s, d in edges)
    
    proc = psutil.Popen(
        [exe_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    
    start = time.time()
    proc.stdin.write(input_data)
    proc.stdin.close()
    
    peak_rss = 0
    while proc.is_running():
        try:
            peak_rss = max(peak_rss, proc.memory_info().rss)
        except psutil.Error:
            break
        time.sleep(0.01)
    
    try:
        peak_rss = max(peak_rss, proc.memory_info().rss)
    except psutil.Error:
        pass
    
    out, _ = proc.communicate()
    mincut,elapsed = out.strip().split()
    
    return int(mincut) if out.strip() else 0, float(elapsed), peak_rss / (1024 * 1024)


def run_stoer_wagner(exe_name, V, E, edges):
    """Run Stoer-Wagner C++ binary and return result only."""
    input_data = f"{V} {E}\n" + "\n".join(f"{s} {d} 1" for s, d in edges)
    
    proc = subprocess.Popen(
        [exe_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    
    proc.stdin.write(input_data)
    proc.stdin.close()
    
    out, _ = proc.communicate()
    
    return int(out.strip()) if out.strip() else 0


print("Compiling C++ binaries...")
os.system("g++ -O3 -o kargercppver.exe kargercppver.cpp")
os.system("g++ -O3 -o kargercppopt.exe kargercppopt.cpp")
os.system("g++ -O3 -o stoer_wagner.exe stoer_wagner.cpp")

print("\n" + "="*120)
print("KARGER COMPARISON: Standard (100 trials) vs Optimized (10 trials) vs Stoer-Wagner (exact)")
print("="*120)
print("\nGenerating random sparse and dense graphs (100 vertices)...\n")

results = []
errors = []

for graph_type in ['sparse', 'dense']:
    print(f"\n{graph_type.upper()} GRAPHS:")
    print(f"{'Graph':<8} {'SW':<8} {'Ver100':<10} {'Opt10':<10} {'Error%':<12} {'Ver-Time':<12} {'Opt-Time':<12}")
    print("-" * 120)
    
    for i in range(10):
        G = generate_graph(800, graph_type)
        V = len(G)
        edges = [(r, c) for r in range(V) for c in range(r+1, V) if G[r][c] == 1]
        E = len(edges)
        
        # Stoer-Wagner (exact answer)
        sw_result = run_stoer_wagner("stoer_wagner.exe", V, E, edges)
        
        # Karger standard (100 trials)
        ver_result, ver_t, ver_m = run_karger("kargercppver.exe", V, E, edges, trials=100)
        
        # Karger optimized (10 trials)
        opt_result, opt_t, opt_m = run_karger("kargercppopt.exe", V, E, edges, trials=100)
        
        # Calculate error percentages
        ver_error = ((ver_result - sw_result) / sw_result * 100) if sw_result > 0 else 0
        opt_error = ((opt_result - sw_result) / sw_result * 100) if sw_result > 0 else 0
        
        print(f"{i+1:<8} {sw_result:<8} {ver_result:<10} {opt_result:<10} V:{ver_error:+.1f}% O:{opt_error:+.1f}% {ver_t:<12.4f} {opt_t:<12.4f}")
        
        results.append({
            'type': graph_type,
            'graph': i+1,
            'V': V,
            'E': E,
            'sw_result': sw_result,
            'ver_result': ver_result,
            'opt_result': opt_result,
            'ver_error_pct': ver_error,
            'opt_error_pct': opt_error,
            'ver_time': ver_t,
            'opt_time': opt_t,
        })
        
        # Track errors
        if ver_result != sw_result:
            errors.append(('Standard', graph_type, i+1, sw_result, ver_result, ver_error))
        if opt_result != sw_result:
            errors.append(('Optimized', graph_type, i+1, sw_result, opt_result, opt_error))

# Summary
print("\n" + "="*120)
print("ERROR ANALYSIS")
print("="*120)

if errors:
    print(f"\n⚠️  {len(errors)} APPROXIMATION ERRORS FOUND:")
    print(f"{'Impl':<15} {'Type':<8} {'Graph':<8} {'SW':<8} {'Karger':<8} {'Error%':<12}")
    print("-" * 60)
    for impl, gtype, gnum, sw, karger, err in errors:
        print(f"{impl:<15} {gtype:<8} {gnum:<8} {sw:<8} {karger:<8} {err:+.2f}%")
else:
    print("\n✓ All Karger results match Stoer-Wagner (lucky day!)!")

ver_errors = [abs(r['ver_error_pct']) for r in results]
opt_errors = [abs(r['opt_error_pct']) for r in results]

print(f"\nAverage Absolute Error:")
print(f"  Standard (100 trials):  {sum(ver_errors)/len(ver_errors):.2f}%")
print(f"  Optimized (10 trials):  {sum(opt_errors)/len(opt_errors):.2f}%")

ver_times = [r['ver_time'] for r in results]
opt_times = [r['opt_time'] for r in results]

avg_ver_t = sum(ver_times) / len(ver_times)
avg_opt_t = sum(opt_times) / len(opt_times)

print(f"\nAverage Time:")
print(f"  Standard:  {avg_ver_t:.4f}s (100 trials)")
print(f"  Optimized: {avg_opt_t:.4f}s (10 trials)")
print(f"  Speedup:   {avg_ver_t / avg_opt_t:.2f}x")

# Save results
with open('results/karger_error_analysis.txt', 'w') as f:
    f.write("Graph Type | Graph # | V | E | Stoer-Wagner | Karger-Std | Karger-Opt | Std-Error% | Opt-Error% | Std-Time | Opt-Time\n")
    f.write("-" * 140 + "\n")
    for r in results:
        f.write(f"{r['type']:<11} | {r['graph']:<7} | {r['V']:<4} | {r['E']:<5} | {r['sw_result']:<12} | {r['ver_result']:<10} | {r['opt_result']:<10} | {r['ver_error_pct']:+8.2f}% | {r['opt_error_pct']:+8.2f}% | {r['ver_time']:<8.4f} | {r['opt_time']:<8.4f}\n")

print(f"\n✓ Error analysis saved to results/karger_error_analysis.txt")
