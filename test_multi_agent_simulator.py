import graphs_test
# from simulators.alternating_simulator import MultiAgentSimulator
# from simulators.adopted_greedy_simulator import MultiAgentSimulator
from multi_agent_simulator import MultiAgentSimulator
from graph import Graph
from typing import List
import big_graph

def main():
    # sim = MultiAgentSimulator(graphs_test.multi_two_long_path_graph_known, graphs_test.multi_two_long_path_graph_unknown, graphs_test.multi_two_long_path_visibility, 1, graphs_test.multi_two_long_path_targets)
    # sim = MultiAgentSimulator(big_graph.big_graph_known, big_graph.big_graph_unknown, big_graph.big_graph_visibility, 2, big_graph.big_graph_targets)
    sim = MultiAgentSimulator(big_graph.big_graph_known, big_graph.big_graph_unknown, big_graph.big_graph_visibility, 1, [20])

    # sim.run_anakin_simulation()
    sim.run_simu()
    print("total time taken:", end=" ")
    print(sim.time)

main()