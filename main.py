from graph import Graph, graph_dict

gd: graph_dict = {
    "num_nodes": 3,
    "edges": [(0, 1, 1.0), (1, 0, 2.0), (0, 2, 3.0), (2, 0, 4.0)],
    "node_weight": [0, 0, 0],
}
g = Graph.from_dict(gd)
print(g.adjacen_list)
