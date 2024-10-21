'''
Ignore this for now, this is the same as m_a_s.py
I was tweaking about the code not being clean
I want to comment this out for my sake so I can see it nicer
'''


import graph
from graph import Graph
from graphs_test import small_graph_known, small_graph_unknown, small_graph_visibility
from typing import List, Tuple, Callable, Set
import algos
import time

class MultiAgentSimulator:
    """
    Simulates multiple agents traversing a graph with multiple targets
    """
    #initialize
    agent_pos = [] #current agent positions
    agent_dest = [] # next node each agent is traveling to
    agent_path = [[]] #paths of each agent to the first immediate target
    agent_progress = [] #how far along the current edge each agent is
    num_agents = 1 #change number when needed
    visibility = [[]] #visibility of the graph from each node, represented as an array of tuples of edge to edge
    discovered_edges = [] #edges that have been seen by agents
    broken_edges = [] #discovered edges that are broken
    targets: Set[int] #list of targets agents have to repair
    discovered_edge_count = 0 #count of discovered edges
    broken_edge_count = 0 #count of broken edges
    cd = 0.20 #chance of edges being broken


    def __init__(self, known: graph.Graph, unknown: graph.Graph, visibility: List[List[Tuple]], num_agents: int, targets: List[int]):
        """
        initialize simulator
        """
        self.known = known
        self.unknown = unknown
        self.visibility = visibility
        self.num_agents = num_agents
        self.targets = set(targets)
        self.agent_pos = [0] * num_agents
        self.agent_dest = [-1] * num_agents
        self.agent_progress = [0] * num_agents
        self.agent_path = [[self.agent_pos[idx]] for idx in range(num_agents)]
    
    def run_simu(self):
        """
        
        """
        while(len(self.targets) > 0):
            
            self._update_known_graph()

            '''
            create a complete graph (all nodes connect) from the updated known graph
            this graph will be used to access the shortest paths between nodes
            however when traversing, we will use the incomplete graph and work step by step
            '''
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
            
            '''
            create the agent paths using Anakin's method
            (altered to account for different starting positions)
            '''
            target_paths = algos.different_start_greedy_assignment(small_complete_known_graph, self.num_agents, self.agent_pos)

            partition = algos.different_start_find_partition_with_heuristic(small_complete_known_graph, target_paths, self.agent_pos, algos.different_start_greedy_assignment, alpha=0.13)

            paths = algos.solve_partition(small_complete_known_graph, partition, self.agent_pos, algos.different_start_greedy_assignment)

            '''
            using the paths, we set the current path of each agent from their current position to their immediate next target
            if the agent has not been assigned a target it goes to the first target in the list
            '''
            for agent in range(self.num_agents):
                if len(paths[agent]) >= 2:
                    self.agent_path[agent] = algos.shortest_path(self.known, self.agent_pos[agent], paths[agent][1])
                else: 
                    self.agent_path[agent] = algos.shortest_path(self.known, self.agent_pos[agent], list(self.targets)[0])
            
            #change the broken edge chance based off of how many broken edges we have discovered
            self.cd = self.broken_edge_count/self.discovered_edge_count

            for agent_num, target_path in enumerate(paths):
                target_node = self.agent_path[agent_num][-1]

                min_path_cost = float('inf')

                new_dest = [-1] * self.num_agents
                for vantage_node in range(self.known.num_nodes):
                    if vantage_node == self.agent_pos[agent_num]:
                        continue
                    path, path_cost = self.vantage_vs_target(agent_num, vantage_node, target_node)
                    if path_cost < min_path_cost:
                        self.agent_path[agent_num] = path
                        min_path_cost = path_cost

                        if self.agent_dest[agent_num] == -1:
                            new_dest[agent_num] = self.agent_path[agent_num][1]
                for agent_num in range(self.num_agents):
                    if self.agent_dest[agent_num] == -1:
                        self.agent_dest[agent_num] = new_dest[agent_num]
            
            self._update_positions()

            for agent_num in range(self.num_agents):
                if self.agent_pos[agent_num] in self.targets:
                    self.known.set_node_weight(self.agent_pos[agent_num], 0)
                    self.targets.remove(self.agent_pos[agent_num])

    def vantage_vs_target(self, agent_num: int, vantage_node: int, target_node: int) -> list:

        path_to_vantage = algos.shortest_path(self.know, self.agent_pos[agent_num], vantage_node)
        path_to_target = algos.shortest_path(self.know, self.agent_pos[agent_num], target_node)
        vantage_to_target_path = algos.shortest_path(self.know, vantage_node, target_node)


        vantage_path_cost = algos.path_length(self.known, path_to_vantage)
        target_path_cost = algos.path_length(self.known, path_to_target)
        vantage_to_target_path_cost = algos.path_length(self.known, vantage_to_target_path)


        vantage_path_cost_without_edge = 0
        target_path_cost_without_edge = 0
        vantage_to_target_cost_without_edge = 0
        

        for node in range(len(path_to_vantage) - 1):
            if  (path_to_vantage[node], path_to_vantage[node + 1]) in self.discovered_edges:
                continue
            deleted_edge_weight = self.known.edge_weight[path_to_vantage[node]][path_to_vantage[node + 1]]

            self.known.delete_edge(path_to_vantage[node], path_to_vantage[node + 1])
            cost = 0
            to_node_path_len = algos.path_length(self.known, algos.shortest_path(self.known, self.agent_pos[agent_num], path_to_vantage[node]))
            node_to_target_path_len = algos.path_length(self.known, algos.shortest_path(self.known, path_to_vantage[node], vantage_node))
            if to_node_path_len != -1 and node_to_target_path_len != -1:
                cost = to_node_path_len + node_to_target_path_len

            vantage_path_cost_without_edge += cost - vantage_path_cost
            self.known.add_edge(path_to_vantage[node], path_to_vantage[node + 1], deleted_edge_weight)

        for node in range(len(path_to_target) - 1):
            if  (path_to_target[node], path_to_target[node + 1]) in self.discovered_edges:
                continue
            deleted_edge_weight = self.known.edge_weight[path_to_target[node]][path_to_target[node + 1]]
            self.known.delete_edge(path_to_target[node], path_to_target[node + 1])
            cost = 0
            to_node_path_len = algos.path_length(self.known, algos.shortest_path(self.known, self.agent_pos[agent_num], path_to_target[node]))
            node_to_target_path_len = algos.path_length(self.known, algos.shortest_path(self.known, path_to_target[node], target_node))
            if to_node_path_len != -1 and node_to_target_path_len != -1:
                cost = to_node_path_len + node_to_target_path_len

            target_path_cost_without_edge += cost - target_path_cost
            self.known.add_edge(path_to_target[node], path_to_target[node + 1], deleted_edge_weight)
        for node in range(len(vantage_to_target_path) - 1):
            if  (vantage_to_target_path[node], vantage_to_target_path[node + 1]) in self.discovered_edges:
                continue
            deleted_edge_weight = self.known.edge_weight[vantage_to_target_path[node]][vantage_to_target_path[node + 1]]
            self.known.delete_edge(vantage_to_target_path[node], vantage_to_target_path[node + 1])
            if (vantage_to_target_path[node], vantage_to_target_path[node + 1]) not in self.visibility[vantage_node]:
                to_node_path_len = algos.path_length(self.known, algos.shortest_path(self.known, vantage_node, vantage_to_target_path[node]))
                node_to_target_path_len = algos.path_length(self.known, algos.shortest_path(self.known, vantage_to_target_path[node], target_node))
                if to_node_path_len != -1 and node_to_target_path_len != -1:
                    vantage_to_target_cost_without_edge += to_node_path_len + node_to_target_path_len - vantage_to_target_path_cost
                self.known.add_edge(vantage_to_target_path[node], vantage_to_target_path[node + 1], deleted_edge_weight)
            else:
                new_path_len = algos.path_length(self.known, algos.shortest_path(self.known, vantage_node, target_node))
                if new_path_len != -1:
                    vantage_to_target_cost_without_edge += new_path_len - vantage_to_target_path_cost
                self.known.add_edge(vantage_to_target_path[node], vantage_to_target_path[node + 1], deleted_edge_weight)

        # calculate cost decrease for other agents
        # NOTE: need to add check that the other agent(s) will reach the edge after the current agent reaches the vantage node
        other_agent_gain = 0
        for agent in range(self.num_agents):
            if agent == agent_num:
                continue
            if vantage_node in self.agent_path[agent]:
                other_agent_gain = float("-inf")
            path = self.agent_path[agent]
            for node in range(len(path) - 1):
                path_len = algos.path_length(self.known, path)
                if (path[node], path[node + 1]) not in self.discovered_edges and (path[node], path[node + 1]) in self.visibility[vantage_node]:
                    deleted_edge_weight = self.known.edge_weight[path[node]][path[node + 1]]
                    self.known.delete_edge(path[node], path[node + 1])
                    new_path_len = algos.path_length(self.known, algos.shortest_path(self.known, self.agent_pos[agent], path[-1]))

                    if new_path_len != -1:
                        other_agent_gain += new_path_len - path_len
                    self.known.add_edge(path[node], path[node + 1], deleted_edge_weight)


        vantage_cost = self.cd * (vantage_path_cost_without_edge + vantage_to_target_cost_without_edge - other_agent_gain) + vantage_path_cost + vantage_to_target_path_cost
        target_cost = self.cd * (target_path_cost_without_edge) + target_path_cost
        if (vantage_node == 8):
            print(f"agent pos: {self.agent_pos[agent_num]} vantage_node: {vantage_node} target: {target_cost} vantage: {vantage_cost}")
            print(f"go to vantage: {path_to_vantage + vantage_to_target_path[1:]}")
            print(f"go to target: {path_to_target}")
        if (vantage_cost <= target_cost):
            # print(f"go to vantage: {path_to_vantage + vantage_to_target_path[1:]}")
            return path_to_vantage + vantage_to_target_path[1:], vantage_cost
        else:
            # print(f"go to target: {path_to_target}")
            return path_to_target, target_cost
        
    def _update_positions(self) -> int:
        
        agents_at_node = []
        time_delta = min(self.known.edge_weight[self.agent_pos[agent]][self.agent_dest[agent]] - self.agent_progress[agent] for agent in range(self.num_agents))
        self.time += time_delta
        # print(f"time: {self.time}")
        self.agent_progress = [progress + time_delta for progress in self.agent_progress]
        for agent in range(self.num_agents):
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

    
    def _vantage_incentive(self, vantage_node: int) -> int:

        #sets the amount of potential edges to the amount of visible edges from the given vantage node
        potential_edges = len(self.visibility[vantage_node])

        #if the edge has already been discovered then we reduce the amount of potential edges

        vantage_path = algos.shortest_path(self.known, self.agent_pos[0], vantage_node)

        #returns the value of potental edges to discover/path length based on known graph
        path_length = algos.path_length(self.known, vantage_path)
        if path_length == 0:
            return 0
        return potential_edges/path_length