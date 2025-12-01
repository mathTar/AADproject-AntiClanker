#!/bin/bash
# Comprehensive QuickSort Benchmark Runner
# Compiles, runs benchmark, and generates plots

set -e  # Exit on error

echo "QuickSort Analysis - Complete Pipeline"
echo "======================================="
echo ""

# Navigate to project root
cd "$(dirname "$0")"

# Step 1: Compile
echo "[1/3] Compiling benchmark..."
cd src
g++ -std=c++17 -O2 -o sort_bench main.cpp
echo "✓ Compilation successful"
echo ""

# Step 2: Run benchmark
echo "[2/3] Running benchmark (this may take a few minutes)..."
./sort_bench
echo "✓ Benchmark complete"
echo ""

# Step 3: Generate plots
echo "[3/3] Generating plots..."
python3 plot_graphs.py
echo "✓ Plots generated"
echo ""

echo "======================================="
echo "COMPLETE! Results available in:"
echo "  - CSV: csv/sorting_benchmark.csv"
echo "  - Plots: img/*.png"
echo "  - Stats: img/summary_statistics.csv"
echo "======================================="
