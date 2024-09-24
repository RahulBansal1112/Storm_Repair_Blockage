from graph import Graph, graph_dict
import random

graph_node_range = 0
graph_edge_range = 0
graph_node_weight_range = 0
graph_node_chance = 0

assert (graph_node_range < graph_edge_range)



random_graph_dict: graph_dict = {
   "num_nodes": 0,
   "edges": [],
   "node_weight": [0 for _ in graph_node_range]
}

random_graph = Graph.from_dict(random_graph_dict)

for i in range(graph_node_range):
    chance = random.randint(1, 10)
    if (chance <= graph_node_chance):
        random_graph.add_node(random.randint(1, graph_node_weight_range))
    else:
        random_graph.add_node(0)
