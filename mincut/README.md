# Min-Cut Algorithms: Karger and Stoer–Wagner

This repository contains C++ implementations (with Python wrappers) of Karger’s randomized min-cut and the Stoer–Wagner exact min-cut, plus analysis and empirical experiments.

## Directory Structure
- `algorithms/` – Python wrappers and C++ sources for the core algorithms
  - `karger/` – `kargercppver.cpp` and wrapper `karger_cpp.py`
  - `stoer_wagner/` – `stoer_wagner.cpp` and wrapper `stoer_wagner_cpp.py`
- `analysis/` –  analyses that generate datasets, run algorithms, and save plots/results
  - `run_analysis.py` – main analysis entry
- `data/` – Dataset generation utilities (`generate_dataset.py`)
- `graphs/` – Input datasets (created/used by analyses)
- `results/` – Analysis outputs (text summaries and PNG charts)
- `karger_empirical_analysis/` – Standalone empirical timing/memory study for Karger
- `stoer_wagner_empirical_analysis/` – Standalone empirical timing/memory study for Stoer–Wagner
- `kargeroptattempt/` – Side-by-side Karger variants comparison (standard vs optimized)

## Prerequisites (Windows)
- C++ compiler (e.g., MinGW-w64 `g++` in PATH)
- Python 3.9+ with packages: `matplotlib`, `numpy`, `psutil`

Install Python packages:
```powershell
python -m pip install matplotlib numpy psutil
```

## Build Core C++ Binaries (for Python wrappers)
The Python wrappers in `algorithms/*` expect the compiled executables to live beside the C++ sources with these names:
- `algorithms/karger/kargercppver.exe`
- `algorithms/stoer_wagner/stoer_wagner.exe`

Build them once:
```powershell
# Karger
cd algorithms/karger
g++ -O3 -o kargercppver.exe kargercppver.cpp

# Stoer–Wagner
cd ../stoer_wagner
g++ -O3 -o stoer_wagner.exe stoer_wagner.cpp
```


## Running the Main Analysis
`analysis/run_analysis.py` manages dataset generation and runs the algorithms using the C++ binaries via Python wrappers.

Recommended: run from the project root (but it also works from anywhere thanks to internal path handling).
```powershell
# From repo root
python .\analysis\run_analysis.py
```

### Where files are read/written
- Reads datasets from `graphs/` (expects `random_graphs.txt`, `sparse_graphs.txt`, `dense_graphs.txt` unless regeneration is enabled)
- Writes results and plots to `results/`

### Key flags inside `analysis/run_analysis.py`
Edit these at the top of the file to control behavior:
- `TRIALS` (int): Karger trials per graph (default 100)
- `NUM_GRAPHS` (int): Count per type when regenerating datasets
- `REGENERATE_GRAPHS` (bool):
  - `False` (default): Use existing files in `graphs/`
  - `True`: Regenerate the dataset files in `graphs/` before analysis
- `RUN_BASIC_ANALYSIS` (bool):
  - When `True`: runs Karger vs Stoer–Wagner on `random`, `sparse`, `dense`
  - Outputs: `{type}_analysis.txt`, `{type}_comparison.png`, plus `overall_comparison.png` in `results/`
- `RUN_TRIALS_IMPACT_ANALYSIS` (bool):
  - When `True`: sweeps trial counts; outputs `trials_analysis.txt` and `trials_impact_analysis.png` in `results/`
- `RUN_SIZE_IMPACT_ANALYSIS` (bool):
  - When `True`: runs on multiple graph sizes; outputs `size_analysis.txt` and `size_impact_comparison.png` in `results/`
- `RUN_KARGER_100_VS_THEORY` (bool):
  - When `True`: compares 100 trials vs theoretical $n^2\log n$; outputs `karger_100_vs_theory.txt/.png` in `results/`

Quick start examples (toggle one analysis at a time for clarity):
```powershell
# 1) Basic analysis with dataset regeneration
# Edit run_analysis.py: set REGENERATE_GRAPHS=True; RUN_BASIC_ANALYSIS=True
python .\analysis\run_analysis.py

# 2) Trials impact
# Edit run_analysis.py: RUN_TRIALS_IMPACT_ANALYSIS=True
python .\analysis\run_analysis.py

# 3) Size impact
# Edit run_analysis.py: RUN_SIZE_IMPACT_ANALYSIS=True
python .\analysis\run_analysis.py

# 4) 100 trials vs n^2 log n
# Edit run_analysis.py: RUN_KARGER_100_VS_THEORY=True
python .\analysis\run_analysis.py
```

## Empirical Studies (run from their folders)
These scripts are self-contained and compile their own local executables before running. 
**Always change directory into the folder first.**

### Karger empirical
Outputs time/memory plots and CSV under `karger_empirical_analysis/empiricaltestinggraph/`.
```powershell
cd karger_empirical_analysis
python .\karger_empirical_analysis.py
```
Notes:
- Requires `g++` and links `-lpsapi` (Windows) automatically.
- Produces: `kargerdataset.txt`, `karger_time.png`, `Karger_memory.png`.

### Stoer–Wagner empirical
Outputs under `stoer_wagner_empirical_analysis/empiricaltestinggraph/`.
```powershell
cd stoer_wagner_empirical_analysis
python .\stoer_wagner_empricial_analysis.py
```
Produces: `stoerwagnerdataset.txt`, `stoer_wagner_time.png`, `stoer_wagner_memory.png`.

## Karger Variant Comparison (optimized vs standard)
Run from within the folder; it compiles needed binaries and saves a summary.
```powershell
cd kargeroptattempt
python .\compare_karger.py
```
Outputs:
- `kargeroptattempt/results/karger_error_analysis.txt`
- Console summary with accuracy and timing comparisons.

