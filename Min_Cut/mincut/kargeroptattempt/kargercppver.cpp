#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <climits>
#include<chrono>
using namespace std;

class DisjointUnionSets {
    /*
    An object-oriented implementation of the Union-Find
    (or Disjoint Set) data structure.
    */
public:
    vector<int> rank;
    vector<int> parent;

    DisjointUnionSets(int n) {
        rank.assign(n, 0);
        parent.resize(n);
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
    }

    int find(int i) {
        /*
        Finds the representative (root) of the set containing
        element i, using path compression.
        */
        // Base case: if i is the parent of itself, it's the root
        if (parent[i] == i) {
            return i;
        }
        
        // Recursive step: find the root and set i's parent
        // directly to the root (path compression).
        parent[i] = find(parent[i]);
        return parent[i];
    }

    void unionSets(int x, int y) {
        /*
        Merges the sets containing x and y, using union by rank.
        */
        int xRoot = find(x);
        int yRoot = find(y);

        // If they are already in the same set, do nothing
        if (xRoot == yRoot) {
            return;
        }

        // Union by Rank: Attach smaller rank tree under root
        // of high rank tree.
        if (rank[xRoot] < rank[yRoot]) {
            parent[xRoot] = yRoot;
        } else if (rank[yRoot] < rank[xRoot]) {
            parent[yRoot] = xRoot;
        } else {
            // If ranks are same, make one as root and
            // increment its rank by one
            parent[yRoot] = xRoot;
            rank[xRoot] += 1;
        }
    }
};

int karger_min_cut_trial(int V, int E, vector<pair<int, int>>& edges) {
    /*
    Runs one trial of Karger's randomized algorithm using Union-Find.
    
    V: Number of vertices
    E: Number of edges
    edges: Vector of (src, dest) edge pairs
    
    Returns: The size of the cut found in this trial.
    */
    
    // Allocate memory for creating V subsets using the DisjointUnionSets class
    DisjointUnionSets dus(V);

    // Initially there are V vertices in contracted graph
    int vertices = V;

    // Keep contracting vertices until there are 2 vertices.
    while (vertices > 2) {
        // Pick a random edge (from 0 to E-1)
        int i = rand() % E;

        // Find vertices (or sets) of two corners of current edge
        int subset1 = dus.find(edges[i].first);
        int subset2 = dus.find(edges[i].second);

        // If two corners belong to same subset, then no point 
        // considering this edge (it's a self-loop in the
        // contracted graph)
        if (subset1 == subset2) {
            continue;
        }
        
        // Else contract the edge (combine the sets)
        else {
            // cout << "Contracting edge " << edges[i].first << "-" << edges[i].second << endl;
            vertices -= 1;
            dus.unionSets(subset1, subset2);
        }
    }

    // Now we have two vertices (or subsets) left.
    // Count the edges between these two components.
    int cutedges = 0;
    for (int i = 0; i < E; i++) {
        int subset1 = dus.find(edges[i].first);
        int subset2 = dus.find(edges[i].second);
        if (subset1 != subset2) {
            cutedges += 1;
        }
    }

    return cutedges;
}

// Driver program to test above functions
int karger_min_cut(vector<vector<int>>& G, int trials = 100) {
    /*
    Creates a graph, runs Karger's algorithm many times,
    and returns the minimum cut found.
    */
    int V = G.size();
   
    vector<pair<int, int>> edges;
    
    // this part of the code is to convert the input adjacency matrix into an edge representation
    for (int i = 0; i < V; i++) {
       
        for (int j = i + 1; j < V; j++) {
            if (G[i][j] == 1) {
                edges.push_back(make_pair(i, j));
            }
        }
    }
    
    int E = edges.size();
    int min_cut = INT_MAX;
    
    for (int i = 0; i < trials; i++) {
        int cut_size = karger_min_cut_trial(V, E, edges);
        
        if (cut_size < min_cut) {
            min_cut = cut_size;
        }
    }
    return min_cut;
}

// Main function
int main() {
    srand(time(0));
    
    int V, E, trials = 100;
    cin >> V >> E >> trials;
    
    vector<vector<int>> G(V, vector<int>(V, 0)); // VxV adj matrix G
    
    for (int i = 0; i < E; i++) {
        int src, dst;
        cin >> src >> dst;
        G[src][dst] = 1;
        G[dst][src] = 1;
    } // undirectd graph. populate G for edges
    auto start = std::chrono::high_resolution_clock::now();

    int result = karger_min_cut(G, trials);
    auto end = std::chrono::high_resolution_clock::now();
    double elapsed = std::chrono::duration<double>(end - start).count();

    cout << result <<" "<< elapsed<<endl;
    
    return 0;
}
