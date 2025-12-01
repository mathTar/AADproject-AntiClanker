#!/bin/bash
# Generate plots only (assumes CSV exists)

echo "========================================"
echo "Generating Plots"
echo "========================================"
echo ""

if [ ! -f "../csv/sorting_benchmark.csv" ]; then
    echo "ERROR: sorting_benchmark.csv not found!"
    echo "Run benchmark first with ./run_only.sh"
    exit 1
fi

# Create img directory
mkdir -p ../img

echo "Generating plots from benchmark data..."

python3 plot_graphs.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Plots generated successfully!"
    echo ""
    echo "Output files:"
    ls -lh ../img/*.png 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
    echo ""
    if [ -f "../img/summary_statistics.csv" ]; then
        echo "  ../img/summary_statistics.csv"
    fi
else
    echo "✗ Plot generation failed!"
    exit 1
fi
