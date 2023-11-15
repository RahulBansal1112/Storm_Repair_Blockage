import graphs_test
from simulator import Simulator
from graph import Graph
from typing import List

agent_1 = [0, 3, 4, 5, 8, 7, 6]
agent_2 = [0, 1, 0, 3, 4, 5, 2]

def get_next_agent_pos(known: Graph, current_pos: List[int]):
    global agent_1, agent_2

    if len(agent_1) >= 1 and current_pos[0] != agent_1[0]:
        agent_1 = agent_1[1:]
    if len(agent_2) >= 1 and current_pos[1] != agent_2[0]:
        agent_2 = agent_2[1:]
    return [agent_1[1] if len(agent_1) >= 2 else -1, agent_2[1] if len(agent_2) >= 2 else -1]

def main():

    sim = Simulator(graphs_test.small_graph_known, graphs_test.small_graph_unknown, graphs_test.small_graph_visibility, 2, graphs_test.small_graph_targets)
    sim.start_sim(get_next_agent_pos, [0, 0])
    print("total time taken:", end=" ")
    print(sim.time)

main()