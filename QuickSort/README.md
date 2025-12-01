# QuickSort Benchmark - Running Instructions

## Quick Start (Automated)
NOTE: MAINTAIN THE DIRECTORY STRUCTURE
**Step 1: Install Python Dependencies**
```bash
pip3 install -r requirements.txt
```

**Step 2: Run the Benchmark**
```bash
./run_all.sh
```
**Output:** Benchmark data in `csv/`, plots in `img/`

---

## Manual Execution Steps

### Step 1: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

**Required Python Packages:**
- **`pandas`** - Data processing and CSV reading
- **`matplotlib`** - Plotting library
- **`seaborn`** - Statistical visualization
- **`numpy`** - Numerical operations

---

### Step 2: Compile the Benchmark

```bash
cd src
g++ -std=c++17 -O2 -o sort_bench main.cpp
```

**Required:**
- `src/main.cpp`

**Output:**
- `src/sort_bench` (executable)

---

### Step 3: Run the Benchmark

```bash
cd src
./sort_bench
```

**Required:**
- `src/sort_bench` (from Step 2)

**Output:**
- `csv/sorting_benchmark.csv` (29,400 records)

**Runtime:** ~30-45 minutes

---

### Step 4: Generate Plots

```bash
cd src
python3 plot_graphs.py
```

**Required:**
- `src/plot_graphs.py`
- `csv/sorting_benchmark.csv` (from Step 3)

**Output (11 files in `img/` directory):**
1. `1_all_algorithms_random.png`
2. `2_all_algorithms_almost_sorted.png`
3. `3_low_entropy_comparison.png`
4. `4_randomized_variance_scatter.png`
5. `5_comparisons_vs_theoretical.png`
6. `6_recursion_depth.png`
7. `7_time_complexity_scaling_linear.png`
8. `8_quicksort_variants_comparison.png`
9. `9_swaps_loglog_analysis.png`
10. `10_summary_table.png`
11. `summary_statistics.csv`

---

## Required Files

### Essential Files:
- `requirements.txt` - Python dependencies
- `src/main.cpp` - Benchmark implementation
- `src/plot_graphs.py` - Plotting script
- `run_all.sh` - Automated execution script

### Generated Files:
- `src/sort_bench` - Compiled binary (Step 2)
- `csv/sorting_benchmark.csv` - Benchmark results (Step 3)
- `img/*.png` and `img/summary_statistics.csv` - Plots (Step 4)

---

## Troubleshooting

**Compilation fails:**
- Check g++ version: `g++ --version` (need 7.0+)
- Verify `main.cpp` exists in `src/`

**Python import errors:**
- Install dependencies: `pip3 install -r requirements.txt`
- Check Python version: `python3 --version` (need 3.6+)

**Benchmark not running:**
- Ensure `sort_bench` is executable: `chmod +x src/sort_bench`
- Run from `src/` directory

**Missing CSV file for plotting:**
- Run Step 3 (benchmark) before Step 4 (plotting)
- Check that `csv/sorting_benchmark.csv` was created

---

## System Requirements

- **OS:** Linux (tested), macOS, or Windows with WSL
- **Compiler:** g++ 7.0+ with C++17 support
- **Python:** 3.6 or higher
- **RAM:** 4GB+ recommended
- **Disk Space:** ~500MB for outputs
