#!/bin/bash
# Run benchmark only (assumes already compiled)

echo "========================================"
echo "Running QuickSort Benchmark"
echo "========================================"
echo ""

if [ ! -f "sort_bench" ]; then
    echo "ERROR: sort_bench not found!"
    echo "Run ./compile.sh first"
    exit 1
fi

# Create CSV directory
mkdir -p ../csv

# Remove old CSV
rm -f ../csv/sorting_benchmark.csv

echo "Starting benchmark..."
echo "This will take approximately 30-60 minutes."
echo "Started at: $(date)"
echo ""

./sort_bench

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Benchmark complete at: $(date)"
    
    if [ -f "../csv/sorting_benchmark.csv" ]; then
        RECORDS=$(wc -l < ../csv/sorting_benchmark.csv)
        echo "Generated $RECORDS records"
    fi
else
    echo "✗ Benchmark failed!"
    exit 1
fi
