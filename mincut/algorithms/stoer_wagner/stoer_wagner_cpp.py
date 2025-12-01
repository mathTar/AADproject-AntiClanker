import subprocess
from pathlib import Path

def stoer_wagner(G):
    """
    Wrapper that calls the C++ Stoer-Wagner implementation.
    
    Has the EXACT SAME INTERFACE as stoer_wagner.py so you can swap it in.
    
    Args:
        G: Adjacency matrix (list of lists)
    
    Returns:
        Minimum cut value
    """
    V = len(G)
    
    # Extract edges from adjacency matrix
    edges = []
    for i in range(V):
        for j in range(i + 1, V):
            if G[i][j] > 0:
                edges.append((i, j, G[i][j]))
    
    E = len(edges)
    
    # Find the C++ binary in this module's directory
    module_dir = Path(__file__).resolve().parent
    binary = None
    for name in ("stoer_wagner.exe", "stoer_wagner"):
        candidate = module_dir / name
        if candidate.exists():
            binary = str(candidate)
            break
    
    if binary is None:
        raise FileNotFoundError(
            "Compiled C++ binary not found!\n"
            "First compile with:\n"
            "  g++ -O3 -o stoer_wagner stoer_wagner.cpp"
        )
    
    # Prepare input for C++ program
    input_data = f"{V} {E}\n"
    for src, dst, weight in edges:
        input_data += f"{src} {dst} {weight}\n"
    
    try:
        # Call C++ binary
        result = subprocess.run(
            [binary],
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
        raise TimeoutError("C++ Stoer-Wagner timed out")
    except ValueError:
        raise ValueError(f"Could not parse C++ output: {result.stdout}")
