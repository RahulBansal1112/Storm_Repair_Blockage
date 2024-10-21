import sys
sys.path.append('/Users/rahulbansal/Documents/Storm_Repair_Blockage')

from graph import Graph, graph_dict
from algos import shortest_path

small_graph_known_dict: graph_dict = {
   "num_nodes": 9,
   "edges": [(0, 1, 7.0), (1, 0, 5.0), (1, 2, 8.0), (2, 1, 12.0), (2, 5, 5.0), (5, 2, 6.0), (5, 8, 4.0), (8, 5, 1.0), (8, 7, 11.0), (7, 8, 5.0),
   (7, 6, 7.0), (6, 7, 2.0), (6, 3, 3.0), (3, 6, 6.0), (3, 0, 2.0), (0, 3, 14.0), (3, 4, 11.0), (4, 5, 2.0), (4, 1, 9.0), (7, 4, 7.0)],
   "node_weight": [10, 13, 5, 7, 11, 21, 6, 16, 21]
}
small_graph_known = Graph.from_dict(small_graph_known_dict)

print(shortest_path(small_graph_known, 0, 5))

