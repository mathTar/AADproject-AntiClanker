#!/usr/bin/env python3
"""
Plotting script for QuickSort analysis
Generates comprehensive visualizations from benchmark data
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Create output directory
output_dir = Path("../img")
output_dir.mkdir(exist_ok=True)

# Load data
df = pd.read_csv("../csv/sorting_benchmark.csv")

print(f"Loaded {len(df)} benchmark records")
print(f"Algorithms: {df['Algorithm'].unique()}")
print(f"Datasets: {df['Dataset'].unique()}")
print(f"Size range: {df['Size'].min()} to {df['Size'].max()}")

# =============================================================================
# 1. ALL ALGORITHMS ON RANDOM DATASET
# =============================================================================

print("\n1. Plotting all algorithms on Random dataset...")

random_data = df[df['Dataset'] == 'Random'].groupby(['Algorithm', 'Size']).agg({
    'Time_ms': 'mean',
    'Comparisons': 'mean',
    'Swaps': 'mean'
}).reset_index()

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Time plot
for algo in random_data['Algorithm'].unique():
    algo_data = random_data[random_data['Algorithm'] == algo]
    axes[0].plot(algo_data['Size'], algo_data['Time_ms'], marker='o', label=algo, linewidth=2)

axes[0].set_xlabel('Input Size (n)')
axes[0].set_ylabel('Time (ms)')
axes[0].set_title('Execution Time vs Input Size\n(Random Dataset)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Comparisons plot
for algo in random_data['Algorithm'].unique():
    algo_data = random_data[random_data['Algorithm'] == algo]
    axes[1].plot(algo_data['Size'], algo_data['Comparisons'], marker='o', label=algo, linewidth=2)

axes[1].set_xlabel('Input Size (n)')
axes[1].set_ylabel('Number of Comparisons')
axes[1].set_title('Comparisons vs Input Size\n(Random Dataset)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Swaps plot
for algo in random_data['Algorithm'].unique():
    algo_data = random_data[random_data['Algorithm'] == algo]
    axes[2].plot(algo_data['Size'], algo_data['Swaps'], marker='o', label=algo, linewidth=2)

axes[2].set_xlabel('Input Size (n)')
axes[2].set_ylabel('Number of Swaps')
axes[2].set_title('Swaps vs Input Size\n(Random Dataset)')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '1_all_algorithms_random.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 2. ALL ALGORITHMS ON ALMOST SORTED DATASET
# =============================================================================

print("2. Plotting all algorithms on AlmostSorted dataset...")

almost_sorted_data = df[df['Dataset'] == 'AlmostSorted'].groupby(['Algorithm', 'Size']).agg({
    'Time_ms': 'mean',
    'Comparisons': 'mean',
    'Swaps': 'mean'
}).reset_index()

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Time plot
for algo in almost_sorted_data['Algorithm'].unique():
    algo_data = almost_sorted_data[almost_sorted_data['Algorithm'] == algo]
    axes[0].plot(algo_data['Size'], algo_data['Time_ms'], marker='o', label=algo, linewidth=2)

axes[0].set_xlabel('Input Size (n)')
axes[0].set_ylabel('Time (ms)')
axes[0].set_title('Execution Time vs Input Size\n(Almost Sorted Dataset - Worst Case for Naive)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Comparisons plot
for algo in almost_sorted_data['Algorithm'].unique():
    algo_data = almost_sorted_data[almost_sorted_data['Algorithm'] == algo]
    axes[1].plot(algo_data['Size'], algo_data['Comparisons'], marker='o', label=algo, linewidth=2)

axes[1].set_xlabel('Input Size (n)')
axes[1].set_ylabel('Number of Comparisons')
axes[1].set_title('Comparisons vs Input Size\n(Almost Sorted Dataset)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Swaps plot
for algo in almost_sorted_data['Algorithm'].unique():
    algo_data = almost_sorted_data[almost_sorted_data['Algorithm'] == algo]
    axes[2].plot(algo_data['Size'], algo_data['Swaps'], marker='o', label=algo, linewidth=2)

axes[2].set_xlabel('Input Size (n)')
axes[2].set_ylabel('Number of Swaps')
axes[2].set_title('Swaps vs Input Size\n(Almost Sorted Dataset)')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '2_all_algorithms_almost_sorted.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 3. NAIVE vs RANDOMIZED vs THREE-WAY ON LOW ENTROPY
# =============================================================================

print("3. Plotting Naive vs Randomized vs Three-Way on LowEntropy dataset...")

low_entropy_data = df[(df['Dataset'] == 'LowEntropy') & 
                      (df['Algorithm'].isin(['Naive', 'Randomized', 'ThreeWay']))].groupby(['Algorithm', 'Size']).agg({
    'Time_ms': 'mean',
    'Comparisons': 'mean',
    'Swaps': 'mean'
}).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Time plot
for algo in ['Naive', 'Randomized', 'ThreeWay']:
    algo_data = low_entropy_data[low_entropy_data['Algorithm'] == algo]
    axes[0].plot(algo_data['Size'], algo_data['Time_ms'], marker='o', label=algo, linewidth=2)

axes[0].set_xlabel('Input Size (n)')
axes[0].set_ylabel('Time (ms)')
axes[0].set_title('Execution Time vs Input Size\n(Low Entropy Dataset - 10 distinct values)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Add theoretical O(n log d) line for Three-Way
sizes = low_entropy_data['Size'].unique()
d = 10  # distinct values
theoretical = [n * np.log2(d) * 0.0001 for n in sizes]  # scaling factor
axes[0].plot(sizes, theoretical, '--', label='O(n log d) theoretical', alpha=0.5, color='gray')

# Comparisons plot
for algo in ['Naive', 'Randomized', 'ThreeWay']:
    algo_data = low_entropy_data[low_entropy_data['Algorithm'] == algo]
    axes[1].plot(algo_data['Size'], algo_data['Comparisons'], marker='o', label=algo, linewidth=2)

axes[1].set_xlabel('Input Size (n)')
axes[1].set_ylabel('Number of Comparisons')
axes[1].set_title('Comparisons vs Input Size\n(Low Entropy Dataset)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '3_low_entropy_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 4. VARIANCE ANALYSIS - NAIVE AND RANDOMIZED COMPARISON
# =============================================================================

print("4. Creating variance scatter plots for Naive and Randomized QuickSort...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# NAIVE: 50 runs Random + 50 runs AlmostSorted
naive_random = df[(df['Dataset'] == 'Random') & (df['Algorithm'] == 'Naive')]
naive_almost = df[(df['Dataset'] == 'AlmostSorted') & (df['Algorithm'] == 'Naive')]

# Time scatter - combine both datasets
axes[0, 0].scatter(naive_random['Size'], naive_random['Time_ms'], alpha=0.4, s=20, color='blue', label='Random (50 runs)')
axes[0, 0].scatter(naive_almost['Size'], naive_almost['Time_ms'], alpha=0.4, s=20, color='orange', label='AlmostSorted (50 runs)')
mean_times_rand = naive_random.groupby('Size')['Time_ms'].mean()
mean_times_almost = naive_almost.groupby('Size')['Time_ms'].mean()
axes[0, 0].plot(mean_times_rand.index, mean_times_rand.values, 'b-', linewidth=2, label='Mean (Random)')
axes[0, 0].plot(mean_times_almost.index, mean_times_almost.values, 'orange', linewidth=2, linestyle='--', label='Mean (AlmostSorted)')
axes[0, 0].set_xlabel('Input Size (n)')
axes[0, 0].set_ylabel('Time (ms)')
axes[0, 0].set_title('Naive QuickSort: Time Variance (100 runs total)')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Swaps scatter
axes[0, 1].scatter(naive_random['Size'], naive_random['Swaps'], alpha=0.4, s=20, color='blue', label='Random (50 runs)')
axes[0, 1].scatter(naive_almost['Size'], naive_almost['Swaps'], alpha=0.4, s=20, color='orange', label='AlmostSorted (50 runs)')
mean_swaps_rand = naive_random.groupby('Size')['Swaps'].mean()
mean_swaps_almost = naive_almost.groupby('Size')['Swaps'].mean()
axes[0, 1].plot(mean_swaps_rand.index, mean_swaps_rand.values, 'b-', linewidth=2, label='Mean (Random)')
axes[0, 1].plot(mean_swaps_almost.index, mean_swaps_almost.values, 'orange', linewidth=2, linestyle='--', label='Mean (AlmostSorted)')
axes[0, 1].set_xlabel('Input Size (n)')
axes[0, 1].set_ylabel('Number of Swaps')
axes[0, 1].set_title('Naive QuickSort: Swap Variance (100 runs total)')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# RANDOMIZED: 50 runs Random + 50 runs AlmostSorted
randomized_random = df[(df['Dataset'] == 'Random') & (df['Algorithm'] == 'Randomized')]
randomized_almost = df[(df['Dataset'] == 'AlmostSorted') & (df['Algorithm'] == 'Randomized')]

# Time scatter
axes[1, 0].scatter(randomized_random['Size'], randomized_random['Time_ms'], alpha=0.4, s=20, color='green', label='Random (50 runs)')
axes[1, 0].scatter(randomized_almost['Size'], randomized_almost['Time_ms'], alpha=0.4, s=20, color='purple', label='AlmostSorted (50 runs)')
mean_times_rand = randomized_random.groupby('Size')['Time_ms'].mean()
mean_times_almost = randomized_almost.groupby('Size')['Time_ms'].mean()
axes[1, 0].plot(mean_times_rand.index, mean_times_rand.values, 'g-', linewidth=2, label='Mean (Random)')
axes[1, 0].plot(mean_times_almost.index, mean_times_almost.values, 'purple', linewidth=2, linestyle='--', label='Mean (AlmostSorted)')
axes[1, 0].set_xlabel('Input Size (n)')
axes[1, 0].set_ylabel('Time (ms)')
axes[1, 0].set_title('Randomized QuickSort: Time Variance (100 runs total)')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Swaps scatter
axes[1, 1].scatter(randomized_random['Size'], randomized_random['Swaps'], alpha=0.4, s=20, color='green', label='Random (50 runs)')
axes[1, 1].scatter(randomized_almost['Size'], randomized_almost['Swaps'], alpha=0.4, s=20, color='purple', label='AlmostSorted (50 runs)')
mean_swaps_rand = randomized_random.groupby('Size')['Swaps'].mean()
mean_swaps_almost = randomized_almost.groupby('Size')['Swaps'].mean()
axes[1, 1].plot(mean_swaps_rand.index, mean_swaps_rand.values, 'g-', linewidth=2, label='Mean (Random)')
axes[1, 1].plot(mean_swaps_almost.index, mean_swaps_almost.values, 'purple', linewidth=2, linestyle='--', label='Mean (AlmostSorted)')
axes[1, 1].set_xlabel('Input Size (n)')
axes[1, 1].set_ylabel('Number of Swaps')
axes[1, 1].set_title('Randomized QuickSort: Swap Variance (100 runs total)')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '4_randomized_variance_scatter.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 5. VARIANCE ANALYSIS - BOX PLOTS (REMOVED)
# =============================================================================

# print("5. Creating box plots for variance analysis...")

# # Select a few representative sizes
# selected_sizes = [1000, 5000, 10000, 30000, 50000, 100000]
# variance_data = df[(df['Dataset'] == 'Random') & 
#                    (df['Algorithm'].isin(['Naive', 'Randomized', 'MedianOfThree'])) &
#                    (df['Size'].isin(selected_sizes))]

# fig, axes = plt.subplots(2, 3, figsize=(18, 10))
# axes = axes.flatten()

# for idx, size in enumerate(selected_sizes):
#     size_data = variance_data[variance_data['Size'] == size]
#     size_data.boxplot(column='Time_ms', by='Algorithm', ax=axes[idx])
#     axes[idx].set_title(f'n = {size}')
#     axes[idx].set_xlabel('Algorithm')
#     axes[idx].set_ylabel('Time (ms)')
#     axes[idx].get_figure().suptitle('')

# plt.suptitle('Time Variance Across Multiple Runs (Random Dataset)', fontsize=14, y=1.00)
# plt.tight_layout()
# plt.savefig(output_dir / '5_variance_boxplots.png', dpi=300, bbox_inches='tight')
# plt.close()

# =============================================================================
# 5. COMPARISONS VS THEORETICAL BOUNDS
# =============================================================================

print("5. Plotting comparisons vs theoretical bounds...")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Random dataset - show only Naive and Randomized
random_comp = df[df['Dataset'] == 'Random'].groupby(['Algorithm', 'Size'])['Comparisons'].mean().reset_index()

for algo in ['Naive', 'Randomized']:
    if algo in random_comp['Algorithm'].values:
        algo_data = random_comp[random_comp['Algorithm'] == algo]
        axes[0].plot(algo_data['Size'], algo_data['Comparisons'], marker='o', label=algo, linewidth=2)

sizes = sorted(random_comp['Size'].unique())
theoretical_avg = [2 * n * np.log(n) for n in sizes]
theoretical_worst = [n * n for n in sizes]
axes[0].plot(sizes, theoretical_avg, '--', label='2n ln(n) expected', alpha=0.5, color='green')
axes[0].set_xlabel('Input Size (n)')
axes[0].set_ylabel('Number of Comparisons')
axes[0].set_title('Comparisons: Random Dataset')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Almost sorted dataset - show only Naive and Randomized
almost_comp = df[df['Dataset'] == 'AlmostSorted'].groupby(['Algorithm', 'Size'])['Comparisons'].mean().reset_index()

for algo in ['Naive', 'Randomized']:
    if algo in almost_comp['Algorithm'].values:
        algo_data = almost_comp[almost_comp['Algorithm'] == algo]
        axes[1].plot(algo_data['Size'], algo_data['Comparisons'], marker='o', label=algo, linewidth=2)

axes[1].plot(sizes, theoretical_avg, '--', label='2n ln(n) expected', alpha=0.5, color='green')
# axes[1].plot(sizes[:len(sizes)//2], [n*n for n in sizes[:len(sizes)//2]], '--', 
#              label='n² worst case', alpha=0.5, color='red')
axes[1].set_xlabel('Input Size (n)')
axes[1].set_ylabel('Number of Comparisons')
axes[1].set_title('Comparisons: Almost Sorted Dataset\n(Naive shows O(n²) behavior)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Low entropy dataset
low_comp = df[df['Dataset'] == 'LowEntropy'].groupby(['Algorithm', 'Size'])['Comparisons'].mean().reset_index()

for algo in ['Naive', 'Randomized', 'ThreeWay']:
    if algo in low_comp['Algorithm'].values:
        algo_data = low_comp[low_comp['Algorithm'] == algo]
        axes[2].plot(algo_data['Size'], algo_data['Comparisons'], marker='o', label=algo, linewidth=2)

d = 10
theoretical_low = [2 * n * np.log(d) for n in sizes]
axes[2].plot(sizes, theoretical_low, '--', label='2n ln(d) for d=10', alpha=0.5, color='purple')
axes[2].set_xlabel('Input Size (n)')
axes[2].set_ylabel('Number of Comparisons')
axes[2].set_title('Comparisons: Low Entropy Dataset\n(Three-Way achieves O(n log d))')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '5_comparisons_vs_theoretical.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 7. SWAPS ANALYSIS (REMOVED)
# =============================================================================

# print("7. Plotting swaps analysis...")

# fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# datasets = ['Random', 'AlmostSorted', 'LowEntropy']
# titles = ['Random Dataset', 'Almost Sorted Dataset', 'Low Entropy Dataset']

# for idx, (dataset, title) in enumerate(zip(datasets, titles)):
#     dataset_swaps = df[df['Dataset'] == dataset].groupby(['Algorithm', 'Size'])['Swaps'].mean().reset_index()
    
#     for algo in dataset_swaps['Algorithm'].unique():
#         if algo == 'std::sort':
#             continue
#         algo_data = dataset_swaps[dataset_swaps['Algorithm'] == algo]
#         axes[idx].plot(algo_data['Size'], algo_data['Swaps'], marker='o', label=algo, linewidth=2)
    
#     axes[idx].set_xlabel('Input Size (n)')
#     axes[idx].set_ylabel('Number of Swaps')
#     axes[idx].set_title(f'Swaps vs Input Size\n({title})')
#     axes[idx].legend()
#     axes[idx].grid(True, alpha=0.3)

# plt.tight_layout()
# plt.savefig(output_dir / '7_swaps_analysis.png', dpi=300, bbox_inches='tight')
# plt.close()

# =============================================================================
# 6. RECURSION DEPTH ANALYSIS
# =============================================================================

print("6. Plotting recursion depth analysis...")

depth_data = df.groupby(['Algorithm', 'Dataset', 'Size'])['MaxDepth'].mean().reset_index()

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, dataset in enumerate(['Random', 'AlmostSorted', 'LowEntropy']):
    dataset_depth = depth_data[depth_data['Dataset'] == dataset]
    
    for algo in dataset_depth['Algorithm'].unique():
        algo_data = dataset_depth[dataset_depth['Algorithm'] == algo]
        if algo_data['MaxDepth'].sum() > 0:  # Only plot algorithms with non-zero depth
            axes[idx].plot(algo_data['Size'], algo_data['MaxDepth'], marker='o', label=algo, linewidth=2)
    
    # Add theoretical O(log n) reference line
    sizes_sorted = sorted(dataset_depth['Size'].unique())
    axes[idx].plot(sizes_sorted, [np.log2(n) for n in sizes_sorted], '--', 
                   label='log₂(n)', alpha=0.5, color='green', linewidth=1.5)
    
    axes[idx].set_xlabel('Input Size (n)', fontsize=12)
    axes[idx].set_ylabel('Maximum Recursion Depth', fontsize=12)
    axes[idx].set_title(f'Recursion Depth\\n({dataset} Dataset)', fontsize=13)
    axes[idx].legend(fontsize=10)
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '6_recursion_depth.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 9. ALGORITHM COMPARISON HEATMAP (REMOVED)
# =============================================================================

# print("9. Creating algorithm comparison heatmap...")

# # Create a summary table
# summary = df.groupby(['Algorithm', 'Dataset']).agg({
#     'Time_ms': 'mean',
#     'Comparisons': 'mean',
#     'Swaps': 'mean'
# }).reset_index()

# # Pivot for time
# time_pivot = summary.pivot(index='Algorithm', columns='Dataset', values='Time_ms')

# plt.figure(figsize=(10, 8))
# sns.heatmap(time_pivot, annot=True, fmt='.2f', cmap='YlOrRd', cbar_kws={'label': 'Average Time (ms)'})
# plt.title('Average Execution Time Across Algorithms and Datasets', fontsize=14)
# plt.ylabel('Algorithm')
# plt.xlabel('Dataset Type')
# plt.tight_layout()
# plt.savefig(output_dir / '9_algorithm_heatmap.png', dpi=300, bbox_inches='tight')
# plt.close()

# =============================================================================
# 7. TIME COMPLEXITY SCALING (LINEAR SCALE)
# =============================================================================

print("7. Creating time complexity scaling plots (linear scale)...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Linear plot for Random dataset
random_time = df[df['Dataset'] == 'Random'].groupby(['Algorithm', 'Size'])['Time_ms'].mean().reset_index()
for algo in random_time['Algorithm'].unique():
    algo_data = random_time[random_time['Algorithm'] == algo]
    axes[0].plot(algo_data['Size'], algo_data['Time_ms'], marker='o', label=algo, linewidth=2)

sizes = sorted(random_time['Size'].unique())
axes[0].plot(sizes, [n * np.log2(n) * 0.0001 for n in sizes], '--', 
                   label='O(n log n)', alpha=0.5, color='green')
axes[0].set_xlabel('Input Size (n)', fontsize=12)
axes[0].set_ylabel('Time (ms)', fontsize=12)
axes[0].set_title('Time Complexity Scaling (Linear)\nRandom Dataset', fontsize=13)
axes[0].legend(fontsize=9)
axes[0].grid(True, alpha=0.3)

# Linear plot for Almost Sorted
almost_time = df[df['Dataset'] == 'AlmostSorted'].groupby(['Algorithm', 'Size'])['Time_ms'].mean().reset_index()
for algo in almost_time['Algorithm'].unique():
    algo_data = almost_time[almost_time['Algorithm'] == algo]
    axes[1].plot(algo_data['Size'], algo_data['Time_ms'], marker='o', label=algo, linewidth=2)

axes[1].plot(sizes, [n * np.log2(n) * 0.0001 for n in sizes], '--', 
                   label='O(n log n)', alpha=0.5, color='green')
axes[1].set_xlabel('Input Size (n)', fontsize=12)
axes[1].set_ylabel('Time (ms)', fontsize=12)
axes[1].set_title('Time Complexity Scaling (Linear)\nAlmost Sorted Dataset', fontsize=13)
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '7_time_complexity_scaling_linear.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 8. QUICKSORT VARIANTS COMPARISON: NAIVE, RANDOMIZED, AND MOM
# =============================================================================

print("8. Creating QuickSort variants comparison across datasets...")

fig, axes = plt.subplots(3, 3, figsize=(18, 14))

quicksort_variants = ['Naive', 'Randomized', 'MoM']
datasets = ['Random', 'AlmostSorted', 'LowEntropy']
metrics = ['Time_ms', 'Comparisons', 'Swaps']
metric_labels = ['Time (ms)', 'Number of Comparisons', 'Number of Swaps']

for row, metric in enumerate(metrics):
    for col, dataset in enumerate(datasets):
        ax = axes[row, col]
        
        # Get data for this dataset and metric
        dataset_data = df[df['Dataset'] == dataset].groupby(['Algorithm', 'Size'])[metric].mean().reset_index()
        
        # Plot each QuickSort variant
        for algo in quicksort_variants:
            if algo in dataset_data['Algorithm'].unique():
                algo_data = dataset_data[dataset_data['Algorithm'] == algo]
                ax.plot(algo_data['Size'], algo_data[metric], marker='o', label=algo, linewidth=2, markersize=4)
        
        # Add theoretical reference lines for comparisons
        if metric == 'Comparisons':
            sizes_sorted = sorted(dataset_data['Size'].unique())
            if dataset == 'LowEntropy':
                # O(n log d) for d=10
                ax.plot(sizes_sorted, [2 * n * np.log(10) for n in sizes_sorted], '--', 
                       label='2n ln(10)', alpha=0.5, color='purple', linewidth=1.5)
            else:
                # O(n log n)
                ax.plot(sizes_sorted, [2 * n * np.log2(n) for n in sizes_sorted], '--', 
                       label='2n log₂(n)', alpha=0.5, color='green', linewidth=1.5)
        
        # Set labels and title
        ax.set_xlabel('Input Size (n)', fontsize=10)
        ax.set_ylabel(metric_labels[row], fontsize=10)
        
        if row == 0:
            ax.set_title(f'{dataset} Dataset', fontsize=12, fontweight='bold')
        
        ax.legend(fontsize=8, loc='best')
        ax.grid(True, alpha=0.3)
        
        # Use log scale for better visualization if values span multiple orders of magnitude
        if metric in ['Comparisons', 'Swaps'] and dataset != 'LowEntropy':
            ax.set_yscale('log')

plt.suptitle('QuickSort Variants Comparison: Naive vs Randomized vs Median-of-Medians', 
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig(output_dir / '8_quicksort_variants_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 9. COMPREHENSIVE SUMMARY STATISTICS
# =============================================================================

print("10. Generating summary statistics...")

summary_stats = df.groupby(['Algorithm', 'Dataset']).agg({
    'Time_ms': ['mean', 'std', 'min', 'max'],
    'Comparisons': ['mean', 'std'],
    'Swaps': ['mean', 'std'],
    'MaxDepth': 'mean'
}).round(2)

print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)
print(summary_stats)

# Save to CSV
summary_stats.to_csv(output_dir / 'summary_statistics.csv')

print("\n" + "="*80)
print("ALL PLOTS GENERATED SUCCESSFULLY!")
print("="*80)
print(f"\nOutput directory: {output_dir.absolute()}")
print("\nGenerated plots:")
print("  1. 1_all_algorithms_random.png - All algorithms on random dataset")
print("  2. 2_all_algorithms_almost_sorted.png - All algorithms on almost sorted dataset")
print("  3. 3_low_entropy_comparison.png - Naive vs Randomized vs Three-Way on duplicates")
print("  4. 4_randomized_variance_scatter.png - Variance analysis for randomized quicksort")
print("  5. 5_comparisons_vs_theoretical.png - Empirical vs theoretical comparisons")
print("  6. 6_recursion_depth.png - Recursion depth analysis")
print("  7. 7_time_complexity_scaling_linear.png - Time complexity scaling (linear plots)")
print("  8. 8_quicksort_variants_comparison.png - QuickSort variants (Naive/Randomized/MoM) across datasets")
print("  9. 9_swaps_loglog_analysis.png - Comprehensive swaps analysis (log-log plots)")
print(" 10. 10_summary_table.png - Summary statistics table")
print(" 11. summary_statistics.csv - Statistical summary (CSV)")

print("\n" + "="*80)

# =============================================================================
# 9. COMPREHENSIVE SWAPS ANALYSIS (LOG-LOG PLOTS)
# =============================================================================

print("9. Creating comprehensive swaps analysis (log-log plots)...")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

datasets = ['Random', 'AlmostSorted', 'LowEntropy']
dataset_titles = ['Random Dataset', 'Almost Sorted Dataset', 'Low Entropy Dataset']

for idx, (dataset, title) in enumerate(zip(datasets, dataset_titles)):
    ax = axes[idx]
    
    # Get swaps data for this dataset
    dataset_swaps = df[df['Dataset'] == dataset].groupby(['Algorithm', 'Size'])['Swaps'].mean().reset_index()
    
    # Plot each algorithm (exclude those with zero swaps)
    for algo in dataset_swaps['Algorithm'].unique():
        algo_data = dataset_swaps[dataset_swaps['Algorithm'] == algo]
        # Only plot if there are non-zero swaps
        if algo_data['Swaps'].max() > 0:
            ax.loglog(algo_data['Size'], algo_data['Swaps'], marker='o', label=algo, linewidth=2, markersize=5)
    
    # Add theoretical reference lines
    sizes_sorted = sorted(dataset_swaps['Size'].unique())
    
    # O(n log n) reference
    ax.loglog(sizes_sorted, [n * np.log2(n) * 0.5 for n in sizes_sorted], '--', 
             label='O(n log n)', alpha=0.5, color='green', linewidth=1.5)
    
    # O(n²) reference for almost sorted (if Naive present)
    if dataset == 'AlmostSorted':
        ax.loglog(sizes_sorted[:10], [n * n * 0.01 for n in sizes_sorted[:10]], '--', 
                 label='O(n²)', alpha=0.5, color='red', linewidth=1.5)
    
    ax.set_xlabel('Input Size (n)', fontsize=12)
    ax.set_ylabel('Number of Swaps (log scale)', fontsize=12)
    ax.set_title(f'Swaps Analysis (Log-Log)\\n{title}', fontsize=13)
    ax.legend(fontsize=9, loc='best')
    ax.grid(True, alpha=0.3, which='both')

plt.suptitle('Comprehensive Swaps Analysis Across All Algorithms and Datasets', 
             fontsize=14, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig(output_dir / '9_swaps_loglog_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 10. SUMMARY STATISTICS TABLE (FIXED WITH MERGED CELLS)
# =============================================================================

print("10. Creating summary statistics table...")

import matplotlib.patches as mpatches

# Create a more readable summary for visualization
summary_table = df.groupby(['Algorithm', 'Dataset']).agg({
    'Time_ms': 'mean',
    'Comparisons': 'mean',
    'Swaps': 'mean',
    'MaxDepth': 'mean'
}).round(2)

# Reorganize data by dataset
datasets = ['Random', 'AlmostSorted', 'LowEntropy']
dataset_names = {'Random': 'Random', 'AlmostSorted': 'Almost Sorted', 'LowEntropy': 'Low Entropy'}
algorithms = sorted(df['Algorithm'].unique())

# Build flat table data (leave dataset column empty, we'll draw merged cells manually)
table_data = []
table_data.append(['Dataset', 'Algorithm', 'Avg Time (ms)', 'Avg Comparisons', 'Avg Swaps', 'Avg Max Depth'])

dataset_row_ranges = {}  # Track row ranges for each dataset

row_idx = 1
for dataset in datasets:
    start_row = row_idx
    dataset_algos = [(algo, summary_table.loc[(algo, dataset)]) 
                     for algo in algorithms if (algo, dataset) in summary_table.index]
    
    for algo, row in dataset_algos:
        table_data.append([
            '',  # Empty - we'll add merged text manually
            algo,
            f"{row['Time_ms']:.2f}",
            f"{row['Comparisons']:.0f}",
            f"{row['Swaps']:.0f}",
            f"{row['MaxDepth']:.2f}"
        ])
        row_idx += 1
    
    dataset_row_ranges[dataset] = (start_row, row_idx - 1)

# Create figure
fig, ax = plt.subplots(figsize=(14, 12))
ax.axis('off')

# Create table
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.15, 0.22, 0.13, 0.18, 0.15, 0.15])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.8)

# Style header row
for i in range(6):
    cell = table[(0, i)]
    cell.set_facecolor('#4472C4')
    cell.set_text_props(weight='bold', color='white', fontsize=10)

# Style data rows and create merged dataset cells
for dataset in datasets:
    start_row, end_row = dataset_row_ranges[dataset]
    
    # Get the cell positions for merging
    first_cell = table[(start_row, 0)]
    last_cell = table[(end_row, 0)]
    
    # Set background color for all cells in this dataset's first column
    for r in range(start_row, end_row + 1):
        table[(r, 0)].set_facecolor('#D9E1F2')
        # Make cell borders invisible for middle cells
        if r > start_row:
            table[(r, 0)].set_edgecolor('#D9E1F2')
        
        # Alternate row colors for data columns
        row_in_group = r - start_row
        if row_in_group % 2 == 0:
            row_color = '#F2F2F2'
        else:
            row_color = '#E7E6E6'
        
        for col in range(1, 6):
            table[(r, col)].set_facecolor(row_color)
    
    # Add dataset name text to the middle of the merged area
    middle_row = (start_row + end_row) // 2
    table[(middle_row, 0)].get_text().set_text(dataset_names[dataset])
    table[(middle_row, 0)].set_text_props(weight='bold', fontsize=10, va='center')

# Add title
ax.set_title('Summary Statistics: Average Performance Across All Algorithms and Datasets',
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(output_dir / '10_summary_table.png', dpi=300, bbox_inches='tight')
plt.close()
print("\n" + "="*80)
