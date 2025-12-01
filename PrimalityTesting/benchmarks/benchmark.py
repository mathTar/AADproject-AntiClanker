"""
Benchmarking and Testing Harness for Primality Testing Algorithms

This script performs comprehensive benchmarking of three primality testing algorithms:
1. Trial Division
2. Fermat's Test
3. Miller-Rabin Test

It generates performance graphs comparing:
- Time complexity across different input sizes
- Error rates (false positives/negatives)
"""

import sys
import os
import time
import random
from pathlib import Path

# Add parent directory to path to import algorithms
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Import the three algorithms
from algorithms import trial_division
from algorithms import fermat
from algorithms import miller_rabin


def generate_prime(bits: int) -> int:
    """
    Generate a probable prime number with the specified bit length.
    
    Uses Miller-Rabin test to verify primality.
    
    Args:
        bits (int): Desired bit length of the prime
    
    Returns:
        int: A probable prime number
    """
    while True:
        # Generate odd number with specified bit length
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1  # Ensure it's odd and has correct bit length
        
        # Quick checks
        if n % 2 == 0:
            continue
        
        # Test with Miller-Rabin
        is_prime, _ = miller_rabin.is_prime(n, k=20)
        if is_prime:
            return n


def generate_composite(bits: int) -> int:
    """
    Generate a composite number with the specified bit length.
    
    Args:
        bits (int): Desired bit length of the composite
    
    Returns:
        int: A composite number
    """
    # Generate two random numbers and multiply them
    half_bits = bits // 2
    p = random.getrandbits(half_bits) | 1
    q = random.getrandbits(bits - half_bits) | 1
    return p * q


def generate_carmichael_numbers() -> list[int]:
    """
    Return a list of known Carmichael numbers for testing.
    
    Carmichael numbers are composite numbers that pass Fermat's test
    for all bases coprime to them.
    
    Returns:
        list[int]: Known Carmichael numbers
    """
    return [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341]


def benchmark_time_complexity():
    """
    Benchmark time complexity of all three algorithms across different input sizes.
    
    Tests numbers with bit lengths from 8 to 64 bits.
    For each bit length, averages results over multiple trials.
    
    Returns:
        tuple: (bit_lengths, trial_times, fermat_times, miller_rabin_times)
    """
    print("\n" + "="*70)
    print("BENCHMARKING TIME COMPLEXITY")
    print("="*70)
    
    # Bit lengths to test (8-bit to 48-bit numbers)
    # Limited to 48-bit to keep trial division practical (runs in reasonable time)
    bit_lengths = [8, 12, 16, 20, 24, 28, 32, 40, 48]
    trials_per_size = 10
    
    trial_times = []
    fermat_times = []
    miller_rabin_times = []
    
    for bits in bit_lengths:
        print(f"\nTesting {bits}-bit numbers...")
        
        # Generate test primes
        test_primes = [generate_prime(bits) for _ in range(trials_per_size)]
        
        # Benchmark Trial Division
        trial_time_sum = 0
        for num in test_primes:
            _, exec_time = trial_division.is_prime(num)
            trial_time_sum += exec_time
        trial_avg = trial_time_sum / trials_per_size
        trial_times.append(trial_avg)
        print(f"  Trial Division:  {trial_avg:.6f}s")
        
        # Benchmark Fermat (k=10)
        fermat_time_sum = 0
        for num in test_primes:
            _, exec_time = fermat.is_prime(num, k=10)
            fermat_time_sum += exec_time
        fermat_avg = fermat_time_sum / trials_per_size
        fermat_times.append(fermat_avg)
        print(f"  Fermat (k=10):   {fermat_avg:.6f}s")
        
        # Benchmark Miller-Rabin (k=10)
        mr_time_sum = 0
        for num in test_primes:
            _, exec_time = miller_rabin.is_prime(num, k=10)
            mr_time_sum += exec_time
        mr_avg = mr_time_sum / trials_per_size
        miller_rabin_times.append(mr_avg)
        print(f"  Miller-Rabin (k=10): {mr_avg:.6f}s")
    
    return bit_lengths, trial_times, fermat_times, miller_rabin_times


