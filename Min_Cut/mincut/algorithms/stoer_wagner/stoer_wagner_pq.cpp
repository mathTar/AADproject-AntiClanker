#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>
#include <queue>

using namespace std;

int stoer_wagner(vector<vector<int>>& G_mat) {
    /*
    Stoer-Wagner Algorithm for finding minimum cut of a graph.
    
    Input:
        G: Adjacency matrix (vector of vectors) where G[i][j] = weight of edge between i and j
           G[i][i] = 0 (no self loops)
           G[i][j] = 0 means no edge between i and j
    
    Output:
        mincut: Integer value representing the minimum cut weight
    
    Description:
        Finds the minimum weight edge cut that separates a graph into two parts.
    */
    
    // Create a copy of the adjacency matrix to modify
    vector<vector<int>> G = G_mat;
    
    // Get number of vertices
    int V = G.size();
    
    // Initialize minimum cut to infinity
    int mincut = INT_MAX;

    // --- REMOVED Adjacency List Conversion ---
    // The logic below (esp. contraction) is for a matrix,
    // so we will use the matrix G directly.
    
    // Repeat until only 2 vertices remain (which forms a cut)
    while (V > 1) {
        priority_queue<pair<int,int>> pq;
        // Track which vertices have been added to the growing set
        vector<int> added(V, 0);
        
        // Track total edge weight from each vertex to the growing set
        vector<int> weight(V, 0);
        
        // Count of vertices not yet added
        int unadded = V;
        
        // Start by adding vertex 0 to the growing set
        added[0] = 1;
        unadded -= 1;
        
        // Initialize weights: edge weights from each vertex to vertex 0
        // --- FIXED to use Adjacency Matrix G ---
        for (int i = 0; i < V; i++) {
            if (i != 0) { // No self-loops needed in weight
                weight[i] += G[0][i];
                pq.push({weight[i], i});
            }
        }
        
        // Variables to track the last two added vertices
        int prev = -1;
        int last = 0;
        
        // Keep adding vertices until all are processed
        while (unadded > 0) { // <-- FIXED condition
            // Find the vertex with maximum weight (tightest connection)
            int mosttightvertex = -1;
            
            while (!pq.empty()) {
                auto [current_weight, current_vertex] = pq.top();
                pq.pop(); // Always pop the top element

                if (added[current_vertex] == 0) {
                    // This is a valid, un-added vertex.
                    mosttightvertex = current_vertex;
                    break; // Found our vertex
                }
            }
            // --- End of FIXED PQ Logic ---

            if (mosttightvertex == -1) {
                break;
            }
            
            // Track the two most recently added vertices
            prev = last;
            last = mosttightvertex;
            
            // Add this vertex to the growing set
            added[mosttightvertex] = 1;
            unadded -= 1;

            // Update weights: add edge weights from newly added vertex to remaining vertices
            // --- FIXED to use Adjacency Matrix G ---
            for (int i = 0; i < V; i++) {
                if (!added[i]) {
                    weight[i] += G[mosttightvertex][i];
                    pq.push({weight[i], i});
                }
            }
        }

        // Update minimum cut: check the cut value when last two vertices are separated
        if (unadded == 0) { // <-- Added check
            mincut = min(mincut, weight[last]);
        }
        
        if (prev == -1) {
            break; 
        }

        // Merge the two last vertices: combine their edges
        // --- This logic is CORRECT for an Adjacency Matrix ---
        for (int i = 0; i < V; i++) {
            G[prev][i] += G[last][i];
            G[i][prev] = G[prev][i];
        }

        // Remove the last vertex from the graph
        // --- This logic is CORRECT for an Adjacency Matrix ---
        G.erase(G.begin() + last);
        for (int i = 0; i < G.size(); i++) {
            G[i].erase(G[i].begin() + last);
        }
        V -= 1;
    }
    
    // Return the minimum cut value found
    return mincut;
}

// Main function
int main() {
    int V, E;
    cin >> V >> E;
    
    // Create adjacency matrix
    vector<vector<int>> G(V, vector<int>(V, 0));
    
    // Read edges
    for (int i = 0; i < E; i++) {
        int src, dst, weight;
        cin >> src >> dst >> weight;
        G[src][dst] = weight;
        G[dst][src] = weight;
    }
    
    // Run algorithm
    int result = stoer_wagner(G);
    cout  << result << endl; 
    
    return 0;
}