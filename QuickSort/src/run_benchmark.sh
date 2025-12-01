#!/bin/bash

echo "========================================"
echo "QuickSort Analysis - Full Benchmark Run"
echo "========================================"
echo ""

# Check if compiled
if [ ! -f "sort_bench" ]; then
    echo "Compiling C++ benchmark..."
    g++ -std=c++17 -O2 -o sort_bench main.cpp
    if [ $? -ne 0 ]; then
        echo "ERROR: Compilation failed!"
        exit 1
    fi
    echo "Compilation successful!"
    echo ""
fi

# Check Python dependencies
echo "Checking Python dependencies..."
python3 -c "import pandas, matplotlib, seaborn, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: Missing Python dependencies!"
    echo "Install with: pip3 install pandas matplotlib seaborn numpy"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create directories
mkdir -p ../csv
mkdir -p ../img

# Run benchmark
echo ""
echo "Running benchmark..."
echo "This may take 30-60 minutes depending on your hardware."
echo "Progress will be shown as it runs."
echo ""
echo "Started at: $(date)"
echo ""

./sort_bench

if [ $? -ne 0 ]; then
    echo "ERROR: Benchmark failed!"
    exit 1
fi

echo ""
echo "Benchmark completed at: $(date)"
echo ""

# Check if CSV was generated
if [ ! -f "../csv/sorting_benchmark.csv" ]; then
    echo "ERROR: Benchmark CSV not found!"
    exit 1
fi

# Count records
RECORDS=$(wc -l < ../csv/sorting_benchmark.csv)
echo "Generated $RECORDS benchmark records"
echo ""

# Generate plots
echo "Generating plots..."
python3 plot_graphs.py

if [ $? -ne 0 ]; then
    echo "ERROR: Plot generation failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "BENCHMARK COMPLETE!"
echo "========================================"
echo ""
echo "Results:"
echo "  - Benchmark data: ../csv/sorting_benchmark.csv"
echo "  - Plots: ../img/"
echo "  - Summary: ../img/summary_statistics.csv"
echo ""
echo "Generated plots:"
ls -lh ../img/*.png 2>/dev/null | awk '{print "  - " $9 " (" $5 ")"}'
echo ""
echo "View plots with your image viewer or open in a browser."
echo ""
