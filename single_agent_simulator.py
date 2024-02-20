import graph
from graphs_test import small_graph_known, small_graph_unknown, small_graph_visibility
from typing import List, Tuple, Callable, Set
import algos

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
    known = small_graph_known
    unknown = small_graph_unknown
    time = 0
    visibility = []
    broken_edges = []
    targets: Set[int] #list of targets agents have to repair
    algorithm: Callable[[graph.Graph, List[int]], List[int]]
    discovered = 0
    broken = 0
    cd = 1

    def __init__(self, known: graph.Graph, unknown: graph.Graph, visibility: List[List[Tuple]], num_agents: int, targets: List[int]):
        self.known = known
        self.unknown = unknown
        self.visibility = visibility
        self.num_agents = num_agents
        self.targets = set(targets)
        self.agent_pos = [0] * num_agents
        

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
        self.run_simu()

    def _get_new_dest(self):
        self.agent_path[0] = algos.brute_force_mwlp(self.known, self.agent_pos[0]) 
        self.agent_dest = self.algorithm(self.known, self.agent_pos)


    def run_anakin_simulation(self):
        print("curr pos:", end=" ")
        print(self.agent_pos)
        
        while(len(self.targets) > 0):

            #take in account visibility and update graph known graph nodes
            self._update_known_graph()

            #create an adjacency list of nodes for our incomplete known graph
            shortest_known_paths = algos.floyd_warshall(self.known)
            #create graph that is a complete version of known graph
            small_complete_known_graph: graph.graph_dict = {
                "num_nodes": self.known.num_nodes,
                "edges": [],
                "node_weight": self.known.node_weight
            }
            for start_node in range (len(shortest_known_paths)):
                for end_node in range (len(start_node)):
                    small_complete_known_graph.add_edge(start_node, end_node, small_complete_known_graph[start_node][end_node])
                    
            #create new path of agent based on complete graph
            tempagentpath = algos.brute_force_mwlp(small_complete_known_graph, [self.agent_pos[0]])
            
            """
            this path does not take into account the in between steps to get from each node
            (e.g. goes from New York to LA without stopping at Chicago)
            we find the inbetween path which consists of all the individual steps between the nodes
            this becomes our agent path
            """
            inbetweenpath = []
            for node in range(len(tempagentpath) - 1):
                inbetweenpath += algos.shortest_path(self.known, tempagentpath[node], tempagentpath[node + 1])
                inbetweenpath.pop() #pop so we dont have a repeat of nodes
            self.agent_path[0] = inbetweenpath
            self.agent_dest[0] = self.agent_path[0][1]
           
           
            #update agent position
            #update time taken
            self._update_positions()

            #remove target from target list if agent has visited
            if self.agent_pos[0] in self.targets:
                self.targets.remove(self.agent_pos[0])
            
    
        
    def run_simu(self):
        #TODO
        ## use anakins method to create initial path!!!!
         while(len(self.targets) > 0):
        #update known graph
            self._update_known_graph()

            #create complete graph from given info
            shortest_known_paths = algos.floyd_warshall(self.known)
            small_complete_known_graph: graph.graph_dict = {
                "num_nodes": self.known.num_nodes,
                "edges": [],
                "node_weight": self.known.node_weight
            }
            for start_node in range (len(shortest_known_paths)):
                for end_node in range (len(start_node)):
                    small_complete_known_graph.add_edge(start_node, end_node, small_complete_known_graph[start_node][end_node])
        #complete known graph will be used to access shortest path between nodes, however when traversing, we will use the incomplete graph
            target_path = algos.brute_force_mwlp(small_complete_known_graph, [self.agent_pos[0]])


        #init cd
            cd = self.broken/self.discovered

        #init vantage node and target node
            vantage_node = 0 
            vantage_incentive = self._vantage_incentive(self, 0)

            for node in range(self.know.num_nodes):
                if (self._vantage_incentive(self, node) < vantage_incentive):
                    vantage_incentive = self._vantage_incentive(self, node)
                    vantage_node = node
            target_node = target_path[1]

        #find path based on equation
            self.agent_path[0] = self.vantage_vs_target(vantage_node, target_node)
            self.agent_dest[0] = self.agent_path[0][1]

        
        
        #update position and time
            self._update_positions()

            if self.agent_pos[0] in self.targets:
                self.targets.remove(self.agent_pos[0])

        
    def vantage_vs_target(self, vantage_node: int, target_node: int) -> list:
        print("help")

        #init 3 main paths for algorithm 
        path_to_vantage = algos.shortest_path(self.known, self.agent_pos[0], vantage_node)
        path_to_target = algos.shortest_path(self.known, self.agent_pos[0], target_node)
        vantage_to_target_path = algos.shortest_path(self.known, vantage_node, target_node)

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
            temp_graph = self.known
            graph.delete_edge(temp_graph, path_to_vantage[node], path_to_vantage[node + 1])
            vantage_path_cost_without_edge += algos.path_length(temp_graph, algos.shortest_path(temp_graph, self.agent_pos[0], vantage_node))
        for node in range(len(path_to_target) - 1):
            temp_graph = self.known
            graph.delete_edge(temp_graph, path_to_target[node], path_to_target[node + 1])
            target_path_cost_without_edge += algos.path_length(temp_graph, algos.shortest_path(temp_graph, self.agent_pos[0], vantage_node))
        for node in range(len(vantage_to_target_path) - 1):
            temp_graph = self.known
            graph.delete_edge(temp_graph, vantage_to_target_path[node], vantage_to_target_path[node + 1])
            vantage_to_target_cost_without_edge += algos.path_length(temp_graph, algos.shortest_path(temp_graph, self.agent_pos[0], vantage_node))
        
        vantage_cost = self.cd * (vantage_path_cost_without_edge - vantage_path_cost + vantage_to_target_cost_without_edge - vantage_to_target_path_cost) + vantage_path_cost + vantage_to_target_path_cost
        target_cost = self.cd * (target_path_cost_without_edge - target_path_cost) + target_path_cost

        if (vantage_cost > target_cost):
            return path_to_vantage + vantage_to_target_path
        else:
            return path_to_target

        

    def _update_positions(self) -> int:
        
        time_delta = min(self.known.edge_weight[self.agent_pos[agent]][self.agent_dest[agent]] - self.agent_progress[agent] for agent in range(self.num_agents))
        self.time += time_delta
        self.agent_progress = [progress + time_delta for progress in self.agent_progress]
        for agent in range(self.num_agents):
            if self.known.edge_weight[self.agent_pos[agent]][self.agent_dest[agent]] == self.agent_progress[agent]:
                self.agent_pos[agent] = self.agent_dest[agent]
                self.agent_dest[agent] = -1
                self.agent_progress[agent] = 0
        return time_delta
    
    
        
    
    def _update_known_graph(self) -> None:
        for edge in small_graph_visibility[self.agent_pos[0]]:
            self.visibility += edge
        for edge in self.visibility:
            print("edge 0:")
            print(edge)
            if (not self.unknown.contains_edge(edge[0], edge[1])):
                graph.delete_edge(self.known, edge[0], edge[1])
                self.broken_edges += edge
        self.broken_edges = list(dict.fromkeys(self.broken_edges))
        self.visibility = list(dict.fromkeys(self.visibility))
        self.broken = len(self.broken_edges)
        self.discovered = len(self.visibility)

    
    def _vantage_incentive(self, vantage_node: int) -> int:
        potential_edges = len(small_graph_visibility[vantage_node])
        for visible_edge in self.visibility: 
            for potential_edge in self.visibility:
                if visible_edge == potential_edge:
                    potential_edges -= 1
        vantage_path = algos.shortest_path(self.known, self.agent_pos[0], vantage_node)

        return potential_edges/algos.path_length(self.known, vantage_path)
        

