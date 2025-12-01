#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <cstring>
#include <functional>
#include <sys/resource.h>
#include <unistd.h>

using namespace std;
using namespace std::chrono;

// Global counters for instrumentation
struct Metrics {
    long long comparisons = 0;
    long long swaps = 0;
    double time_ms = 0.0;
    int max_depth = 0;        // Maximum recursion depth
    int current_depth = 0;    // Current recursion depth
    
    void reset() {
        comparisons = 0;
        swaps = 0;
        time_ms = 0.0;
        max_depth = 0;
        current_depth = 0;
    }
};

// Random number generators (Mersenne Twister MT19937)
mt19937 rng(42);       // For pivot selection (reproducible across datasets)
mt19937 dataRng(12345); // For data generation only

// =============================================================================
// WRAPPER TYPE FOR std::sort INSTRUMENTATION
// =============================================================================
struct IntWrap {
    int x;
    Metrics* m;  // Pointer to metrics for counting
    
    IntWrap() : x(0), m(nullptr) {}
    IntWrap(int val, Metrics* metrics) : x(val), m(metrics) {}
};

// Comparison operator for IntWrap (counts comparisons)
bool operator<(const IntWrap& a, const IntWrap& b) {
    if (a.m) a.m->comparisons++;
    return a.x < b.x;
}

// Swap function for IntWrap (ADL finds this, counts swaps)
void swap(IntWrap& a, IntWrap& b) noexcept {
    if (a.m) a.m->swaps++;
    std::swap(a.x, b.x);
}

// Utility functions
void swap_counted(vector<int>& arr, int i, int j, Metrics& m) {
    m.swaps++;  // Count every swap call, even if i == j
    if (i != j) {
        swap(arr[i], arr[j]);
    }
}

bool compare_counted(int a, int b, Metrics& m) {
    m.comparisons++;
    return a < b;
}

bool compare_eq_counted(int a, int b, Metrics& m) {
    m.comparisons++;
    return a == b;
}

bool compare_le_counted(int a, int b, Metrics& m) {
    m.comparisons++;
    return a <= b;
}

// =============================================================================
// PIVOT SELECTION STRATEGIES
// =============================================================================

// 1. Naive - select first element
int findPivot_Naive(vector<int>& arr, int l, int r, Metrics& m) {
    return l;
}

// 2. Median of Three - median of first, middle, last
int findPivot_MedianOfThree(vector<int>& arr, int l, int r, Metrics& m) {
    int mid = l + (r - l) / 2;
    int a = arr[l], b = arr[mid], c = arr[r];
    
    // Cache comparison results to avoid redundant calls and logical contradictions
    bool ab = compare_counted(a, b, m);  // a < b
    bool bc = compare_counted(b, c, m);  // b < c
    bool ac = compare_counted(a, c, m);  // a < c
    
    // Determine median: the element that is neither min nor max
    // Using cached comparisons:
    // If a < b and b < c, then b is median (a < b < c)
    // If c < b and b < a, then b is median (c < b < a)
    if ((ab && bc) || (!ab && !bc && !ac)) {
        return mid;
    }
    // If a < c and c < b, then c is median (a < c < b)
    // If b < c and c < a, then c is median (b < c < a)
    else if ((ac && !bc) || (!ac && bc)) {
        return r;
    }
    // Otherwise a is median
    return l;
}

// 3. Randomized - pick random element
int findPivot_Randomized(vector<int>& arr, int l, int r, Metrics& m) {
    uniform_int_distribution<int> dist(l, r);
    return dist(rng);
}

// 4. Randomized Median of Three
int findPivot_RandomizedMedianOfThree(vector<int>& arr, int l, int r, Metrics& m) {
    uniform_int_distribution<int> dist(l, r);
    int i1 = dist(rng);
    int i2 = dist(rng);
    int i3 = dist(rng);
    
    int a = arr[i1], b = arr[i2], c = arr[i3];
    
    // Cache comparison results to avoid redundant calls and logical contradictions
    bool ab = compare_counted(a, b, m);  // a < b
    bool bc = compare_counted(b, c, m);  // b < c
    bool ac = compare_counted(a, c, m);  // a < c
    
    // Determine median using cached comparisons
    if ((ab && bc) || (!ab && !bc && !ac)) {
        return i2;
    }
    else if ((ac && !bc) || (!ac && bc)) {
        return i3;
    }
    return i1;
}

