import networkx as nx
import matplotlib.pyplot as plt

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
        print(_)
        R = strong_product(R, G)
    return R

def check_k_cop_number(G, k, strong_product_func):
    """Implements the CHECK k-COP NUMBER algorithm."""
    G_k_strong = strong_product_k_times(G, k, strong_product_func)
    f = {u: set(G.nodes) - closed_neighborhood(G, u[0]) for u in G_k_strong.nodes}
    
    while True:
        f_prev = f.copy()

        for u, v in G_k_strong.edges:
            f[u] = f[u].intersection(set().union(*(closed_neighborhood(G, w[0]) for w in f[v])))
            f[v] = f[v].intersection(set().union(*(closed_neighborhood(G, w[0]) for w in f[u])))
        if f == f_prev:
            break
    
    for u in G_k_strong.nodes:
        if not f[u]:
            return f"c(G) ≤ {k}"
    
    return f"c(G) > {k}"

adj_list_G = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1]
    }
    
G = nx.Graph(adj_list_G)

k = 4
result = check_k_cop_number(G, k)
print(result)