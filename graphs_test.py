from graph import Graph, graph_dict


small_graph_known_dict: graph_dict = {
   "num_nodes": 9,
   "edges": [(0, 1, 7.0), (1, 0, 5.0), (1, 2, 8.0), (2, 1, 110.0), (2, 5, 5.0), (5, 2, 6.0), (5, 8, 4.0), (8, 5, 1.0), (8, 7, 11.0), (7, 8, 5.0),
   (7, 6, 7.0), (6, 7, 2.0), (6, 3, 3.0), (3, 6, 6.0), (3, 0, 2.0), (0, 3, 14.0), (3, 4, 11.0), (4, 5, 2.0), (4, 1, 9.0), (7, 4, 7.0)],
   "node_weight": [0, 0, 5, 0, 0, 21, 6, 16, 0]
}
small_graph_known = Graph.from_dict(small_graph_known_dict)


small_graph_unknown_dict: graph_dict = {
   "num_nodes": 9,
   "edges": [(0, 1, 7.0), (1, 0, 5.0), (2, 5, 5.0), (5, 2, 6.0), (5, 8, 4.0), (8, 5, 1.0), (8, 7, 11.0), (7, 8, 5.0),
   (7, 6, 7.0), (6, 7, 2.0), (3, 0, 2.0), (0, 3, 14.0), (3, 4, 11.0), (4, 5, 2.0), (4, 1, 9.0), (7, 4, 7.0)],
   "node_weight": [10, 13, 5, 7, 11, 21, 6, 16, 21]
}
small_graph_unknown = Graph.from_dict(small_graph_unknown_dict)


small_graph_visibility = [[(0,1),(1,0),(0,3),(3,0)],
               [(1,0),(0,1),(1,2),(2,1),(4,1)],
               [(2,1),(1,2),(2,5),(5,2)],
               [(3,0),(0,3),(3,6),(6,3),(3,4)],
               [(3,4),(4,1),(4,5),(7,4),(1,2),(2,1),(2,5),(5,2),(3,6),(6,3),(6,7),(7,6)],
               [(4,5),(2,5),(5,2),(5,8),(8,5)],
               [(3,6),(6,3),(6,7),(7,6)],
               [(6,7),(7,6),(7,4),(7,8),(8,7)],
               [(7,8),(8,7),(5,8),(8,5)]]

small_graph_targets = [2, 5, 6, 7]




single_vantage_graph_known_dict: graph_dict = {
   "num_nodes": 7,
   "edges": [(0, 1, 5.0), (1, 0, 5.0), (0, 2, 10.0), (2, 0, 10.0), (0, 4, 5.0), (4, 0, 5.0), (4, 5, 5.0), (5, 4, 5.0), (2, 1, 10.0), (1, 2, 10.0), (1, 5, 5.0), (5, 1, 5.0), 
      (2, 3, 10.0), (3, 2, 10.0), (1, 3, 5.0), (3, 1, 5.0), (5, 6, 5.0), (6, 5, 5.0), (3, 6, 5.0), (6, 3, 5.0)],
   "node_weight": [0, 0, 0, 1, 0, 0, 0]
}
single_vantage_graph_known = Graph.from_dict(single_vantage_graph_known_dict)


single_vantage_graph_unknown_dict: graph_dict = {
   "num_nodes": 7,
   "edges": [(0, 1, 5.0), (1, 0, 5.0), (0, 2, 10.0), (2, 0, 10.0), (4, 5, 5.0), (5, 4, 5.0), (2, 1, 10.0), (1, 2, 10.0), (1, 5, 5.0), (5, 1, 5.0), 
      (2, 3, 10.0), (3, 2, 10.0), (5, 6, 5.0), (6, 5, 5.0)],
   "node_weight": [0, 0, 0, 1, 0, 0, 0]
}
single_vantage_graph_unknown = Graph.from_dict(single_vantage_graph_unknown_dict)


