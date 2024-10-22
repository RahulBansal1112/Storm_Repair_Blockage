from graph import Graph, graph_dict
import random

graph_node_range = 0 #set this for number of nodes you want
graph_edge_range = 0 #set this for number of edges you want (edges must be at least the same as number of nodes)
'''
edges must be greater than (n-1) and less than (n)(n-1)

'''
graph_node_weight_range = 0 
graph_node_chance = 0

assert (graph_edge_range > (graph_node_range - 1) and graph_edge_range <= (graph_node_range - 1)*(graph_node_range))

'''
steps:
create known graph -> ensure that every node is connected
use known graph to create corresponding "unknown" graph -> ensure every node is connected



'''

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
