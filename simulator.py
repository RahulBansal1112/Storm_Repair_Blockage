from graph import Graph
from typing import List, Tuple

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
    time = 0
    visibility = []
    targets = [] #list of targets agents have to repair

    def __init__(self, known: Graph, unknown: Graph, visibility: List[List[Tuple]], num_agents: int, targets: List[int]):
        self.known = known
        self.visibility = visibility
        self.num_agents = num_agents
        self.targets = targets


    def start_sim(self, algorithm: str, start_nodes: List[int]):
        if(algorithm != "anakin" or algorithm != "R&R"):
            raise Exception("Selected algorithm is not valid")

        if(algorithm == "anakin"):
            #this is where we run anakin's algorithm with the graph, targets, and agents we have
        elif(algorithm == "R&R"):
            #this is where we run our algorithm when we make it


    def run_simulation(self):
        while(len(self.targets) > 0):
            self._update_positions()
            self._update_known_graph()
            # self._get_new_dest() # TODO
        

    def _update_positions(self) -> int:
        time_delta = min(self.known.edge_weight[self.agent_pos[agent]][self.agent_dest[agent]] - self.agent_progress[agent] for agent in range(self.num_agents))
        self.agent_progress = [progress + time_delta for progress in self.agent_progress]
        for agent in range(self.num_agents):
            if self.known.edge_weight[self.agent_pos[agent]][self.agent_dest[agent]] == self.agent_progress[agent]:
                self.agent_pos[agent] = self.agent_dest[agent]
                self.agent_dest[agent] = -1
                self.agent_progress[agent] = 0
        return time_delta
    
    def _update_known_graph(self) -> None:
        for agent in range(self.num_agents):
            if self.agent_progress[agent] == 0:
                visible_edges = self.visibility[self.agent_pos[agent]]
                for edge in visible_edges:
                    self.known.set_edge_weight(edge[0], edge[1], self.unknown.edge_weight[edge[0]][edge[1]]) # WILL PROBABLY NEED TO DELETE EDGE



    