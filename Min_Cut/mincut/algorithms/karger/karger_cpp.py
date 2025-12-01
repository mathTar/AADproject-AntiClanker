import subprocess
from pathlib import Path

def karger_min_cut(G, trials=100):
    """
    Wrapper that calls the C++ Karger implementation.
    
    Has the EXACT SAME INTERFACE as krager.py so you can swap it in.
    
    Args:
        G: Adjacency matrix (list of lists)
        trials: Number of trials (default 100)
    
    Returns:
        Minimum cut value
    """
    V = len(G)
    
    # Extract edges from adjacency matrix
    edges = []
    for i in range(V):
        for j in range(i + 1, V):
            if G[i][j] == 1:
                edges.append((i, j))
    
    E = len(edges)
    
    # Find the C++ executable in this module's directory
    module_dir = Path(__file__).resolve().parent
    executable = None
    for name in ("kargercppver.exe", "kargercppver"):
        candidate = module_dir / name
        if candidate.exists():
            executable = str(candidate)
            break
    
    if executable is None:
        raise FileNotFoundError(
            "Compiled C++ executable not found!\n"
            "First compile with:\n"
            "  g++ -O3 -o kargercppver kargercppver.cpp"
        )
    
    # Prepare input for C++ program
    input_data = f"{V} {E} {trials}\n"
    for src, dst in edges:
        input_data += f"{src} {dst}\n"
    
    try:
        # Call C++ executable
        result = subprocess.run(
            [executable],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"C++ program failed: {result.stderr}")
        
        # Parse output
        min_cut = int(result.stdout.strip())
        return min_cut
    
    except subprocess.TimeoutExpired:
        raise TimeoutError("C++ Karger timed out")
    except ValueError:
        raise ValueError(f"Could not parse C++ output: {result.stdout}")