single_vantage_graph_visibility = [[(0,1),(1,0),(0,2),(2,0), (0,4),(4,0)],
               [(1,0),(0,1),(1,2),(2,1),(1,3),(3,1), (1,5),(5,1)],
               [(2,1),(1,2),(2,0),(0,2), (2,3),(3,2), (1,5),(5,1), (5,6),(6,5), (3,6),(6,3)],
               [(3,2),(2,3),(3,6),(6,3),(3,1), (1,3)],
               [(0,4),(4,0),(4,5),(5,4)],
               [(4,5),(5,4),(5,1),(1,5),(5,6), (6,5)],
               [(3,6),(6,3),(5,6),(6,5)]]

single_vantage_graph_targets = [3]




two_long_path_known_dict: graph_dict = {
   "num_nodes": 11,
   "edges": [(0, 1, 1.0), (1, 0, 1.0), (1, 2, 1.0), (2, 1, 1.0), (2, 3, 2.0), (3, 2, 2.0), (3, 4, 1.0), (4, 3, 1.0), (4, 5, 1.0), (5, 4, 1.0), (0, 6, 1.0), (6, 0, 1.0), (6, 7, 1.0), (7, 6, 1.0), (7, 8, 1.0), (8, 7, 1.0), (8, 9, 1.0), (9, 8, 1.0), (9, 5, 1.0), (5, 9, 1.0), (0, 10, 1.0), (10, 0, 1.0)],
   "node_weight": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
}
two_long_path_graph_known = Graph.from_dict(two_long_path_known_dict)


two_long_path_unknown_dict: graph_dict = {
   "num_nodes": 11,
   "edges": [(0, 1, 1.0), (1, 0, 1.0), (1, 2, 1.0), (2, 1, 1.0), (2, 3, 2.0), (3, 2, 2.0), (3, 4, 1.0), (4, 3, 1.0), (4, 5, 1.0), (5, 4, 1.0), (0, 6, 1.0), (6, 0, 1.0), (6, 7, 1.0), (7, 6, 1.0), (7, 8, 1.0), (8, 7, 1.0), (9, 5, 1.0), (5, 9, 1.0), (0, 10, 1.0), (10, 0, 1.0)],
   "node_weight": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
}
two_long_path_graph_unknown = Graph.from_dict(two_long_path_unknown_dict)


two_long_path_visibility = [[(0,1),(1,0),(0,6),(6,0), (0,10),(10,0)],
               [(1,0),(0,1),(1,2),(2,1)],
               [(2,1),(1,2),(2,3),(3,2)],
               [(3,2),(2,3),(3,4),(4,3)],
               [(3,4),(4,3),(4,5),(5,4)],
               [(4,5),(5,4),(5,9),(9,5)],
               [(0,6),(6,0),(7,6),(6,7)],
               [(6,7),(7,6),(7,8),(8,7)],
               [(8,7),(7,8),(9,8),(8,9)],
               [(8,9),(9,8),(9,5),(5,9)],
               [(0,10),(10,0),(0,1),(1,0),(1,2),(2,1),(2,3),(3,2),(3,4),(4,3),(4,5),(5,4),(0,6),(6,0),(6,7),(7,6),(7,8),(8,7),(8,9),(9,8),(5,9),(9,5)]]

two_long_path_targets = [5, 8]




two_long_far_vantage_path_known_dict: graph_dict = {
   "num_nodes": 11,
   "edges": [(0, 1, 1.0), (1, 0, 1.0), (1, 2, 1.0), (2, 1, 1.0), (2, 3, 2.0), (3, 2, 2.0), (3, 4, 1.0), (4, 3, 1.0), (4, 5, 1.0), (5, 4, 1.0), (0, 6, 1.0), (6, 0, 1.0), (6, 7, 1.0), (7, 6, 1.0), (7, 8, 1.0), (8, 7, 1.0), (8, 9, 1.0), (9, 8, 1.0), (9, 5, 1.0), (5, 9, 1.0), (2, 10, 1.0), (10, 2, 1.0)],
   "node_weight": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
}
two_long_far_vantage_path_graph_known = Graph.from_dict(two_long_far_vantage_path_known_dict)


