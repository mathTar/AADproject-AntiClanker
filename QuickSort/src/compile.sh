#!/bin/bash
# Compile the benchmark

echo "Compiling QuickSort benchmark..."
g++ -std=c++17 -O2 -o sort_bench main.cpp

if [ $? -eq 0 ]; then
    echo "✓ Compilation successful!"
    echo "Executable: sort_bench"
else
    echo "✗ Compilation failed!"
    exit 1
fi