// Helper for MoM - sort small arrays (<=5 elements) in-place
void sort5_MoM(vector<int>& arr, int l, int r, Metrics& m) {
    // Simple insertion sort for tiny arrays
    for (int i = l + 1; i <= r; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= l && compare_counted(key, arr[j], m)) {
            arr[j + 1] = arr[j];
            m.swaps++;  // Count data movement
            j--;
        }
        arr[j + 1] = key;
    }
}

// MoM select - find k-th smallest element (returns INDEX)
// CRITICAL: Does NOT partition the full range - only finds median position
// QuickSort will do the actual partitioning
int momSelect(vector<int>& arr, int l, int r, int k, Metrics& m) {
    int n = r - l + 1;
    
    // Base case: sort small arrays and return k-th position
    if (n <= 5) {
        sort5_MoM(arr, l, r, m);
        return l + k;
    }
    
    // Divide into groups of 5 and find median of each group
    int numGroups = (n + 4) / 5;
    
    for (int i = 0; i < numGroups; i++) {
        int subL = l + i * 5;
        int subR = min(subL + 4, r);
        
        // Sort this group of 5
        sort5_MoM(arr, subL, subR, m);
        
        // Move median to front of array
        int medianIdx = subL + (subR - subL) / 2;
        swap_counted(arr, l + i, medianIdx, m);
    }
    
    // Recursively find median of medians (NO partitioning of full range)
    int mom_k = (numGroups - 1) / 2;
    int momIndex = momSelect(arr, l, l + numGroups - 1, mom_k, m);
    
    // Return the index directly - no partitioning here!
    return momIndex;
}

// 5. Median of Medians
// NOTE: momSelect rearranges elements to find median, then QuickSort partitions normally.
// This is the standard approach - MoM provides good pivot, QuickSort does its own partition.
int findPivot_MoM(vector<int>& arr, int l, int r, Metrics& m) {
    int n = r - l + 1;
    int k = (n - 1) / 2;  // Find median (0-indexed)
    return momSelect(arr, l, r, k, m);  // Returns index directly
}

// =============================================================================
// PARTITION FUNCTIONS
// =============================================================================

// Standard two-way partition
// Uses consistent comparison semantics: always compare arr[i] < pivot (never reversed)
int partition_TwoWay(vector<int>& arr, int l, int r, Metrics& m) {
    int pivot = arr[l];
    int startPtr = l + 1;
    int endPtr = r;
    
    while (startPtr <= endPtr) {
        // Move startPtr forward while arr[startPtr] <= pivot
        while (startPtr <= endPtr && compare_le_counted(arr[startPtr], pivot, m)) {
            startPtr++;
        }
        // Move endPtr backward while arr[endPtr] > pivot
        while (startPtr <= endPtr && compare_counted(pivot, arr[endPtr], m)) {
            endPtr--;
        }
        // Swap if pointers haven't crossed
        if (startPtr < endPtr) {
            swap_counted(arr, startPtr, endPtr, m);
            startPtr++;
            endPtr--;
        }
    }
    
    swap_counted(arr, l, endPtr, m);
    return endPtr;
}

// Three-way partition (for duplicate handling)
void partition_ThreeWay(vector<int>& arr, int l, int r, int& lt, int& gt, Metrics& m) {
    int pivot = arr[l];
    lt = l;
    gt = r;
    int i = l + 1;
    
    while (i <= gt) {
        if (compare_counted(arr[i], pivot, m)) {
            swap_counted(arr, lt, i, m);
            lt++;
            i++;
        } else if (compare_counted(pivot, arr[i], m)) {
            swap_counted(arr, i, gt, m);
            gt--;
        } else {
            i++;
        }
    }
}

// =============================================================================
// QUICKSORT IMPLEMENTATIONS
// =============================================================================

