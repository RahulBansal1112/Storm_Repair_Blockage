from graph import Graph, graph_dict
import random
import algos

'''
edges must be greater than (n-1) and less than (n)(n-1)

'''



'''
steps:
create known graph -> ensure that every node is connected
use known graph to create corresponding "unknown" graph -> ensure every node is connected



'''
def is_connected(graph: Graph) -> bool:
    short_paths = algos.floyd_warshall(graph)
    for i in range(graph.num_nodes):
        if float('inf') in short_paths[i]:
            return False
    return True


def visibility(graph: Graph) -> list:
    visibility = [[] for _ in range(graph.num_nodes)]
    for i in range(graph.num_nodes):
        for j in range(graph.num_nodes):
            if graph.contains_edge(i, j):
                visibility[i].append((i,j))
            if graph.contains_edge(j, i):
                visibility[i].append((j, i))
    
    return visibility



def generate_random_graph(num_nodes: int, edge_chance: int, max_edge_weight: int, max_node_weight: int, node_chance: int, edge_removal_chance: int):
    random_graph_dict: graph_dict = {
   "num_nodes": 0,
   "edges": [],
   "node_weight": [0 for _ in num_nodes]
    }

    random_graph = Graph.from_dict(random_graph_dict)

    targets = []

    for i in range(num_nodes):
        chance = random.randint(1, 10)
        if (chance <= node_chance):
            random_graph.add_node(random.randint(1, max_node_weight))
            targets.append(i)
        else:
            random_graph.add_node(0)

    shortest_paths = algos.floyd_warshall(random_graph)

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.randint(1,10) <= edge_chance:
                random_graph.add_edge(i, j, random.randint(1, max_edge_weight))

    while (not is_connected(random_graph)):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i != j and random.randint(1,10) <= edge_chance and not random_graph.contains_edge(i, j):
                    random_graph.add_edge(i, j, random.randint(1, max_edge_weight))
    
    random_graph_unknown = random_graph

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.randint(1,10) <= edge_removal_chance and random_graph.contains_edge(i, j):
                random_graph_unknown.delete_edge(i, j)
            if not is_connected(random_graph_unknown):
                random_graph_unknown.add_edge(i, j, random_graph.edge_weight[i][j])

    visibility = visibility(random_graph)


    return random_graph, random_graph_unknown, visibility, targets

def main():
    num_nodes = 10 # number of nodes
    edge_chance = 8 # chance an edge is created between 2 nodes
    max_edge_weight = 5 
    max_node_weight = 5
    node_chance = 6 #chance a node is designated as a target node (chance a node is given a weight other than zero)
    edge_removal_chance = 1 #chance an edge is removed when making an unknown graph


    known_graph, unknown_graph, visibility, targets = generate_random_graph(num_nodes, edge_chance, max_edge_weight, max_node_weight, node_chance, edge_removal_chance)

    print(known_graph)
    print(unknown_graph)
    print(visibility)

    

