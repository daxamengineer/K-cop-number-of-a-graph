import networkx as nx
import matplotlib.pyplot as plt
import os
import graph_generator

def closed_neighborhood(G, u):
    return set(G.neighbors(u)).union({u})

def strong_product(G1, G2):
    R = nx.Graph()
    for u in G1.nodes:
        for v in G2.nodes:
            R.add_node((u, v))
    
    for (u1, u2) in G1.edges:
        for v in G2.nodes:
            R.add_edge((u1, v), (u2, v))
            R.add_edge((u2, v), (u1, v))
    
    for u in G1.nodes:
        for (v1, v2) in G2.edges:
            R.add_edge((u, v1), (u, v2))
            R.add_edge((u, v2), (u, v1))
    
    for (u1, u2) in G1.edges:
        for (v1, v2) in G2.edges:
            R.add_edge((u1, v1), (u2, v2))
            R.add_edge((u2, v2), (u1, v1))
            R.add_edge((u1, v2), (u2, v1))
            R.add_edge((u2, v1), (u1, v2))

    return R

def strong_product_k_times(G, k):
    R = G
    for _ in range(k - 1):
        R = strong_product(R, G)
    return R

def check_k_cop_number(G, k):
    """Implements the CHECK k-COP NUMBER algorithm."""
    G_k_strong = strong_product_k_times(G, k)
    converted_strong_product = {node: list(neighbors) for node, neighbors in G_k_strong.adj.items()}
    
    total_vertices = []
    f = {}

    for u in converted_strong_product:
        total_vertices.append(u)
    
    for u in converted_strong_product:
        closed_neighbour_list = converted_strong_product[u]
        closed_neighbour_list.append(u)
        f[u] = list(set(total_vertices) - set(closed_neighbour_list))
    
    while True:
        f_prev = f.copy()

        for u, v in G_k_strong.edges:
            closed_neighbour_list_u = converted_strong_product[u]
            closed_neighbour_list_u.append(u)    

            closed_neighbour_list_v = converted_strong_product[v]
            closed_neighbour_list_v.append(v)    
            f[u] = list(set(f[u]) & set(closed_neighbour_list_v))
            f[v] = list(set(f[v]) & set(closed_neighbour_list_u))
            
        if f == f_prev:
            break
    
    for u in converted_strong_product:
        if f[u] == []:
            return f"c(G) ≤ {k}"
    
    return f"c(G) > {k}"

n = 19

graph_list = graph_generator.generate_all_connected_graphs(n)
print("Graphs Generated")
print()
count = 1
for graph in graph_list:
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                G.add_edge(i, j)
    k = 3
    result = check_k_cop_number(G, k)
    
    output_dir = "output_graphs"
    nx.draw(G)
    plt.text(0.5, 0.02, result, fontsize=12, ha='center')
    output_path = os.path.join(output_dir, f"graph {count}.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Output {count} complete")
    count += 1
    print()
