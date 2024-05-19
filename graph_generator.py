import itertools
import networkx as nx
import time

def generate_all_connected_graphs(n, limit = 1000):
    if n < 1:
        raise ValueError("Number of vertices n must be at least 1.")
    if n == 1:
        return [[[0]]]

    num_edges = n * (n - 1) // 2
    start_time = time.time()

    def is_connected(graph):
        G = nx.Graph()
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    G.add_edge(i, j)
        return len(G.nodes) == n and nx.is_connected(G)

    def is_unique(graph, unique_graphs):
        G1 = nx.Graph()
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    G1.add_edge(i, j)
        for G2 in unique_graphs:
            if nx.is_isomorphic(G1, G2):
                return False
        unique_graphs.append(G1)
        return True

    all_graphs = []
    unique_graphs = []
    generated_counter = 0
    total_counter = 0

    for edges_bitmap in range(1 << num_edges):
        graph = [[0] * n for _ in range(n)]
        edge_index = 0
        for i in range(n):
            for j in range(i + 1, n):
                if edges_bitmap & (1 << edge_index):
                    graph[i][j] = 1
                    graph[j][i] = 1
                edge_index += 1

        if is_connected(graph) and is_unique(graph, unique_graphs):
            all_graphs.append(graph)
            print(f"Graph {generated_counter + 1} generated")
            generated_counter += 1

        total_counter += 1
        
        if total_counter % 100000 == 0:
            end_time = time.time()
            print(f"Checked {total_counter} graphs in {end_time - start_time} seconds.")
            if end_time - start_time > 3600:  # Stop after 1 hour
                print("Stopping early due to time constraints.")
                return all_graphs
            
    return all_graphs

