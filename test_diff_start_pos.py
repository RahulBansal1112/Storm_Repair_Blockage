import gc
import random
from collections import deque
from itertools import combinations, permutations, product
from typing import Callable, Deque, Optional
from typing import List, Tuple, Callable, Set

import numpy as np
from more_itertools import set_partitions
import sys

import graph
import algos
import graphs_test
from graph import Graph
from algos import path_length


def different_start_greedy_assignment(g: Graph, k: int, start: list[int]) -> list[list[int]]:

    if Graph.is_complete(g) is False:
        raise ValueError("Passed graph is not complete")

    # The only valid nodes to visit are non-starting nodes
    nodes: list[int] = list(range(0, g.num_nodes))
    # Sort the nodes from heaviest to least heavy
    nodes = sorted(nodes, key=lambda x: g.node_weight[x], reverse=True)
    # All paths must start with the start node
    paths: list[list[int]] = [[start[idx]] for idx in range(k)]

    for node in nodes:
        # if node does have a weight, skip it
        if g.node_weight[node] == 0:
            continue
        # find agent with shortest path (i.e. the agent who will finish first)
        agent: int = min(range(k), key=lambda x: path_length(g, paths[x]))
        # append current node (heaviest unvisited) to agent (assuming the agent isn't already there)
        if paths[agent][0] != node:
            paths[agent].append(node)

    return paths

def create_complete_graph(known: graph.Graph):
    #create complete graph from given info
    shortest_known_paths = algos.floyd_warshall(known)
    small_complete_known_graph_dict: graph.graph_dict = {
        "num_nodes": known.num_nodes,
        "edges": [],
        "node_weight": known.node_weight
    }
    small_complete_known_graph = Graph.from_dict(small_complete_known_graph_dict)
    for start_node in range (known.num_nodes):
        for end_node in range (known.num_nodes):
            small_complete_known_graph.add_edge(start_node, end_node, shortest_known_paths[start_node][end_node])
    return small_complete_known_graph


def get_paths(known: graph.Graph, num_agents: int, start_pos: List[int]):
    paths = different_start_greedy_assignment(known, num_agents, start_pos)
    return paths


known_graph = create_complete_graph(graphs_test.two_long_path_graph_known)

print(get_paths(known_graph, 3, [0, 4, 7]))

algos.transfers_and_swaps_mwlp(
            known_graph, get_paths(known_graph, 3, [0, 4, 7]), algos.greedy
        )