two_long_far_vantage_path_unknown_dict: graph_dict = {
   "num_nodes": 11,
   "edges": [(0, 1, 1.0), (1, 0, 1.0), (1, 2, 1.0), (2, 1, 1.0), (2, 3, 2.0), (3, 2, 2.0), (3, 4, 1.0), (4, 3, 1.0), (4, 5, 1.0), (5, 4, 1.0), (0, 6, 1.0), (6, 0, 1.0), (6, 7, 1.0), (7, 6, 1.0), (7, 8, 1.0), (8, 7, 1.0), (9, 5, 1.0), (5, 9, 1.0), (2, 10, 1.0), (10, 2, 1.0)],
   "node_weight": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
}
two_long_far_vantage_path_graph_unknown = Graph.from_dict(two_long_far_vantage_path_unknown_dict)


two_long_far_vantage_path_visibility = [[(0,1),(1,0),(0,6),(6,0)],
               [(1,0),(0,1),(1,2),(2,1)],
               [(2,1),(1,2),(2,3),(3,2),(2,10),(10,2)],
               [(3,2),(2,3),(3,4),(4,3)],
               [(3,4),(4,3),(4,5),(5,4)],
               [(4,5),(5,4),(5,9),(9,5)],
               [(0,6),(6,0),(7,6),(6,7)],
               [(6,7),(7,6),(7,8),(8,7)],
               [(8,7),(7,8),(9,8),(8,9)],
               [(8,9),(9,8),(9,5),(5,9)],
               [(2,10),(10,2),(0,1),(1,0),(1,2),(2,1),(2,3),(3,2),(3,4),(4,3),(4,5),(5,4),(0,6),(6,0),(6,7),(7,6),(7,8),(8,7),(8,9),(9,8),(5,9),(9,5)]]

two_long_far_vantage_path_targets = [5]

multi_two_long_path_known_dict: graph_dict = {
   "num_nodes": 11,
   "edges": [(0, 1, 5.0), (1, 0, 5.0), (1, 2, 5.0), (2, 1, 5.0), (2, 3, 10.0), (3, 2, 10.0), (3, 4, 5.0), (4, 3, 5.0), (4, 5, 5.0), (5, 4, 5.0), (0, 6, 5.0), (6, 0, 5.0), (6, 7, 5.0), (7, 6, 5.0), (7, 8, 5.0), (8, 7, 5.0), (8, 9, 5.0), (9, 8, 5.0), (9, 5, 5.0), (5, 9, 5.0), (0, 10, 1.0), (10, 0, 1.0)],
   "node_weight": [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
}
multi_two_long_path_graph_known = Graph.from_dict(multi_two_long_path_known_dict)


multi_two_long_path_unknown_dict: graph_dict = {
   "num_nodes": 11,
   "edges": [(0, 1, 5.0), (1, 0, 5.0), (1, 2, 5.0), (2, 1, 5.0), (2, 3, 10.0), (3, 2, 10.0), (3, 4, 5.0), (4, 3, 5.0), (4, 5, 5.0), (5, 4, 5.0), (0, 6, 5.0), (6, 0, 5.0), (6, 7, 5.0), (7, 6, 5.0), (7, 8, 5.0), (8, 7, 5.0), (9, 5, 5.0), (5, 9, 5.0), (0, 10, 1.0), (10, 0, 1.0)],
   "node_weight": [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
}
multi_two_long_path_graph_unknown = Graph.from_dict(multi_two_long_path_unknown_dict)


multi_two_long_path_visibility = [[(0,1),(1,0),(0,6),(6,0), (0,10),(10,0)],
               [(1,0),(0,1),(1,2),(2,1)],
               [(2,1),(1,2),(2,3),(3,2)],
               [(3,2),(2,3),(3,4),(4,3)],
               [(3,4),(4,3),(4,5),(5,4)],
               [(4,5),(5,4),(5,9),(9,5)],
               [(0,6),(6,0),(7,6),(6,7)],
               [(6,7),(7,6),(7,8),(8,7)],
               [(8,7),(7,8),(9,8),(8,9)],
               [(8,9),(9,8),(9,5),(5,9)],
               [(0,10),(10,0),(0,1),(1,0),(1,2),(2,1),(2,3),(3,2),(3,4),(4,3),(4,5),(5,4),(0,6),(6,0),(6,7),(7,6),(7,8),(8,7),(8,9),(9,8),(5,9),(9,5)]]

multi_two_long_path_targets = [5]