template<typename PivotFunc>
void quicksort_TwoWay(vector<int>& arr, int l, int r, Metrics& m, PivotFunc findPivot) {
    if (l >= r) return;
    
    m.current_depth++;
    if (m.current_depth > m.max_depth) {
        m.max_depth = m.current_depth;
    }
    
    // Find pivot and move to first position
    int pivotIdx = findPivot(arr, l, r, m);
    swap_counted(arr, l, pivotIdx, m);
    
    // Partition
    int mid = partition_TwoWay(arr, l, r, m);
    
    // Recurse
    quicksort_TwoWay(arr, l, mid - 1, m, findPivot);
    quicksort_TwoWay(arr, mid + 1, r, m, findPivot);
    
    m.current_depth--;
}

void quicksort_ThreeWay(vector<int>& arr, int l, int r, Metrics& m) {
    if (l >= r) return;
    
    m.current_depth++;
    if (m.current_depth > m.max_depth) {
        m.max_depth = m.current_depth;
    }
    
    int lt, gt;
    partition_ThreeWay(arr, l, r, lt, gt, m);
    
    quicksort_ThreeWay(arr, l, lt - 1, m);
    quicksort_ThreeWay(arr, gt + 1, r, m);
    
    m.current_depth--;
}

// =============================================================================
// MERGE SORT
// =============================================================================

void merge(vector<int>& arr, int l, int mid, int r, Metrics& m) {
    int n1 = mid - l + 1;
    int n2 = r - mid;
    
    vector<int> L(n1), R(n2);
    
    for (int i = 0; i < n1; i++) {
        L[i] = arr[l + i];
    }
    for (int j = 0; j < n2; j++) {
        R[j] = arr[mid + 1 + j];
    }
    
    int i = 0, j = 0, k = l;
    
    while (i < n1 && j < n2) {
        if (compare_le_counted(L[i], R[j], m)) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        m.swaps++;  // Each assignment is a swap
        k++;
    }
    
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
        m.swaps++;
    }
    
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
        m.swaps++;
    }
}

void mergeSortHelper(vector<int>& arr, int l, int r, Metrics& m) {
    if (l < r) {
        m.current_depth++;
        if (m.current_depth > m.max_depth) {
            m.max_depth = m.current_depth;
        }
        
        int mid = l + (r - l) / 2;
        mergeSortHelper(arr, l, mid, m);
        mergeSortHelper(arr, mid + 1, r, m);
        merge(arr, l, mid, r, m);
        
        m.current_depth--;
    }
}

void mergeSort(vector<int>& arr, Metrics& m) {
    if (arr.size() > 1) {
        mergeSortHelper(arr, 0, arr.size() - 1, m);
    }
}

// =============================================================================
// HEAP SORT
// =============================================================================

void heapify(vector<int>& arr, int n, int i, Metrics& m) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    
    if (left < n && compare_counted(arr[largest], arr[left], m)) {
        largest = left;
    }
    
    if (right < n && compare_counted(arr[largest], arr[right], m)) {
        largest = right;
    }
    
    if (largest != i) {
        swap_counted(arr, i, largest, m);
        heapify(arr, n, largest, m);
    }
}

void heapSort(vector<int>& arr, Metrics& m) {
    int n = arr.size();
    
    // Build max heap
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i, m);
    }
    
    // Extract elements from heap one by one
    for (int i = n - 1; i > 0; i--) {
        swap_counted(arr, 0, i, m);
        heapify(arr, i, 0, m);
    }
}

// =============================================================================
// DATASET GENERATION
// =============================================================================

// Random dataset using MT19937
vector<int> generateRandom(int n) {
    vector<int> arr(n);
    uniform_int_distribution<int> dist(1, 1000000);
    for (int i = 0; i < n; i++) {
        arr[i] = dist(dataRng);
    }
    return arr;
}

