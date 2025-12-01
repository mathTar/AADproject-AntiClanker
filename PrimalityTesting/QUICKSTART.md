# Quick Start Guide

## 1. Install Dependencies (One-time setup)
```powershell
pip install -r requirements.txt
```

## 2. Run the Complete Benchmark
```powershell
python benchmarks\benchmark.py
```
This will:
- Test all three algorithms on various input sizes
- Measure time complexity and error rates
- Generate graphs in `results/` directory
- Takes approximately 1-2 minutes

## 3. View Results
Open the generated graphs:
- `results\time_complexity.png` - Shows execution time comparison
- `results\error_rates.png` - Shows accuracy comparison

## 4. Test Individual Algorithms
```powershell
# Test Trial Division
python algorithms\trial_division.py

# Test Fermat
python algorithms\fermat.py

# Test Miller-Rabin
python algorithms\miller_rabin.py
```

## 5. Use in Your Own Code
```python
from algorithms.miller_rabin import is_prime

# Check if 1009 is prime using 10 rounds
result, exec_time = is_prime(1009, k=10)
print(f"1009 is prime: {result}")
print(f"Execution time: {exec_time:.6f}s")
```

## Understanding the Results

### Time Complexity Graph (Line Plot)
- **X-axis**: Input size in bits (8 to 48 bits)
- **Y-axis**: Execution time in seconds (log scale)
- **Observation**: Trial Division grows exponentially, while Fermat and Miller-Rabin remain nearly constant

### Error Rate Graph (Bar Chart)
- **Left chart**: False Positive Rate (composite classified as prime)
- **Right chart**: False Negative Rate (prime classified as composite)
- **Observation**: Trial Division is 100% accurate, Miller-Rabin has 0% error with k=10, Fermat may have small false positive rate

## Graph Choice Explanation

### Why Line Plot for Time Complexity?
- Both axes are continuous variables (size and time)
- Shows trends and growth rates clearly
- Easy to compare multiple algorithms
- Log scale handles wide range of values

### Why Bar Chart for Error Rates?
- Comparing discrete categories (algorithms)
- Showing percentages/counts clearly
- Grouped comparison (FP vs FN)
- Easy to see which algorithm is most accurate

## Common Issues

### Import Errors
Make sure you run scripts from the project root directory:
```powershell
cd c:\Users\DELL\Downloads\aadCodes
python benchmarks\benchmark.py
```

### Missing Dependencies
Install all required packages:
```powershell
pip install numpy matplotlib scipy
```

## Project Structure
```
aadCodes/
├── algorithms/          # Algorithm implementations
├── benchmarks/          # Benchmarking scripts
├── results/             # Generated graphs
├── utils/               # Helper functions
├── ogFiles/             # Original files (legacy)
└── README.md           # Full documentation
```
