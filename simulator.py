from graph import Graph
from typing import List, Tuple

class Simulator:
    """Simulates multiple agents traversing a graph with multiple target

    Attributes:
        TODO
    """

    

    def __init__(self, known: Graph, unknown: Graph, visibility: List[List[Tuple]], num_agents: int, targets: List[int]):
        pass

    def start_sim(self, algorithm: str, start_nodes: List[int]):
        pass

    def run_simulation(self):
        # while(True):
        #     _update_positions(self)
        pass

    def _update_positions(self) -> int:
        time_delta = min(self.known.edge_weight[self.agent_pos[agent]][self.agent_dest[agent]] - self.agent_progress[agent] for agent in range(self.num_agents))
        self.agent_progress = [progress + time_delta for progress in self.agent_progress]
        for agent in range(self.num_agents):
            if self.known.edge_weight[self.agent_pos[agent]][self.agent_dest[agent]] == self.agent_progress[agent]:
                self.agent_pos[agent] = self.agent_dest[agent]
                self.agent_dest[agent] = -1
                self.agent_progress[agent] = 0
        return time_delta


    