// Almost sorted dataset (1% noise - worst case for naive first-pivot)
vector<int> generateAlmostSorted(int n) {
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        arr[i] = i;  // 0-indexed like reference
    }
    
    // Perform max(1, n/100) random swaps (1% noise)
    int noise = max(1, n / 100);
    uniform_int_distribution<int> dist(0, n - 1);
    for (int i = 0; i < noise; i++) {
        int idx1 = dist(dataRng);
        int idx2 = dist(dataRng);
        swap(arr[idx1], arr[idx2]);
    }
    
    return arr;
}

// Low entropy dataset (many duplicates) - only d distinct values
vector<int> generateLowEntropy(int n, int d = 10) {
    vector<int> arr(n);
    uniform_int_distribution<int> dist(1, d);
    for (int i = 0; i < n; i++) {
        arr[i] = dist(dataRng);
    }
    return arr;
}

// Sorted dataset (worst case for naive)
vector<int> generateSorted(int n) {
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        arr[i] = i + 1;
    }
    return arr;
}

// =============================================================================
// MEMORY USAGE
// =============================================================================
// BENCHMARK RUNNER
// =============================================================================

void runBenchmark(const string& algoName, vector<int> arr, Metrics& m, 
                  function<void(vector<int>&, Metrics&)> sortFunc) {
    auto start = high_resolution_clock::now();
    sortFunc(arr, m);
    auto end = high_resolution_clock::now();
    
    m.time_ms = duration_cast<microseconds>(end - start).count() / 1000.0;
}

// =============================================================================
// MAIN
// =============================================================================