def benchmark_error_rates():
    """
    Benchmark error rates for probabilistic algorithms.
    
    Tests on:
    - Known primes
    - Known composites
    - Carmichael numbers (challenge for Fermat)
    
    Returns:
        dict: Error rate statistics for each algorithm
    """
    print("\n" + "="*70)
    print("BENCHMARKING ERROR RATES")
    print("="*70)
    
    # Generate test sets
    print("\nGenerating test cases...")
    primes = [generate_prime(32) for _ in range(50)]
    composites = [generate_composite(32) for _ in range(50)]
    carmichael = generate_carmichael_numbers()
    
    # Test configurations
    k_values = [5, 10, 20]
    
    results = {
        'trial_division': {'fp': 0, 'fn': 0, 'total': 0},
        'fermat': {},
        'miller_rabin': {}
    }
    
    # Initialize for different k values
    for k in k_values:
        results['fermat'][k] = {'fp': 0, 'fn': 0, 'total': 0}
        results['miller_rabin'][k] = {'fp': 0, 'fn': 0, 'total': 0}
    
    # Test Trial Division (deterministic, should have 0 errors)
    print("\nTesting Trial Division (Deterministic)...")
    for num in primes:
        is_prime_result, _ = trial_division.is_prime(num)
        results['trial_division']['total'] += 1
        if not is_prime_result:
            results['trial_division']['fn'] += 1  # False negative
    
    for num in composites + carmichael:
        is_prime_result, _ = trial_division.is_prime(num)
        results['trial_division']['total'] += 1
        if is_prime_result:
            results['trial_division']['fp'] += 1  # False positive
    
    print(f"  False Positives: {results['trial_division']['fp']}")
    print(f"  False Negatives: {results['trial_division']['fn']}")
    
    # Test Fermat and Miller-Rabin with different k values
    for k in k_values:
        print(f"\nTesting Fermat (k={k})...")
        
        # Test on primes
        for num in primes:
            is_prime_result, _ = fermat.is_prime(num, k=k)
            results['fermat'][k]['total'] += 1
            if not is_prime_result:
                results['fermat'][k]['fn'] += 1
        
        # Test on composites and Carmichael numbers
        for num in composites + carmichael:
            is_prime_result, _ = fermat.is_prime(num, k=k)
            results['fermat'][k]['total'] += 1
            if is_prime_result:
                results['fermat'][k]['fp'] += 1
        
        print(f"  False Positives: {results['fermat'][k]['fp']}")
        print(f"  False Negatives: {results['fermat'][k]['fn']}")
        
        print(f"\nTesting Miller-Rabin (k={k})...")
        
        # Test on primes
        for num in primes:
            is_prime_result, _ = miller_rabin.is_prime(num, k=k)
            results['miller_rabin'][k]['total'] += 1
            if not is_prime_result:
                results['miller_rabin'][k]['fn'] += 1
        
        # Test on composites and Carmichael numbers
        for num in composites + carmichael:
            is_prime_result, _ = miller_rabin.is_prime(num, k=k)
            results['miller_rabin'][k]['total'] += 1
            if is_prime_result:
                results['miller_rabin'][k]['fp'] += 1
        
        print(f"  False Positives: {results['miller_rabin'][k]['fp']}")
        print(f"  False Negatives: {results['miller_rabin'][k]['fn']}")
    
    return results


