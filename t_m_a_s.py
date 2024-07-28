import graphs_test
from m_a_s import MultiAgentSimulator
from graph import Graph
from typing import List
import big_graph

def main():
    # sim = MultiAgentSimulator(graphs_test.multi_two_long_path_graph_known, graphs_test.multi_two_long_path_graph_unknown, graphs_test.multi_two_long_path_visibility, 3, graphs_test.multi_two_long_path_targets)
    sim = MultiAgentSimulator(big_graph.big_graph_known, big_graph.big_graph_unknown, big_graph.big_graph_visibility, 1, big_graph.big_graph_targets)

    # sim.run_anakin_simulation()
    sim.run_simu()
    print("total time taken:", end=" ")
    print(sim.time)

main()