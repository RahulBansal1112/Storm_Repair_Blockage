import graph
from graph import Graph
from graphs_test import small_graph_known, small_graph_unknown, small_graph_visibility
from typing import List, Tuple, Callable, Set
import algos

import time

class MultiAgentSimulator:
    """Simulates single agent traversing a graph with multiple target

    Attributes:
        TODO
    """

    # you can initialize these if you want
    agent_pos = [] # current agent positions
    agent_dest = [] # next node each agent is traveling towards
    agent_target = [] # current assigned target the agent is travelling towards
    agent_path = [[]]
    agent_progress = [] # how far along the path the agents are
    num_agents = 1
    # known = small_graph_known
    # unknown = small_graph_unknown
    time = 0
    visibility = []
    discovered_edges = []
    broken_edges = []
    targets: Set[int] #list of targets agents have to repair
    algorithm: Callable[[graph.Graph, List[int]], List[int]]
    discovered_count = 0
    broken_count = 0
    cd = 0.20

    agent_target = []
    prev_discovered_count = 0

    def __init__(self, known: graph.Graph, unknown: graph.Graph, visibility: List[List[Tuple]], num_agents: int, targets: List[int]):
        self.known = known
        self.unknown = unknown
        self.visibility = visibility
        self.num_agents = num_agents
        self.targets = set(targets)
        self.agent_pos = [0] * num_agents
        self.agent_dest = [-1] * num_agents
        self.agent_progress = [0] * num_agents
        self.agent_target = [-1] * num_agents
        self.agent_path = [[self.agent_pos[idx]] for idx in range(num_agents)]

        self.agent_target = [-1] * self.num_agents
        

    def _get_new_dest(self):
        self.agent_path[0] = algos.brute_force_mwlp(self.known, self.agent_pos[0]) 
        self.agent_dest = self.algorithm(self.known, self.agent_pos)
    
        
    def run_simu(self):

        self._update_known_graph()

        while(len(self.targets) > 0):
            print(f"agent pos: {self.agent_pos}")

            self.prev_discovered_count = self.broken_count
            #update known graph
            self._update_known_graph()

            #create complete graph from given info
            shortest_known_paths = algos.floyd_warshall(self.known)
            small_complete_known_graph_dict: graph.graph_dict = {
                "num_nodes": self.known.num_nodes,
                "edges": [],
                "node_weight": self.known.node_weight
            }
            small_complete_known_graph = Graph.from_dict(small_complete_known_graph_dict)
            for start_node in range (self.known.num_nodes):
                for end_node in range (self.known.num_nodes):
                    small_complete_known_graph.add_edge(start_node, end_node, shortest_known_paths[start_node][end_node])
            #complete known graph will be used to access shortest path between nodes, however when traversing, we will use the incomplete graph

            # finds the initial path for the agents (not accounting for visibility)
            paths = self.get_targets()

            # finds the shortest path from an agent's current position to its (first) target node
            for agent in range(self.num_agents):
                if (self.agent_target[agent] != -1):
                    self.agent_path[agent] = algos.shortest_path(self.known, self.agent_pos[agent], paths[agent])
                    self.agent_dest[agent] = self.agent_path[agent][1]
            print(f"agent path: {self.agent_path}")
            print(f"agent dest: {self.agent_dest}")

            # self.cd = self.broken_count/self.discovered_count

            #update position and time
            self._update_positions()

            for agent_num in range(self.num_agents):
                if self.agent_pos[agent_num] in self.targets:
                    self.known.set_node_weight(self.agent_pos[agent_num], 0)
                    self.targets.remove(self.agent_pos[agent_num])
        

    def _update_positions(self) -> int:
        
        agents_at_node = []
        time_delta = min((self.known.edge_weight[self.agent_pos[agent]][self.agent_dest[agent]] - self.agent_progress[agent] for agent in range(self.num_agents) if self.agent_dest[agent] != -1), default=0)
        self.time += time_delta
        self.agent_progress = [progress + time_delta for progress in self.agent_progress]
        for agent in range(self.num_agents):
            if (self.agent_dest[agent] == -1):
                self.agent_progress[agent] == 0
                continue
            if self.known.edge_weight[self.agent_pos[agent]][self.agent_dest[agent]] == self.agent_progress[agent]:
                self.agent_pos[agent] = self.agent_dest[agent]
                self.agent_dest[agent] = -1
                self.agent_progress[agent] = 0
                agents_at_node.append(agent)
        return agents_at_node
    
    
        
    
    def _update_known_graph(self) -> None:
        
        for agent_num in range(self.num_agents):
            #add visible edges from visibility to our list of discovered edges
            for edges in self.visibility[self.agent_pos[agent_num]]:
                self.discovered_edges.append(edges)
            self.visibility[self.agent_pos[agent_num]] = []
            
            #if the edge does not exist in our unknown graph delete it from known graph and add edge to list of broken edges
            for edge in self.discovered_edges:
                if (not self.unknown.contains_edge(edge[0], edge[1])):
                    self.known.delete_edge(edge[0], edge[1])
                    self.broken_edges += edge

        #gets rid of all repeat edges in broken and discovered edges list
        self.broken_edges = list(dict.fromkeys(self.broken_edges))
        self.discovered_edges = list(dict.fromkeys(self.discovered_edges))

        #adjusts the value of the amount of broken and discovered edges
        self.broken_count = len(self.broken_edges)
        self.discovered_count = len(self.discovered_edges)

    
    def consider_vantage_nodes(self) -> None:
        for agent_num in range(self.num_agents):
            target_node = self.agent_path[agent_num][-1]

            #find path based on equation
            min_path_cost = float('inf')

            new_dest = -1
            for vantage_node in range(self.known.num_nodes):
                if (vantage_node == self.agent_pos[agent_num]):
                    continue
                path, path_cost = self.vantage_vs_target(agent_num, vantage_node, target_node)
                if path_cost < min_path_cost:
                    self.agent_path[agent_num] = path
                    min_path_cost = path_cost
                if self.agent_dest[agent_num] == -1:
                    self.agent_dest[agent_num] = self.agent_path[agent_num][1]

    def get_targets(self):
        targets = list(self.targets)
        for agent_num in range(self.num_agents):
            if (self.agent_dest[agent_num] == -1 and self.agent_pos[agent_num] == 0):
                    self.agent_target[agent_num] = -1
        if (self.broken_count != self.prev_discovered_count):
            print("broken edge found")
            for agent_num in range(self.num_agents):
                if (self.agent_target[agent_num] == targets[0]):
                    self.agent_target[agent_num] = 0
            for agent_num in range(self.num_agents):
                if (self.agent_target[agent_num] == -1):
                    self.agent_target[agent_num] = targets[0]
                    break
        if (targets[0] not in self.agent_target):
            for agent_num in range(self.num_agents):
                if (self.agent_target[agent_num] == -1):
                    self.agent_target[agent_num] = targets[0]
                    break
        return self.agent_target
        

