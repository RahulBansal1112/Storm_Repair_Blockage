import graphs_test
from multi_agent_simulator import MultiAgentSimulator
from graph import Graph
from typing import List

def main():
    sim = MultiAgentSimulator(graphs_test.multi_two_long_path_graph_known, graphs_test.multi_two_long_path_graph_unknown, graphs_test.multi_two_long_path_visibility, 3, graphs_test.multi_two_long_path_targets)
    sim.run_simu()
    print("total time taken:", end=" ")
    print(sim.time)

main()