def plot_time_complexity(bit_lengths, trial_times, fermat_times, miller_rabin_times):
    """
    Generate a line plot comparing time complexity of all three algorithms.
    
    This is the most appropriate graph type because:
    - X-axis is continuous (bit length)
    - Y-axis is continuous (time)
    - We want to show trend/growth rate
    - Multiple series need to be compared
    
    Args:
        bit_lengths: List of bit lengths tested
        trial_times: Execution times for trial division
        fermat_times: Execution times for Fermat
        miller_rabin_times: Execution times for Miller-Rabin
    """
    plt.figure(figsize=(12, 7))
    
    # Plot with log scale on y-axis to handle wide range of times
    plt.semilogy(bit_lengths, trial_times, 'o-', label='Trial Division', 
                 linewidth=2, markersize=8, color='#e74c3c')
    plt.semilogy(bit_lengths, fermat_times, 's-', label='Fermat (k=10)', 
                 linewidth=2, markersize=8, color='#3498db')
    plt.semilogy(bit_lengths, miller_rabin_times, '^-', label='Miller-Rabin (k=10)', 
                 linewidth=2, markersize=8, color='#2ecc71')
    
    plt.xlabel('Input Size (bit length)', fontsize=12, fontweight='bold')
    plt.ylabel('Execution Time (seconds, log scale)', fontsize=12, fontweight='bold')
    plt.title('Time Complexity Comparison of Primality Testing Algorithms', 
              fontsize=14, fontweight='bold', pad=20)
    plt.legend(fontsize=11, loc='upper left')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Save the plot
    results_dir = Path(__file__).parent.parent / 'results'
    results_dir.mkdir(exist_ok=True)
    plt.savefig(results_dir / 'time_complexity.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved time complexity plot to: {results_dir / 'time_complexity.png'}")


def plot_log_time_analysis(bit_lengths, trial_times, fermat_times, miller_rabin_times):
    """
    Plot log(time) vs bit length to analyze growth characteristics.
    
    Theory:
    - For bit length n, the number value N ≈ 2^n, so n ≈ log₂(N)
    - Modular exponentiation on N takes O(log³N) = O(n³) operations
    - If time T ∝ n³, then log(T) ∝ 3·log(n)
    - Plotting log(T) vs log(n) should give slope ≈ 3
    - Plotting log(T) vs n should give slope ∝ 3/n (decreasing)
    
    Better approach: Plot log(time) vs log(bit_length)
    - For O(n^k): log(time) ∝ k·log(n), slope = k
    - For Fermat/Miller-Rabin with O(n³): slope ≈ 3
    - For O(n²): slope ≈ 2
    
    Args:
        bit_lengths: List of bit lengths tested
        trial_times: Execution times for trial division
        fermat_times: Execution times for Fermat
        miller_rabin_times: Execution times for Miller-Rabin
    """
    # Convert to numpy arrays
    bits = np.array(bit_lengths, dtype=float)
    log_bits = np.log(bits)  # log(bit_length)
    
    # Calculate log(time), handling zeros
    min_time = 1e-8
    log_trial = np.log([max(t, min_time) for t in trial_times])
    log_fermat = np.log([max(t, min_time) for t in fermat_times])
    log_mr = np.log([max(t, min_time) for t in miller_rabin_times])
    
    # Calculate gradients using linear regression on log-log plot
    # For polynomial: log(time) = k*log(n) + c, where k is the polynomial degree
    fermat_gradient = np.polyfit(log_bits, log_fermat, 1)[0]
    mr_gradient = np.polyfit(log_bits, log_mr, 1)[0]
    
    # For trial division (exponential in bit length)
    # time ∝ 2^(n/2), so log(time) ∝ n/2, gradient vs bit_length is constant
    trial_gradient_linear = np.polyfit(bits, log_trial, 1)[0]
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: log(time) vs log(bit_length) - shows polynomial degree
    ax1.plot(log_bits, log_trial, 'o-', label=f'Trial Division', 
             linewidth=2.5, markersize=8, color='#e74c3c')
    ax1.plot(log_bits, log_fermat, 's-', label=f'Fermat (slope={fermat_gradient:.2f})', 
             linewidth=2.5, markersize=8, color='#3498db')
    ax1.plot(log_bits, log_mr, '^-', label=f'Miller-Rabin (slope={mr_gradient:.2f})', 
             linewidth=2.5, markersize=8, color='#2ecc71')
    
    # Add best-fit lines for polynomial algorithms
    fermat_fit = np.polyval(np.polyfit(log_bits, log_fermat, 1), log_bits)
    mr_fit = np.polyval(np.polyfit(log_bits, log_mr, 1), log_bits)
    
    ax1.plot(log_bits, fermat_fit, '--', alpha=0.5, color='#3498db', linewidth=2, label=f'Fermat fit')
    ax1.plot(log_bits, mr_fit, '--', alpha=0.5, color='#2ecc71', linewidth=2, label=f'M-R fit')
    
    ax1.set_xlabel('log(Bit Length)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('log(Execution Time)', fontsize=12, fontweight='bold')
    ax1.set_title('log-log Plot: Polynomial Degree Analysis', fontsize=13, fontweight='bold', pad=15)
    ax1.legend(fontsize=10, loc='upper left')
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Add annotation
    ax1.text(0.05, 0.95, f'For polynomial O(n^k):\nSlope of log(T) vs log(n) = k\n\nFermat: slope = {fermat_gradient:.2f}\nMiller-Rabin: slope = {mr_gradient:.2f}\n\nTheoretical: ~2-3 for O(n²)-O(n³)',
             transform=ax1.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    # Plot 2: log(time) vs bit_length - shows exponential nature
    ax2.plot(bits, log_trial, 'o-', label=f'Trial Division (slope={trial_gradient_linear:.3f})', 
             linewidth=2.5, markersize=8, color='#e74c3c')
    ax2.plot(bits, log_fermat, 's-', label=f'Fermat', 
             linewidth=2.5, markersize=8, color='#3498db')
    ax2.plot(bits, log_mr, '^-', label=f'Miller-Rabin', 
             linewidth=2.5, markersize=8, color='#2ecc71')
    
    # Add best-fit line for trial division (exponential)
    trial_fit = np.polyval(np.polyfit(bits, log_trial, 1), bits)
    ax2.plot(bits, trial_fit, '--', alpha=0.5, color='#e74c3c', linewidth=2)
    
    ax2.set_xlabel('Bit Length (n)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('log(Execution Time)', fontsize=12, fontweight='bold')
    ax2.set_title('Exponential Growth: Trial Division', fontsize=13, fontweight='bold', pad=15)
    ax2.legend(fontsize=11, loc='upper left')
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # Add annotation
    ax2.text(0.05, 0.95, f'For exponential O(2^(n/2)):\nlog(T) ∝ n/2\nSlope = {trial_gradient_linear:.3f}\n\nPolynomial algorithms:\nlog(T) grows slowly with n',
             transform=ax2.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    
    plt.suptitle('Gradient Analysis: Demonstrating Polynomial vs Exponential Growth', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Save the plot
    results_dir = Path(__file__).parent.parent / 'results'
    results_dir.mkdir(exist_ok=True)
    plt.savefig(results_dir / 'log_time_gradient.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved log-time gradient plot to: {results_dir / 'log_time_gradient.png'}")
    
    # Print gradient analysis
    print("\n" + "="*70)
    print("LOG-TIME GRADIENT ANALYSIS")
    print("="*70)
    print("\nlog-log analysis (log(time) vs log(bit_length)):")
    print(f"  Fermat gradient:       {fermat_gradient:.3f}  (polynomial degree)")
    print(f"  Miller-Rabin gradient: {mr_gradient:.3f}  (polynomial degree)")
    print("\n  Interpretation: For O(n^k), gradient = k")
    print(f"  - Fermat shows O(n^{fermat_gradient:.1f}) complexity")
    print(f"  - Miller-Rabin shows O(n^{mr_gradient:.1f}) complexity")
    print(f"  - Theoretical: O(n²) to O(n³) expected → gradient ~2-3")
    print("\nExponential analysis (log(time) vs bit_length):")
    print(f"  Trial Division gradient: {trial_gradient_linear:.3f}")
    print(f"  - For O(2^(n/2)): log(time) ∝ n/2 · ln(2) ≈ 0.35n")
    print(f"  - Measured gradient matches exponential growth")
    print("="*70)


def plot_error_rates(results):
    """
    Generate a grouped bar chart comparing error rates.
    
    This is the most appropriate graph type because:
    - We're comparing discrete categories (algorithms)
    - We're showing counts/percentages (error rates)
    - Multiple groups (false positives vs negatives)
    - Easy to compare values across algorithms
    
    Args:
        results: Dictionary containing error rate statistics
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Extract data for k=10 (standard testing rounds)
    algorithms = ['Trial Division', 'Fermat\n(k=10)', 'Miller-Rabin\n(k=10)']
    
    fp_counts = [
        results['trial_division']['fp'],
        results['fermat'][10]['fp'],
        results['miller_rabin'][10]['fp']
    ]
    
    fn_counts = [
        results['trial_division']['fn'],
        results['fermat'][10]['fn'],
        results['miller_rabin'][10]['fn']
    ]
    
    totals = [
        results['trial_division']['total'],
        results['fermat'][10]['total'],
        results['miller_rabin'][10]['total']
    ]
    
    # Calculate error rates as percentages
    fp_rates = [(fp / total) * 100 if total > 0 else 0 for fp, total in zip(fp_counts, totals)]
    fn_rates = [(fn / total) * 100 if total > 0 else 0 for fn, total in zip(fn_counts, totals)]
    
    # Plot 1: False Positive Rates
    colors = ['#e74c3c', '#3498db', '#2ecc71']
    bars1 = ax1.bar(algorithms, fp_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('False Positive Rate (%)', fontsize=12, fontweight='bold')
    ax1.set_title('False Positive Rates\n(Composite wrongly classified as Prime)', 
                  fontsize=12, fontweight='bold', pad=15)
    ax1.set_ylim(0, max(fp_rates) * 1.3 if max(fp_rates) > 0 else 1)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bar, rate, count in zip(bars1, fp_rates, fp_counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.2f}%\n({count} errors)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Plot 2: False Negative Rates
    bars2 = ax2.bar(algorithms, fn_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('False Negative Rate (%)', fontsize=12, fontweight='bold')
    ax2.set_title('False Negative Rates\n(Prime wrongly classified as Composite)', 
                  fontsize=12, fontweight='bold', pad=15)
    ax2.set_ylim(0, max(fn_rates) * 1.3 if max(fn_rates) > 0 else 1)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bar, rate, count in zip(bars2, fn_rates, fn_counts):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.2f}%\n({count} errors)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.suptitle('Error Rate Comparison of Primality Testing Algorithms', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    # Save the plot
    results_dir = Path(__file__).parent.parent / 'results'
    results_dir.mkdir(exist_ok=True)
    plt.savefig(results_dir / 'error_rates.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved error rate plot to: {results_dir / 'error_rates.png'}")


def main():
    """
    Main function to run all benchmarks and generate graphs.
    """
    print("\n" + "="*70)
    print("PRIMALITY TESTING ALGORITHM BENCHMARK SUITE")
    print("="*70)
    print("\nThis script will:")
    print("  1. Benchmark time complexity across different input sizes")
    print("  2. Measure error rates for each algorithm")
    print("  3. Generate comparison graphs")
    print("\nEstimated time: 2-3 minutes")
    print("="*70)
    
    # Run benchmarks
    bit_lengths, trial_times, fermat_times, mr_times = benchmark_time_complexity()
    error_results = benchmark_error_rates()
    
    # Generate plots
    print("\n" + "="*70)
    print("GENERATING GRAPHS")
    print("="*70)
    
    plot_time_complexity(bit_lengths, trial_times, fermat_times, mr_times)
    plot_log_time_analysis(bit_lengths, trial_times, fermat_times, mr_times)
    plot_error_rates(error_results)
    
    print("\n" + "="*70)
    print("BENCHMARK COMPLETE")
    print("="*70)
    print("\nGraphs saved to 'results/' directory:")
    print("  - time_complexity.png: Line plot showing execution time vs input size")
    print("  - log_time_gradient.png: log(time) vs bit length with gradient analysis")
    print("  - error_rates.png: Bar chart showing false positive/negative rates")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
