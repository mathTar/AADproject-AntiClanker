
def stoer_wagner(G):
    """
    Stoer-Wagner Algorithm for finding minimum cut of a graph.
    
    Input:
        G: Adjacency matrix (list of lists) where G[i][j] = weight of edge between i and j
           G[i][i] = 0 (no self loops)
           G[i][j] = 0 means no edge between i and j
    
    Output:
        mincut: Integer value representing the minimum cut weight
    
    Description:
        Finds the minimum weight edge cut that separates a graph into two parts.
    """
    # Get number of vertices
    V = len(G)
    
    # Initialize minimum cut to infinity
    mincut = float('inf')
   
    # Repeat until only 2 vertices remain (which forms a cut)
    while V > 1:
        # Track which vertices have been added to the growing set
        added = [False for i in range(V)]
        
        # Track total edge weight from each vertex to the growing set
        weight = [0 for i in range(V)]
        
        # Count of vertices not yet added
        unadded = V
        
        # Start by adding vertex 0 to the growing set
        added[0] = 1
        unadded -= 1
        
        # Initialize weights: edge weights from each vertex to vertex 0
        for i in range(V):
            weight[i] += G[i][0]
        
        # Variables to track the last two added vertices
        prev = -1
        last = 0
        
        # Keep adding vertices until all are processed
        while unadded:
            # Find the vertex with maximum weight (tightest connection)
            mosttightvertex = -1
            maxval = -1
            for i in range(V):
                if weight[i] > maxval and added[i] == 0:
                    maxval = weight[i]
                    mosttightvertex = i
            
            # Track the two most recently added vertices
            prev = last
            last = mosttightvertex
            
            # Add this vertex to the growing set
            added[mosttightvertex] = 1
            unadded -= 1

            # Update weights: add edge weights from newly added vertex to remaining vertices
            for i in range(V):
                if not added[i]:
                    weight[i] += G[mosttightvertex][i]

        # Update minimum cut: check the cut value when last two vertices are separated
        mincut = min(mincut, weight[last])
        
        # Merge the two last vertices: combine their edges
        for i in range(V):
            G[prev][i] += G[last][i]
            G[i][prev] = G[prev][i]

        # Remove the last vertex from the graph
        for i in range(V):
            del G[i][last]
        del G[last]
        V -= 1
    
    # Return the minimum cut value found
    return mincut
        


G =[
    [0,1,100,1],
    [1,0,2,0],
    [0,2,0,2],
    [100,0,2,0]
    
]






