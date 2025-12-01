import secrets
from pathlib import Path
from typing import Optional

# Use secrets.SystemRandom() for cryptographically secure random number generation
random = secrets.SystemRandom()

# To ensure connected graphs: first create spanning tree, then add random edges
# Spanning tree guarantees connectivity. Then add edges based on density type.

def make_connected(G, num_vertices):
    """Ensure graph is connected by adding spanning tree first."""
    if num_vertices < 2:
        return G
    
    # Create spanning tree path 0-1-2-...-n with weight 1 (unweighted)
    for i in range(num_vertices - 1):
        G[i][i + 1] = 1
        G[i + 1][i] = 1

def generate_graph(num_vertices, graph_type='random'):
    """Generate connected graph: random, sparse, or dense."""
    G = [[0] * num_vertices for _ in range(num_vertices)]
    
    # First make connected with spanning tree
    make_connected(G, num_vertices)
    
    # Add edges based on type
    if graph_type == 'sparse':
        prob = 0.3  # Low probability
    elif graph_type == 'dense':
        prob = 0.7  # High probability
    elif graph_type =='complete':
        prob = 1
    else:  # random
        prob = 0.5  # Medium probability
    
    # Add random edges
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if G[i][j] == 0 and random.random() < prob:
                G[i][j] = 1  # Unweighted: all edges have weight 1
                G[j][i] = 1
    
    return G

def save_graphs(filename='generateGraphs.txt', num_graphs=5, min_vertices=10, max_vertices=400, graph_type='random', output_dir: Optional[Path] = None):
    """Generate connected graphs and save to file."""
    if output_dir is None:
        output_dir = Path('graphs')
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename
    
    with open(filepath, 'w') as f:
        for _ in range(num_graphs):
            num_vertices = random.randint(min_vertices, max_vertices)
            G = generate_graph(num_vertices, graph_type=graph_type)
            
            f.write(f"{num_vertices}\n")
            for row in G:
                f.write(' '.join(map(str, row)) + '\n')
            f.write("---\n")
    
    print(f"Generated {num_graphs} {graph_type} graphs and saved to {filepath}")
