#include <iostream>
#include <vector>
#include <cstdlib>
#include <numeric>  
#include <ctime>
#include <algorithm>
#include <climits>
#include <random>       
#include <algorithm>
#include<chrono>
using namespace std;
std::random_device rd;
std::mt19937 g(rd());
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

int karger_min_cut_trial(int V, int E, const vector<pair<int, int>>& shuffled_edges ) {
    /*
    Runs one trial of Karger's randomized algorithm using Union-Find.
    This version uses a pre-shuffled index list for max efficiency.
    */
    

    DisjointUnionSets dus(V);

    int vertices = V;
    int index_ptr = 0; // We iterate through the pre-shuffled indices
    for(int i=0;i<shuffled_edges.size();i++){
        if (vertices <= 2) {
            break;
        }
        auto[u,v] = shuffled_edges[i];
        int set1 = dus.find(u);
        int set2 = dus.find(v);
        if (set1 != set2) {
            vertices -= 1;
            dus.unionSets(set1, set2);
        }
    }
    

    // This part remains the same
    int cutedges = 0;
    for (int i = 0; i < E; i++) {
        int subset1 = dus.find(shuffled_edges[i].first);
        int subset2 = dus.find(shuffled_edges[i].second);
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
    
    // Fill indices with 0, 1, 2, ... E-1
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
        std::shuffle(edges.begin(), edges.end(), g);

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
    
    vector<vector<int>> G(V, vector<int>(V, 0));
    
    for (int i = 0; i < E; i++) {
        int src, dst;
        cin >> src >> dst;
        G[src][dst] = 1;
        G[dst][src] = 1;
    }
    auto start = std::chrono::high_resolution_clock::now();

    int result = karger_min_cut(G, trials);
    auto end = std::chrono::high_resolution_clock::now();
    double elapsed = std::chrono::duration<double>(end - start).count();
    cout << result <<" "<< elapsed<<endl;

    return 0;
}
