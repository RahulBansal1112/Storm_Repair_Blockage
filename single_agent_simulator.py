import graph
from graph import Graph
from graphs_test import small_graph_known, small_graph_unknown, small_graph_visibility
from typing import List, Tuple, Callable, Set
import algos

import time

class SingleAgentSimulator:
    """Simulates single agent traversing a graph with multiple target

    Attributes:
        TODO
    """

    # you can initialize these if you want
    agent_pos = [] # current agent positions
    agent_dest = [] # next node each agent is traveling towards
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

    def __init__(self, known: graph.Graph, unknown: graph.Graph, visibility: List[List[Tuple]], num_agents: int, targets: List[int]):
        self.known = known
        self.unknown = unknown
        self.visibility = visibility
        self.num_agents = num_agents
        self.targets = set(targets)
        self.agent_pos = [0] * num_agents
        self.agent_dest = [0] * num_agents
        self.agent_progress = [0] * num_agents
        print(known.num_nodes)
        

    # algorithm: function(known graph: Graph, current agent positions: List[int])
    def start_sim(self, algorithm: str, start_nodes: List[int]):
        self.algorithm = algorithm
        # if(algorithm != "anakin" or algorithm != "R&R"):
        #     raise Exception("Selected algorithm is not valid")
        self.agent_pos = start_nodes
        self.agent_progress = [0] * self.num_agents

        # if(algorithm == "anakin"):
        #     #this is where we run anakin's algorithm with the graph, targets, and agents we have
        #     pass
        # elif(algorithm == "R&R"):
        #     #this is where we run our algorithm when we make it
        #     pass
        self._get_new_dest()
        self.run_anakin_simulation()
        # self.run_simu()

    def _get_new_dest(self):
        self.agent_path[0] = algos.brute_force_mwlp(self.known, self.agent_pos[0]) 
        self.agent_dest = self.algorithm(self.known, self.agent_pos)


    def run_anakin_simulation(self):
        while(len(self.targets) > 0):
            print("curr pos:", end=" ")
            print(self.agent_pos)
            #take in account visibility and update graph known graph nodes
            self._update_known_graph()
            
            #create an adjacency list of nodes for our incomplete known graph
            shortest_known_paths = algos.floyd_warshall(self.known)
            #create graph that is a complete version of known graph
            small_complete_known_graph_dict: graph.graph_dict = {
                "num_nodes": self.known.num_nodes,
                "edges": [],
                "node_weight": self.known.node_weight
            }
            
            small_complete_known_graph = Graph.from_dict(small_complete_known_graph_dict)
            for start_node in range (self.known.num_nodes):
                for end_node in range (self.known.num_nodes):
                    small_complete_known_graph.add_edge(start_node, end_node, shortest_known_paths[start_node][end_node])

            # for start_node in range (len(shortest_known_paths)):
            #     for end_node in range (start_node):
            #         small_complete_known_graph.add_edge(start_node, end_node, small_complete_known_graph.edge_weight[start_node][end_node])
                    
            #create new path of agent based on complete graph
            tempagentpath = algos.greedy(small_complete_known_graph, [self.agent_pos[0]])
            
            """
            this path does not take into account the in between steps to get from each node
            (e.g. goes from New York to LA without stopping at Chicago)
            we find the inbetween path which consists of all the individual steps between the nodes
            this becomes our agent path
            """
            inbetweenpath = []
            for node in range(len(tempagentpath) - 1):
                inbetweenpath += algos.shortest_path(self.known, tempagentpath[node], tempagentpath[node + 1])
                if node != len(tempagentpath) - 2:
                    inbetweenpath.pop() #pop so we dont have a repeat of nodes
            self.agent_path[0] = inbetweenpath
            print("agent path:", end=" ")
            print(self.agent_path[0])
            self.agent_dest[0] = self.agent_path[0][1]
           
           
            #update agent position
            #update time taken
            self._update_positions()

            #remove target from target list if agent has visited
            print(self.targets)
            if self.agent_pos[0] in self.targets:
                self.known.set_node_weight(self.agent_pos[0], 0)
                self.targets.remove(self.agent_pos[0])
            
    
        
    def run_simu(self):
        #TODO
        ## use anakins method to create initial path!!!!
         while(len(self.targets) > 0):
        #update known graph
            start_time = time.time()

            print("agent pos: ", end=' ')
            print(self.agent_pos[0])
            self._update_known_graph()

            print("update graph: ", end = ' ')
            update_time = time.time()
            print(update_time - start_time)
            print("targets: ", end = ' ')
            print(self.targets)

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

            print("floyd_warshall: ", end = ' ')
            floyd_time = time.time()
            print(floyd_time - update_time)

            target_path = algos.greedy(small_complete_known_graph, [self.agent_pos[0]])

            print("anakin find path: ", end = ' ')
            mwlp_time = time.time()
            print(mwlp_time - floyd_time)


        #init cd
            print("cd: ", end = ' ')
            print(self.cd)
            # self.cd = self.broken_count/self.discovered_count
            # print("cd: ", end= ' ')
            # print(self.cd)

        #init vantage node and target node
            # may use an incentive function in the future, but right now we're checking every node
            # vantage_node = 0 
            # vantage_incentive = self._vantage_incentive(0)

            # for node in range(self.known.num_nodes):
            #     if (self._vantage_incentive(node) > vantage_incentive):
            #         vantage_incentive = self._vantage_incentive(node)
            #         vantage_node = node
            for node in target_path:
                if node in self.targets:
                    target_node = node
                    break
            # target_node = target_path[1]

        #find path based on equation
            min_path_cost = float('inf')
            for vantage_node in range(self.known.num_nodes):
                if (vantage_node == self.agent_pos[0]):
                    continue
                path, path_cost = self.vantage_vs_target(vantage_node, target_node)
                if path_cost < min_path_cost:
                    self.agent_path[0] = path
                    self.agent_dest[0] = self.agent_path[0][1]

            print("find best vantage point: ", end = ' ')
            vantage_time = time.time()
            print(vantage_time - mwlp_time)
        
        #update position and time
            self._update_positions()

            print("update agent positions: ", end = ' ')
            update_pos_time = time.time()
            print(update_pos_time - vantage_time)
            print()

            if self.agent_pos[0] in self.targets:
                self.known.set_node_weight(self.agent_pos[0], 0)
                self.targets.remove(self.agent_pos[0])

        
    def vantage_vs_target(self, vantage_node: int, target_node: int) -> list:

        #init 3 main paths for algorithm 
        path_to_vantage = algos.shortest_path(self.known, self.agent_pos[0], vantage_node)
        path_to_target = algos.shortest_path(self.known, self.agent_pos[0], target_node)
        vantage_to_target_path = algos.shortest_path(self.known, vantage_node, target_node)
        
        # print("agent pos: ", end=' ')
        # print(self.agent_pos[0])
        # print("vantage node: ", end=' ')
        # print(vantage_node)
        if (self.agent_pos[0] == 0 and vantage_node == 10):
            print("path to vantage", end=' ')
            print(path_to_vantage)
            print("path to target", end=' ')
            print(path_to_target)
            print("vantage to target", end=' ')
            print(vantage_to_target_path)


        #init path costs for 3 paths 
        vantage_path_cost = algos.path_length(self.known, path_to_vantage)
        target_path_cost = algos.path_length(self.known, path_to_target)
        vantage_to_target_path_cost = algos.path_length(self.known, vantage_to_target_path)
        
        #init path costs without edge
        vantage_path_cost_without_edge = 0
        target_path_cost_without_edge = 0
        vantage_to_target_cost_without_edge = 0
        
        """
        for each path:
        create a temporary graph that is the same as our known graph
        delete one edge in that graph that is in the planned path 
        calculate the cost of the path if the delete edge doesn't exist
        add that to the cost of the path without that edge

        """
        for node in range(len(path_to_vantage) - 1):
            # if (path_to_vantage[node], path_to_vantage[node + 1]) in self.discovered_edges and (path_to_vantage[node], path_to_vantage[node + 1]) not in self.broken_edges:
            #     # print("v exists")
            #     pass
            # else:
            #     break
            # temp_graph = self.known
            if ((path_to_vantage[node], path_to_vantage[node + 1]) in self.discovered_edges):
                # vantage_path_cost_without_edge += self.known.edge_weight[path_to_vantage[node]][path_to_vantage[node + 1]]
                continue
            deleted_edge_weight = self.known.edge_weight[path_to_vantage[node]][path_to_vantage[node + 1]]

            self.known.delete_edge(path_to_vantage[node], path_to_vantage[node + 1])
            cost = algos.path_length(self.known, algos.shortest_path(self.known, self.agent_pos[0], path_to_vantage[node])) + algos.path_length(self.known, algos.shortest_path(self.known, path_to_vantage[node], vantage_node))
            if (self.agent_pos[0] == 0 and vantage_node == 2):
                print("path to vantage cost: ", end=' ')
                print(cost)
            vantage_path_cost_without_edge += cost - vantage_path_cost
            self.known.add_edge(path_to_vantage[node], path_to_vantage[node + 1], deleted_edge_weight)

        for node in range(len(path_to_target) - 1):
            if (path_to_target[node], path_to_target[node + 1]) in self.discovered_edges:
                # vantage_path_cost_without_edge += self.known.edge_weight[path_to_target[node]][path_to_target[node + 1]]
                continue
            # else:
            #     break
            # temp_graph = self.known
            deleted_edge_weight = self.known.edge_weight[path_to_target[node]][path_to_target[node + 1]]
            self.known.delete_edge(path_to_target[node], path_to_target[node + 1])
            cost = algos.path_length(self.known, algos.shortest_path(self.known, self.agent_pos[0], path_to_target[node])) + algos.path_length(self.known, algos.shortest_path(self.known, path_to_target[node], target_node))
            if (self.agent_pos[0] == 0 and vantage_node == 2):
                print("cost: ", end=' ')
                print(cost)
            target_path_cost_without_edge += cost - target_path_cost
            self.known.add_edge(path_to_target[node], path_to_target[node + 1], deleted_edge_weight)
        for node in range(len(vantage_to_target_path) - 1):
            if (vantage_to_target_path[node], vantage_to_target_path[node + 1]) in self.discovered_edges:
                # vantage_to_target_cost_without_edge += self.known.edge_weight[vantage_to_target_path[node]][vantage_to_target_path[node + 1]]
                continue
            # else:
            #     break
            # temp_graph = self.known
            deleted_edge_weight = self.known.edge_weight[vantage_to_target_path[node]][vantage_to_target_path[node + 1]]
            self.known.delete_edge(vantage_to_target_path[node], vantage_to_target_path[node + 1])
            if (vantage_to_target_path[node], vantage_to_target_path[node + 1]) not in self.visibility[vantage_node]:
                vantage_to_target_cost_without_edge += algos.path_length(self.known, algos.shortest_path(self.known, vantage_node, vantage_to_target_path[node])) + algos.path_length(self.known, algos.shortest_path(self.known, vantage_to_target_path[node], target_node)) - vantage_to_target_path_cost
                self.known.add_edge(vantage_to_target_path[node], vantage_to_target_path[node + 1], deleted_edge_weight)
            else:
                vantage_to_target_cost_without_edge += algos.path_length(self.known, algos.shortest_path(self.known, vantage_node, target_node)) - vantage_to_target_path_cost
                self.known.add_edge(vantage_to_target_path[node], vantage_to_target_path[node + 1], deleted_edge_weight)
                # vantage_to_target_cost_without_edge += self.known.edge_weight[vantage_to_target_path[node]][vantage_to_target_path[node + 1]]
        if (self.agent_pos[0] == 0 and vantage_node == 10):
            print(target_path_cost_without_edge)
            print(vantage_path_cost_without_edge)
            print(vantage_to_target_cost_without_edge)
        vantage_cost = self.cd * (vantage_path_cost_without_edge + vantage_to_target_cost_without_edge) + vantage_path_cost + vantage_to_target_path_cost
        target_cost = self.cd * (target_path_cost_without_edge) + target_path_cost

        if (self.agent_pos[0] == 0 and vantage_node == 10):
            print("agent pos: ", end=' ')
            print(self.agent_pos[0])
            print("vantage node: ", end=' ')
            print(vantage_node)
            print("vantage_cost: ", end=' ')
            print(vantage_cost)
            print("target_cost: ", end=' ')
            print(target_cost)
            print()

        if (vantage_cost <= target_cost):
            # print("go to vantage")
            return path_to_vantage + vantage_to_target_path, vantage_cost
        else:
            # print("go to target")
            return path_to_target, target_cost

        

    def _update_positions(self) -> int:
        
        agents_at_node = []
        time_delta = min(self.known.edge_weight[self.agent_pos[agent]][self.agent_dest[agent]] - self.agent_progress[agent] for agent in range(self.num_agents))
        self.time += time_delta
        self.agent_progress = [progress + time_delta for progress in self.agent_progress]
        for agent in range(self.num_agents):
            if self.known.edge_weight[self.agent_pos[agent]][self.agent_dest[agent]] == self.agent_progress[agent]:
                self.agent_pos[agent] = self.agent_dest[agent]
                self.agent_dest[agent] = -1
                self.agent_progress[agent] = 0
                agents_at_node.append(agent)
        return agents_at_node
    
    
        
    
    def _update_known_graph(self) -> None:
        
        #add visible edges from visibility to our list of discovered edges
        for edges in self.visibility[self.agent_pos[0]]:
            self.discovered_edges.append(edges)
        # print("agent pos in update:", end=' ')
        # print(self.agent_pos[0])
        self.visibility[self.agent_pos[0]] = []
        # print(self.visibility)
        # print("targets:", end=' ')
        # print(self.targets)
        # print("adjacency", end=' ')
        # print(self.known.adjacen_list)
        # print("node weights", end=' ')
        # print(self.known.node_weight)
        
        #if the edge does not exist in our unknown graph delete it from known graph and add edge to list of broken edges
        # print("discovered edges:")
        # print(self.discovered_edges)
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
        

