import random
import math

class DisjointUnionSets:
    """
    An object-oriented implementation of the Union-Find
    (or Disjoint Set) data structure.
    """
    def __init__(self, n):
        self.rank = [0] * n
        self.parent = list(range(n))

    def find(self, i):
        """
        Finds the representative (root) of the set containing
        element i, using path compression.
        """
        # Base case: if i is the parent of itself, it's the root
        if self.parent[i] == i:
            return i
        
        # Recursive step: find the root and set i's parent
        # directly to the root (path compression).
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def unionSets(self, x, y):
        """
        Merges the sets containing x and y, using union by rank.
        """
        xRoot = self.find(x)
        yRoot = self.find(y)

        # If they are already in the same set, do nothing
        if xRoot == yRoot:
            return

        # Union by Rank: Attach smaller rank tree under root
        # of high rank tree.
        if self.rank[xRoot] < self.rank[yRoot]:
            self.parent[xRoot] = yRoot
        elif self.rank[yRoot] < self.rank[xRoot]:
            self.parent[yRoot] = xRoot
        else:
            # If ranks are same, make one as root and
            # increment its rank by one
            self.parent[yRoot] = xRoot
            self.rank[xRoot] += 1

def karger_min_cut_trial(V, E, edges):
    """
    Runs one trial of Karger's randomized algorithm using Union-Find.
    
    V: Number of vertices
    E: Number of edges
    edges: List of (src, dest) edge tuples
    
    Returns: The size of the cut found in this trial.
    """
    
    # Allocate memory for creating V subsets using the DSU class
    dus = DisjointUnionSets(V)

    # Initially there are V vertices in contracted graph
    vertices = V

    # Keep contracting vertices until there are 2 vertices.
    while vertices > 2:
        # Pick a random edge (from 0 to E-1)
        i = random.randrange(E)

        # Find vertices (or sets) of two corners of current edge
        subset1 = dus.find(edges[i][0])
        subset2 = dus.find(edges[i][1])

        # If two corners belong to same subset, then no point 
        # considering this edge (it's a self-loop in the
        # contracted graph)
        if subset1 == subset2:
            continue
        
        # Else contract the edge (combine the sets)
        else:
            # print(f"Contracting edge {edges[i][0]}-{edges[i][1]}")
            vertices -= 1
            dus.unionSets(subset1, subset2)

    # Now we have two vertices (or subsets) left.
    # Count the edges between these two components.
    cutedges = 0
    for i in range(E):
        subset1 = dus.find(edges[i][0])
        subset2 = dus.find(edges[i][1])
        if subset1 != subset2:
            cutedges += 1

    return cutedges

# Driver program to test above functions
def karger_min_cut(G,trials = 100):
    """
    Creates a graph, runs Karger's algorithm many times,
    and prints the minimum cut found.
    """
    V = len(G)
   
    edges = []
    
   
    
   
    
    
    
    #this part of the code is to convert the input adjacency matrix into a edge representation
    for i in range(V):
       
        for j in range(i + 1, V):
            if G[i][j] == 1:
                edges.append((i, j))
    
    E = len(edges)
    min_cut = float('inf')
    
    
    for i in range(trials):
        cut_size = karger_min_cut_trial(V, E, edges)
        
        if cut_size < min_cut:
            min_cut = cut_size
    return min_cut

