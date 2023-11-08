from graph import Graph
from typing import List, Tuple

class Simulator:
    """Simulates multiple agents traversing a graph with multiple target

    Attributes:
        TODO
    """

    # agent_pos = []
    # agent_dest = []
    # agent_progress = []
    # num_agents = 0
    # known: Graph
    # time = 0
    # visibility = []

    def __init__(self, known: Graph, unknown: Graph, visibility: List[List[Tuple]], num_agents: int, targets: List[int]):
        pass

    def start_sim(self, algorithm: str, start_nodes: List[int]):
        pass

    def run_simulation(self):
        while(len(self.targets) > 0):
            self._update_positions()
            self._update_known_graph()
            # self._get_new_dest()
        

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



    