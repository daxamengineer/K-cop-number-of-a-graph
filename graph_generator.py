from itertools import combinations

def is_connected(graph, n):
    visited = [False] * n
    stack = [0]
    visited[0] = True
    count = 1
    
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)
                count += 1
                
    return count == n

def generate_all_connected_graphs(n):
    if n <= 0:
        return []
    
    vertex_pairs = list(combinations(range(n), 2))
    
    total_graphs = 2 ** len(vertex_pairs)
    
    connected_graphs = []
    
    for i in range(total_graphs):

        graph = {v: [] for v in range(n)}
        edge_count = 0
        
        for j, (u, v) in enumerate(vertex_pairs):
            if (i & (1 << j)) != 0:
                graph[u].append(v)
                graph[v].append(u)
                edge_count += 1

        if is_connected(graph, n):
            connected_graphs.append(graph)
    
    return connected_graphs

n = 3
connected_graphs = generate_all_connected_graphs(n)
print(connected_graphs)
for idx, graph in enumerate(connected_graphs):
    print(f"Graph {idx + 1}: {graph}")
