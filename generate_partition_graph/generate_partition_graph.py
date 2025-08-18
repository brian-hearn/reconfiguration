from gpg_functions import *
from gpg_helper_functions import *
import networkx as nx
import json

# Specify Graph and Original Partition
# n = 25
# parts = [
#     {0, 1, 2, 3, 4},
#     {5, 6, 7, 8, 9},
#     {10, 11, 12, 13, 14},
#     {15, 16, 17, 18, 19},
#     {20, 21, 22, 23, 24}
# ]
# edges = []
# for i in range(len(parts)):
#     a = parts[i]
#     b = parts[(i + 1) % len(parts)]
#     for u in a:
#         for v in b:
#             if u != 0:
#                 edges.append((u, v))

n = 14
parts = [
    {0, 1, 2, 3},
    {4, 5, 6, 7},
    {8,9,10,11},
    {12,13}
]
edges = [(0,12),(4,12),(8,12),(1,13),(2,13),(3,13),(5,13),(6,13),(7,13),(9,13),(10,13),(11,13), (0,4),(0,5), (1,5), (1,7), (0,8), (0,9), (2,9), (2,10), (4,8), (4,10), (5,10), (6,9), (6,11), (7,10), (7,11)]
adj = build_adjacency_list(n, edges)
start_partition = normalize_partition(parts)

# Specify vertices which are allowed to move
vertices_to_move = [4,10,11,12,13]

# Specify depth from original partition
steps = 3

# Specify whether original partition should be displayed
show_original = False

all_partitions, depth_dict = find_partitions_within_steps(n, adj, start_partition, vertices_to_move, steps)
meta_graph = build_meta_graph(all_partitions, adj, n)

# Add depth attribute for Gephi
for node, depth in depth_dict.items():
    meta_graph.nodes[node]['depth'] = depth

visualize_graph_and_meta_graph(n, edges, start_partition, depth_dict, meta_graph, show_original=show_original)

# Save the meta_graph in GEXF format (works well with Gephi too)
nx.write_gexf(meta_graph, "data/meta_graph.gexf")
print("Meta graph saved to data/meta_graph.gexf")

# Save depth_dict as JSON with string keys
depth_dict_str_keys = {str(k): v for k, v in depth_dict.items()}
with open("data/depth_dict.json", "w") as f:
    json.dump(depth_dict_str_keys, f, indent=2)

with open("data/vertices_to_move.json", "w") as f:
    json.dump(vertices_to_move, f)
