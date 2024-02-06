from graph import Graph, graph_dict
from graphs_test import small_graph_known, small_graph_unknown
from typing import List, Tuple, Callable, Set
from algos import floyd_warshall, brute_force_mwlp

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
    targets: Set[int] #list of targets agents have to repair
    algorithm: Callable[[Graph, List[int]], List[int]]
    discovered = visibility.len()
    broken = 0
    cd = 1

    def __init__(self, known: Graph, unknown: Graph, visibility: List[List[Tuple]], num_agents: int, targets: List[int]):
        self.known = known
        self.unknown = unknown
        self.visibility = visibility
        self.num_agents = num_agents
        self.targets = set(targets)
        

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
        self.run_simulation()

    def _get_new_dest(self):
        self.agent_path[0] = brute_force_mwlp(self.known, self.agent_pos[0]) 
        self.agent_dest = self.algorithm(self.known, self.agent_pos)


    def run_anakin_simulation(self):
        print("curr pos:", end=" ")
        print(self.agent_pos)
        
        while(len(self.targets) > 0):
            """
            shortest_known_paths = algos.floyd_warshall(known)
            small_complete_known_graph: graph_dict = {
                "num_nodes": known.num_nodes,
                "edges": [],
                "node_weight": known.node_weight
            }
            for start_node in range (small_complete_known_graph.length):
                for end_node in range (start_node.length):
                    small_complete_known_graph.edges += [start_node, end_node, small_complete_known_graph[start_node][end_node]]
            
        
            
            self._update_positions()
            self._update_known_graph()
            self._get_new_dest()
            print("curr pos:", end=" ")
            print(self.agent_pos)
            """
            #create complete graph from given info
            shortest_known_paths = floyd_warshall(self.known)
            small_complete_known_graph: graph_dict = {
                "num_nodes": self.known.num_nodes,
                "edges": [],
                "node_weight": self.known.node_weight
            }
            for start_node in range (small_complete_known_graph.length):
                for end_node in range (start_node.length):
                    small_complete_known_graph.edges += [start_node, end_node, small_complete_known_graph[start_node][end_node]]
           
            #create new path of agent
            for agent in range(self.num_agents):
                self.agent_path[agent] = brute_force_mwlp(small_complete_known_graph, self.agent_pos[agent])
                self.agent_dest[agent] = self.agent_path[agent][1]
            
            #update agent position
            #update time taken
            self._update_positions()
            
            
            #take in account visibility and update graph known graph nodes
            self._update_known_graph()
            
            #NOTE: Graphs known and known complete will be stored as seperate so we can properly update edges between individual nodes
        
    def run_simu(self):
        #TODO
        ## use anakins method to create initial path!!!!

        #update known graph
        self._update_known_graph()

         #create complete graph from given info
        shortest_known_paths = floyd_warshall(self.known)
        small_complete_known_graph: graph_dict = {
            "num_nodes": self.known.num_nodes,
            "edges": [],
            "node_weight": self.known.node_weight
        }
        for start_node in range (small_complete_known_graph.length):
            for end_node in range (start_node.length):
                small_complete_known_graph.edges += [start_node, end_node, small_complete_known_graph[start_node][end_node]]
        #complete known graph will be used to access shortest path between nodes, however when traversing, we will use the incomplete graph


        #init cd
        cd = self.broken/self.discovered

        #init vantage node and target node
        vantage_node = 1
        target_node = 1

        #find path based on equation
        go_to_vantage = self.vantage_vs_target(vantage_node, target_node)

        if(go_to_vantage):
            self.agent_path[0] = [1,2]
            agent_dest = self.agent_path[0][1]
        else:
            self.agent_path[0] = [1,3]
        
        #update position and time
        self._update_positions()
        
    def vantage_vs_target(vantage_node: int, target_node: int) -> bool:
        #if true, vantage
        #if false, target
        print("help")
        vantage_path = 1
        target_path = 1
        vantage_to_target_path = 1

        vantage_cost = self.cd * -1 * (vantage_path + vantage_to_target_path) + vantage_path + vantage_to_target_path
        target_cost = self.cd * -1 * (target_path) + target_path

        if (vantage_cost > target_cost):
            return True
        else:
            return False

        

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
        """
        for agent in range(self.num_agents):
            if self.agent_pos[agent] in self.targets:
                self.targets.remove(self.agent_pos[agent])
            if self.agent_progress[agent] == 0:
                visible_edges = self.visibility[self.agent_pos[agent]]
                matches = false
                for assumed_edge in known.edges:
                    for known_edge in visible_edges:
                        if known_edge == assumed.edge:
                            matches = true
                    if !matches:
        """
    
        
