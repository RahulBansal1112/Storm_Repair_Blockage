"""
Graph class with integer nodes, integer node weights, float edge weights
"""
from __future__ import annotations

import json
import random
from itertools import product
from typing import Collection, no_type_check

# import networkx as nx  # type: ignore
from typing_extensions import TypedDict

graph_dict = TypedDict(
    "graph_dict",
    {
        # number of nodes
        "num_nodes": int,
        # list of correct length of node_weights
        "node_weight": list[int],
        # list of tuples of form (start_node, end_node, node_weight)
        "edges": list[tuple[int, int, float]],
    },
)


class Graph:
    """Directed graph class with weighted edges and nodes

    Attributes:
        num_nodes: number of nodes from [0, n)
        adjacen_list: directed adjacency list
        edge_weight: 2D matrix representing l(i, j)
        node_weight: list of all weights w(i)

    """

    def __init__(self, n: int = 0):
        """
        Creates a graph with n nodes

        Parameters
        ----------
        n: int
            Number of nodes in the graph
            Default: 0
            Assertions:
                Assertion 1
                Assertion 2

        Returns
        -------
        Graph
            Graph with n nodes and no edges or node weights

        """

        if n < 0:
            raise ValueError(f"Number of nodes passed in is negative: {n}")

        self.num_nodes = n
        self.adjacen_list: list[list[int]] = [[] for _ in range(n)]
        self.edge_weight: list[list[float]] = [
            [1000000 for _ in range(n)] for _ in range(n)
        ]
        self.node_weight: list[int] = [0 for _ in range(n)]

    @staticmethod
    def from_dict(gd: graph_dict) -> Graph:
        """
        Alternate constructor using dictionary

        Parameters
        ----------
        gd: graph_dict
            Contains the needed information for a graph
            Assertions:
                Number of nodes must be >= 0
                List of node weights must be correct length
                Node weights must be all >= 0
                Edges must be between nodes that exist

        Returns
        -------
        Graph
            Graph with nodes and edges as described by the dictionary

        """

        if gd["num_nodes"] < 0:
            raise ValueError(f"Number of nodes is negative: {gd['num_nodes']}")
        g = Graph(gd["num_nodes"])

        if len(gd["node_weight"]) != g.num_nodes:
            raise ValueError(
                "node_weight list is incorrect length: "
                + f"{gd['node_weight']} vs {g.num_nodes}"
            )

        if min(gd["node_weight"]) < 0:
            raise ValueError(
                f"node_weight list contains negative values: {gd['node_weight']}"
            )
        g.node_weight = gd["node_weight"]

        for start_node, end_node, edge_weight in gd["edges"]:
            if start_node >= g.num_nodes or g.num_nodes < 0:
                raise ValueError(
                    f"Starting node {start_node} is out of range [0, {g.num_nodes - 1}]"
                )
            if end_node >= g.num_nodes or g.num_nodes < 0:
                raise ValueError(
                    f"Ending node {end_node} is out of range [0, {g.num_nodes - 1}]"
                )
            g.add_edge(start_node, end_node, edge_weight)

        return g

    @staticmethod
    def dict_from_graph(g: Graph) -> graph_dict:
        """
        Create graph_dict from passed Graph

        Parameters
        ----------
        g: Graph
            Graph to be encoded into a dictionary

        Returns
        -------
        graph_dict
            Dictionary that can be transformed back into passed graph

        """

        num_nodes: int = g.num_nodes
        node_weight: list[int] = g.node_weight

        edges: list[tuple[int, int, float]] = []
        for (i, j) in product(range(num_nodes), range(num_nodes)):
            if i != j and j in g.adjacen_list[i]:
                edges.append((i, j, g.edge_weight[i][j]))

        gd: graph_dict = {
            "num_nodes": num_nodes,
            "edges": edges,
            "node_weight": node_weight,
        }

        return gd

    @staticmethod
    def from_file(loc: str) -> Graph:
        """
        Alternate constructor using graph_dict from json

        Parameters
        ----------
        loc: str
            file location of dictionary json

        Returns
        -------
        Graph
            Graph with nodes and edges as described by the json file

        """

        with open(loc, encoding="utf-8") as gd_json:
            gd: graph_dict = json.load(gd_json)
            return Graph.from_dict(gd)

    @staticmethod
    def to_file(g: Graph, loc: str) -> None:
        """
        Write graph to a file

        Parameters
        ----------
        g: Graph
            input graph

        loc: str
            file location of dictionary json

        """

        with open(loc, "w", encoding="utf-8") as outfile:
            gd: graph_dict = Graph.dict_from_graph(g)
            json.dump(gd, outfile)


    def add_repair_time(self, amt: float = 0.0) -> None:
        """
        Adds a desired fixed repair time to all edges

        Parameters
        ----------
        amt: float
            Repair time to be added
            Default: 0.0
            Assertions:
                Must be non-negative

        """

        if amt < 0.0:
            raise ValueError(f"Passed repair time is negative: {amt}")

        n: int = self.num_nodes
        for u, v in product(range(n), range(n)):
            if u != v:
                self.edge_weight[u][v] += amt


    def add_node(self, node_weight: int = 0) -> None:
        """
        Add a node to a graph

        Parameters
        ----------
        node_weight: int
            Node weight of new node
            Default: 0
            Assertions:
                Node weight must be >= 0

        """

        if node_weight < 0:
            raise ValueError(f"Passed node_weight is negative: {node_weight}")

        self.num_nodes += 1
        self.adjacen_list.append([])
        self.node_weight.append(node_weight)

        # need to add slot for new node to edge weight matrix
        for weight_list in self.edge_weight:
            weight_list.append(1000000)

        # add new row to edge weight matrix
        self.edge_weight.append([1000000 for _ in range(self.num_nodes)])

    def add_edge(self, start: int, end: int, weight: float = 0.0) -> None:
        """
        Add an edge to a graph

        Parameters
        ----------
        start: int
            Start node of edge
            Assertions:
                Node must be in the graph

        end: int
            End node of edge
            Assertions:
                Node must be in the graph

        Assertion:
            Edge cannot already exist

        weight: float
            Weight of edge start -> end
            Default: 0.0

        """

        # ensure nodes exist
        if start >= self.num_nodes or start < 0:
            raise ValueError(
                f"Starting node {start} is out of range [0, {self.num_nodes - 1}]"
            )
        if end >= self.num_nodes or end < 0:
            raise ValueError(
                f"Ending node {end} is out of range [0, {self.num_nodes - 1}]"
            )

        # add edge only once
        if end in self.adjacen_list[start]:
            raise ValueError(
                f"Edge from {start} to {end} already exists "
                + "with weight {self.edge_weight[start][end]}"
            )

        self.adjacen_list[start].append(end)
        self.edge_weight[start][end] = weight

    def set_node_weight(self, node: int, node_weight: int) -> None:
        """
        Change node weight of a desired node

        Parameters
        ----------
        node: int
            Node whose weight is being changed
            Assertions:
                Node must be in the graph

        node_weight: int
            New node weight of node
            Assertions:
                Node weight must be >= 0

        """

        if node >= self.num_nodes or node < 0:
            raise ValueError(f"Node {node} is out of range [0, {self.num_nodes - 1}]")

        if node_weight < 0:
            raise ValueError(f"Passed node_weight is negative: {node_weight}")

        self.node_weight[node] = node_weight

    def set_edge_weight(
        self, start_node: int, end_node: int, edge_weight: float
    ) -> None:
        """
        Change edge weight of an edge in the graph

        Parameters
        ----------
        start_node: int
            Start node of edge
            Assertions:
                Node must be in the graph

        end_node: int
            End node of edge
            Assertions:
                Node must be in the graph

        Assertion:
            Edge must exist

        edge_weight: float
            New weight of edge start -> end

        """

        # ensure nodes exist
        if start_node >= self.num_nodes:
            raise ValueError(
                f"Starting node {start_node} is out of range [0, {self.num_nodes - 1}]"
            )
        if end_node >= self.num_nodes:
            raise ValueError(
                f"Ending node {end_node} is out of range [0, {self.num_nodes - 1}]"
            )

        if edge_weight < 0.0:
            raise ValueError(f"Edge has negative weight {edge_weight}")
        # add weight only if edge exists
        if end_node not in self.adjacen_list[start_node]:
            raise ValueError(f"{end_node} is not a neighbor of {start_node}")

        self.edge_weight[start_node][end_node] = edge_weight

    