int main() {
    ofstream csv("../csv/sorting_benchmark.csv");
    csv << "Algorithm,Dataset,Size,Run,Time_ms,Comparisons,Swaps,MaxDepth\n";
    
    // Test sizes - up to 10^5
    vector<int> sizes;
    // Fine-grained for small sizes
    for (int i = 100; i <= 1000; i += 100) sizes.push_back(i);
    for (int i = 2000; i <= 10000; i += 1000) sizes.push_back(i);
    for (int i = 20000; i <= 100000; i += 10000) sizes.push_back(i);
    
    int numRuns = 50; // Multiple runs for variance analysis
    
    vector<string> datasetTypes = {"Random", "AlmostSorted", "LowEntropy"};
    
    for (const string& datasetType : datasetTypes) {
        rng.seed(42);      // Reset pivot RNG for fair comparison across datasets
        dataRng.seed(12345); // Reset data RNG for reproducible data generation
        cout << "Processing " << datasetType << " dataset...\n";
        
        for (int size : sizes) {
            cout << "  Size: " << size << "\n";
            
            // Generate base dataset
            vector<int> baseDataset;
            if (datasetType == "Random") {
                baseDataset = generateRandom(size);
            } else if (datasetType == "AlmostSorted") {
                baseDataset = generateAlmostSorted(size);
            } else {
                baseDataset = generateLowEntropy(size, 10);
            }
            
            // Run each algorithm multiple times
            for (int run = 0; run < numRuns; run++) {
                
                // 1. Naive QuickSort
                {
                    Metrics m;
                    vector<int> arr = baseDataset;
                    runBenchmark("Naive", arr, m, [](vector<int>& a, Metrics& met) {
                        quicksort_TwoWay(a, 0, a.size() - 1, met, findPivot_Naive);
                    });
                    csv << "Naive," << datasetType << "," << size << "," << run << ","
                        << m.time_ms << "," << m.comparisons << "," << m.swaps << ","
                        << m.max_depth << "\n";
                }
                
                // 2. Median of Three - skip on LowEntropy
                if (datasetType != "LowEntropy") {
                    Metrics m;
                    vector<int> arr = baseDataset;
                    runBenchmark("MedianOfThree", arr, m, [](vector<int>& a, Metrics& met) {
                        quicksort_TwoWay(a, 0, a.size() - 1, met, findPivot_MedianOfThree);
                    });
                    csv << "MedianOfThree," << datasetType << "," << size << "," << run << ","
                        << m.time_ms << "," << m.comparisons << "," << m.swaps << ","
                        << m.max_depth << "\n";
                }
                
                // 3. Randomized
                {
                    Metrics m;
                    vector<int> arr = baseDataset;
                    runBenchmark("Randomized", arr, m, [](vector<int>& a, Metrics& met) {
                        quicksort_TwoWay(a, 0, a.size() - 1, met, findPivot_Randomized);
                    });
                    csv << "Randomized," << datasetType << "," << size << "," << run << ","
                        << m.time_ms << "," << m.comparisons << "," << m.swaps << ","
                        << m.max_depth << "\n";
                }
                
                // 4. Randomized Median of Three - skip on LowEntropy
                if (datasetType != "LowEntropy") {
                    Metrics m;
                    vector<int> arr = baseDataset;
                    runBenchmark("RandomizedMedianOfThree", arr, m, [](vector<int>& a, Metrics& met) {
                        quicksort_TwoWay(a, 0, a.size() - 1, met, findPivot_RandomizedMedianOfThree);
                    });
                    csv << "RandomizedMedianOfThree," << datasetType << "," << size << "," << run << ","
                        << m.time_ms << "," << m.comparisons << "," << m.swaps << ","
                        << m.max_depth << "\n";
                }
                
                // 5. Three-Way Partitioning
                {
                    Metrics m;
                    vector<int> arr = baseDataset;
                    runBenchmark("ThreeWay", arr, m, [](vector<int>& a, Metrics& met) {
                        quicksort_ThreeWay(a, 0, a.size() - 1, met);
                    });
                    csv << "ThreeWay," << datasetType << "," << size << "," << run << ","
                        << m.time_ms << "," << m.comparisons << "," << m.swaps << "," 
                        << m.max_depth << "\n";
                }
                
                // 6. std::sort (for comparison) - skip for LowEntropy only
                if (datasetType != "LowEntropy") {
                    Metrics m;
                    // Convert to IntWrap for instrumentation
                    vector<IntWrap> arr;
                    arr.reserve(baseDataset.size());
                    for (int val : baseDataset) {
                        arr.push_back(IntWrap(val, &m));
                    }
                    
                    auto start = high_resolution_clock::now();
                    sort(arr.begin(), arr.end());
                    auto end = high_resolution_clock::now();
                    m.time_ms = duration_cast<microseconds>(end - start).count() / 1000.0;
                    
                    csv << "std::sort," << datasetType << "," << size << "," << run << ","
                        << m.time_ms << "," << m.comparisons << "," << m.swaps << "," 
                        << m.max_depth << "\n";
                }
                
                // 6. MoM (Median of Medians) - skip LowEntropy only
                if (datasetType != "LowEntropy") {
                    Metrics m;
                    vector<int> arr = baseDataset;
                    runBenchmark("MoM", arr, m, [](vector<int>& a, Metrics& met) {
                        quicksort_TwoWay(a, 0, a.size() - 1, met, findPivot_MoM);
                    });
                    csv << "MoM," << datasetType << "," << size << "," << run << ","
                        << m.time_ms << "," << m.comparisons << "," << m.swaps << "," 
                        << m.max_depth << "\n";
                }
                
                // 7. MergeSort (skip LowEntropy)
                if (datasetType != "LowEntropy") {
                    Metrics m;
                    vector<int> arr = baseDataset;
                    runBenchmark("MergeSort", arr, m, [](vector<int>& a, Metrics& met) {
                        mergeSort(a, met);
                    });
                    csv << "MergeSort," << datasetType << "," << size << "," << run << ","
                        << m.time_ms << "," << m.comparisons << "," << m.swaps << "," 
                        << m.max_depth << "\n";
                }
                
                // 8. HeapSort (skip LowEntropy)
                if (datasetType != "LowEntropy") {
                    Metrics m;
                    vector<int> arr = baseDataset;
                    runBenchmark("HeapSort", arr, m, [](vector<int>& a, Metrics& met) {
                        heapSort(a, met);
                    });
                    csv << "HeapSort," << datasetType << "," << size << "," << run << ","
                        << m.time_ms << "," << m.comparisons << "," << m.swaps << "," 
                        << m.max_depth << "\n";
                }
            }
            
            csv.flush();
        }
    }
    
    csv.close();
    cout << "Benchmark complete! Results saved to sorting_benchmark.csv\n";
    
    return 0;
}
