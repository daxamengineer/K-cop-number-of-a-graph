import networkx as nx
import itertools

def generate_all_connected_graphs(n):
    if n < 1:
        return []
    if n == 1:
        return [nx.complete_graph(1)]
    
    connected_graphs = []
    
    nodes = range(n)
    all_possible_edges = list(itertools.combinations(nodes, 2))

    graphcount = 1
    
    for edges_combination in itertools.product([0, 1], repeat=len(all_possible_edges)):
        edges = [all_possible_edges[i] for i in range(len(all_possible_edges)) if edges_combination[i] == 1]
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        
        if nx.is_connected(G):
            is_duplicate = any(nx.is_isomorphic(G, existing_graph) for existing_graph in connected_graphs)
            if not is_duplicate:
                connected_graphs.append(nx.Graph(G)) 
        
        print()
       # print(f"Graph generation count:  {graphcount}")
        G = nx.Graph()  
        graphcount += 1

        print(len(connected_graphs))
        if len(connected_graphs) == 10000:
            return connected_graphs

    return connected_graphs
