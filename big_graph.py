from graph import Graph, graph_dict


big_graph_known_dict: graph_dict = {
   "num_nodes": 22,
   "edges": [(0, 1, 17.0), (1, 0, 17.0), (1, 2, 6.0), (2, 1, 6.0), (2, 3, 4.0), (3, 2, 4.0), (3, 4, 8.0), (4, 3, 8.0), (0, 5, 18.0), (5, 0, 18.0),
             (2, 7, 2.0), (7, 2, 2.0), (4, 8, 7.0), (8, 4, 7.0), (5, 6, 12.0), (6, 5, 12.0), (6, 7, 5.0), (7, 6, 5.0), (7, 8, 4.0), (8, 7, 4.0), 
             (5, 9, 3.0), (9, 5, 3.0), (9, 12, 4.0), (12, 9, 4.0), (12, 14, 3.0), (14, 12, 3.0), (13, 0, 6.0), (0, 13, 6.0), (14, 18, 5.0), (18, 14, 5.0),
             (6, 15, 15.0), (15, 6, 15.0), (7, 10, 6.0), (10, 7, 6.0), (10, 16, 8.0), (16, 10, 8.0), (11, 17, 7.0), (17, 11, 7.0),
             (10, 11, 3.0), (11, 10, 3.0), (15, 16, 4.0), (16, 15, 4.0), (16, 17, 9.0), (17, 16, 9.0), (15, 19, 10.0), (19, 15, 10.0), 
             (16, 20, 1.0), (20, 16, 1.0), (17, 21, 3.0), (21, 17, 3.0), (19, 20, 6.0), (20, 19, 6.0), (20, 21, 5.0), (21, 20, 5.0)],
   "node_weight": [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 10, 0, 4, 9]
}
big_graph_known = Graph.from_dict(big_graph_known_dict)

big_graph_unknown_dict: graph_dict = {
   "num_nodes": 22,
   "edges": [(1, 2, 6.0), (2, 1, 6.0), (2, 3, 4.0), (3, 2, 4.0), (3, 4, 8.0), (4, 3, 8.0), (0, 5, 18.0), (5, 0, 18.0),
             (2, 7, 2.0), (7, 2, 2.0), (4, 8, 7.0), (8, 4, 7.0), (5, 6, 12.0), (6, 5, 12.0), (6, 7, 5.0), (7, 6, 5.0), 
             (5, 9, 3.0), (9, 5, 3.0), (9, 12, 4.0), (12, 9, 4.0), (12, 14, 3.0), (14, 12, 3.0), (13, 0, 6.0), (0, 13, 6.0), (14, 18, 5.0), (18, 14, 5.0),
             (6, 15, 15.0), (15, 6, 15.0), (10, 16, 8.0), (16, 10, 8.0),
             (10, 11, 3.0), (11, 10, 3.0), (15, 16, 4.0), (16, 15, 4.0), (16, 17, 9.0), (17, 16, 9.0), (15, 19, 10.0), (19, 15, 10.0), 
            (17, 21, 3.0), (21, 17, 3.0), (19, 20, 6.0), (20, 19, 6.0)],
   "node_weight": [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 10, 0, 4, 9]
}

big_graph_unknown = Graph.from_dict(big_graph_unknown_dict)

big_graph_visibility = [[(0, 1), (1, 0), (0, 5), (5, 0), (0, 13), (13, 0)],
                        [(0, 1), (1, 0), (0, 5), (5, 0), (1, 2), (2, 1), (2, 7), (7, 2), (6, 7), (7, 6), (5, 6), (6, 5)],
                        [(1, 2), (2, 1), (2, 7), (7, 2), (2, 3), (3, 2), (3, 4), (4, 3)],
                        [(2, 3), (3, 2), (3, 4), (4, 3), (4, 8), (8, 4)],
                        [(4, 8), (8, 4), (4, 3), (3, 4), (7, 8), (8, 7)],
                        [(5, 0), (0, 5), (5, 6), (6, 5), (6, 7), (7, 6), (5, 9), (9, 5), (9, 12), (12, 9)],
                        [(5, 6), (6, 5), (6, 7), (7, 6), (6, 15), (15, 6), (7, 2), (2, 7), (7, 8), (8, 7)],
                        [(7, 6), (6, 7), (2, 7), (7, 2), (7, 8), (8, 7), (7, 10), (10, 7), (10, 11), (11, 10), (10, 16), (16, 10)],
                        [(8, 7), (7, 8), (8, 4), (4, 8), (3, 4), (4, 3)],
                        [(9, 12), (12, 9), (12, 14), (14, 12), (14, 18), (18, 14), (0, 13), (13, 0)],
                        [(10, 11), (11, 10), (10, 16), (16, 10), (10, 7), (7, 10), (11, 17), (17, 11)],
                        [(11, 10), (10, 11), (11, 17), (17, 11), (16, 17), (17, 16), (10, 16), (16, 10)],
                        [(12, 14), (14, 12), (9, 12), (12, 9)],
                        [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3), (0, 5), (5, 0),
                        (2, 7), (7, 2), (4, 8), (8, 4), (5, 6), (6, 5), (6, 7), (7, 6), (7, 8), (8, 7), 
                        (5, 9), (9, 5), (9, 12), (12, 9), (12, 14), (14, 12), (13, 0), (0, 13), (14, 18), (18, 14),
                        (6, 15), (15, 6), (7, 10), (10, 7), (10, 16), (16, 10), (11, 17), (17, 11),
                        (10, 11), (11, 10), (15, 16), (16, 15), (16, 17), (17, 16), (15, 19), (19, 15), 
                        (16, 20), (20, 16), (17, 21), (21, 17), (19, 20), (20, 19), (20, 21), (21, 20)],
                        [(0, 13), (13, 0), (12, 14), (14, 12), (14, 15), (15, 14)],
                        [(15, 16), (16, 15), (15, 6), (6, 15), (15, 19), (19, 15), (20, 19), (19, 20), (16, 20), (20, 16)],
                        [(16, 10), (10, 16), (16, 17), (17, 16), (16, 20), (20, 16), (15, 16), (16, 15)],
                        [(17, 21), (21, 17), (17, 11), (11, 17), (17, 16), (16, 17), (10, 11), (11, 10), (10, 16), (16, 10)],
                        [(18, 14), (14, 18)],
                        [(19, 20), (20, 19), (19, 15), (15, 19), (15, 16), (16, 15), (16, 20), (20, 16)],
                        [(20, 16), (16, 20), (19, 20), (20, 19), (20, 21), (21, 20)],
                        [(21, 17), (17, 21), (21, 20), (20, 21)]]

big_graph_targets = [1, 11, 21, 18, 20]