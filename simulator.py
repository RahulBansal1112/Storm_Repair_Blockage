from graph import Graph, graph_dict
from typing import List, Tuple, Callable, Set
from algos import floyd_warshall

class Simulator:
    """Simulates multiple agents traversing a graph with multiple target

    Attributes:
        TODO
    """

    # you can initialize these if you want
    agent_pos = [] # current agent positions
    agent_dest = [] # next node each agent is traveling towards
    agent_progress = [] # how far along the path the agents are
    num_agents = 0
    known: Graph
    unknown: Graph
    time = 0
    visibility = []
    targets: Set[int] #list of targets agents have to repair
    algorithm: Callable[[Graph, List[int]], List[int]]

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
        self.agent_dest = self.algorithm(self.known, self.agent_pos)


    def run_simulation(self):
        print("curr pos:", end=" ")
        print(self.agent_pos)
        
        while(len(self.targets) > 0):
            shortest_known_paths = floyd_warshall(self.known)
            small_complete_known_graph: graph_dict = {
                "num_nodes": self.known.num_nodes,
                "edges": [],
                "node_weight": self.known.node_weight
            }
            for start_node in range (small_complete_known_graph["num_nodes"]):
                for end_node in range (start_node):
                    small_complete_known_graph["edges"] += [start_node, end_node, small_complete_known_graph[start_node][end_node]]
            


            self._update_positions()
            self._update_known_graph()
            self._get_new_dest()
            print("curr pos:", end=" ")
            print(self.agent_pos)
        

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
        for agent in range(self.num_agents):
            if self.agent_pos[agent] in self.targets:
                self.targets.remove(self.agent_pos[agent])
            if self.agent_progress[agent] == 0:
                visible_edges = self.visibility[self.agent_pos[agent]]
                for edge in visible_edges:
                    self.known.set_edge_weight(edge[0], edge[1], self.unknown.edge_weight[edge[0]][edge[1]]) # WILL PROBABLY NEED TO DELETE EDGE



    