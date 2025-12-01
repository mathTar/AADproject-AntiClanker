# Primality Testing Algorithm Comparison

A comprehensive comparison of three primality testing algorithms: Trial Division, Fermat's Test, and Miller-Rabin Test.

## Overview

This project implements and benchmarks three different primality testing algorithms to compare their:
- **Time Complexity**: Execution time across different input sizes
- **Error Rates**: Accuracy in identifying prime vs composite numbers

## Algorithms Implemented

1. **Trial Division**: Deterministic algorithm that checks divisibility up to √n
2. **Fermat's Primality Test**: Probabilistic algorithm based on Fermat's Little Theorem
3. **Miller-Rabin Test**: Probabilistic algorithm with better accuracy than Fermat

## Project Structure

```
aadCodes/
├── algorithms/
│   ├── trial_division.py    # Trial division implementation
│   ├── fermat.py             # Fermat primality test
│   └── miller_rabin.py       # Miller-Rabin test
├── utils/
│   └── helpers.py            # Helper functions (GCD, etc.)
├── benchmarks/
│   └── benchmark.py          # Benchmarking and testing harness
├── results/
│   └── (generated plots)     # Performance graphs
├── ogFiles/                  # Original implementation files
└── README.md
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies

```powershell
pip install numpy matplotlib scipy
```

Or use the requirements file:

```powershell
pip install -r requirements.txt
```

## Usage

### Run Benchmarks

To run the complete benchmarking suite and generate performance graphs:

```powershell
python benchmarks\benchmark.py
```

This will:
1. Test all three algorithms on various input sizes
2. Measure execution time for each algorithm
3. Calculate error rates (false positives/negatives)
4. Generate comparison graphs in the `results/` directory

### Import Individual Algorithms

You can also use the algorithms in your own code:

```python
from algorithms.trial_division import is_prime as trial_division
from algorithms.fermat import is_prime as fermat_test
from algorithms.miller_rabin import is_prime as miller_rabin

# Trial Division (deterministic)
is_prime, exec_time = trial_division(17)

# Fermat Test (probabilistic, k rounds)
is_prime, exec_time = fermat_test(17, k=10)

# Miller-Rabin Test (probabilistic, k rounds)
is_prime, exec_time = miller_rabin(17, k=10)
```

## Generated Graphs

The benchmark script generates the following visualizations:

1. **Time Complexity Comparison** (Line Plot)
   - X-axis: Input number size (bit length)
   - Y-axis: Execution time (seconds, log scale)
   - Shows how each algorithm scales with input size

2. **Gradient Analysis** (log-log Plot)
   - **Left plot**: log(time) vs log(bit_length) - Shows polynomial degree
     - Fermat gradient: ~1.3 (polynomial growth)
     - Miller-Rabin gradient: ~1.3 (polynomial growth)
     - **Interpretation**: For O(n^k), the gradient equals k
   - **Right plot**: log(time) vs bit_length - Shows exponential growth
     - Trial Division gradient: ~0.39 ≈ ln(2)/2 (exponential: O(2^(n/2)))
   - **Key insight**: Polynomial algorithms show constant gradient on log-log plot (~1-2), while exponential shows linear growth in semi-log plot

3. **Error Rate Comparison** (Bar Chart)
   - Compares false positive and false negative rates
   - Probabilistic algorithms tested with different k values

## Mathematical Analysis: Why Gradient ≈ 1-2 (not 2-3)?

The measured gradients (~1.3) from the log-log plot are correct and expected:

**Theory**:
- For an n-bit number, the value N ≈ 2^n
- Modular exponentiation complexity: O(log³N) = O(n³) in terms of bit operations
- However, measured execution time includes:
  - Python overhead (constant factors)
  - Hardware optimizations
  - Small input sizes (not asymptotic regime)
  
**What the gradient tells us**:
- Gradient ~1-2: **Polynomial growth** (time ∝ n^1-2)
- Trial Division: Gradient ~0.39 in semi-log plot confirms **exponential growth** (2^(n/2))
- The key distinction is polynomial vs exponential, not the exact degree

**Practical Impact**:
- At 48-bit: Trial Division is **38,000× slower** than Miller-Rabin
- This gap grows exponentially for larger inputs!

## Algorithm Complexity

| Algorithm       | Time Complexity | Space | Deterministic |
|----------------|-----------------|-------|---------------|
| Trial Division | O(√n)           | O(1)  | Yes           |
| Fermat         | O(k log³n)      | O(1)  | No            |
| Miller-Rabin   | O(k log³n)      | O(1)  | No            |

## Key Findings

- **Trial Division**: Most accurate (100%) but slowest for large numbers
- **Fermat**: Fast but vulnerable to Carmichael numbers
- **Miller-Rabin**: Best balance of speed and accuracy for large numbers

## References

- Fermat's Little Theorem
- Miller-Rabin Primality Test (1980)
- Probabilistic Algorithms Theory
