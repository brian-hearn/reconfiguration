from generate_partition_graph import *
from counting_functions import *

# Specify Graph and Original Partition
n = 21
parts = [
    {0, 1, 2},
    {3, 4, 5},
    {6, 7, 8},
    {9, 10, 11},
    {12, 13, 14},
    {15, 16, 17},
    (18, 19, 20)
]
edges = []
for i in range(len(parts)):
    a = parts[i]
    b = parts[(i + 1) % len(parts)]
    for u in a:
        for v in b:
            if u != 0:
                edges.append((u, v))

adj = build_adjacency_list(n, edges)
start_partition = normalize_partition(parts)

# Specify vertices which are allowed to move
vertices_to_move = [0, 1, 2]

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

nx.write_gexf(meta_graph, "meta_graph.gexf")
print("Meta graph saved to meta_graph.gexf — open in Gephi to explore.")


# # Example: pick two partitions from all_partitions
# part1 = list(all_partitions)[8]  # just picking some index for example
# part2 = list(all_partitions)[6]  # another index for example

part1 = normalize_partition([
    {0},
    {1},
    {2, 3, 4, 5},
    {6, 7, 8},
    {9, 10, 11},
    {12, 13, 14},
    {15, 16, 17},
    (18, 19, 20)
])

part2 = normalize_partition([
    {0,1},
    {2},
    {3, 4, 5},
    {6, 7, 8},
    {9, 10, 11},
    {12, 13, 14},
    {15, 16, 17},
    (18, 19, 20)
])

# count_mutual_neighbours_at_next_depth_old(
#     meta_graph=meta_graph,
#     depth_dict=depth_dict,
#     part1=part1,
#     part2=part2
# )

res = advanced_three_level_search(meta_graph, depth_dict, special_vertex=0)

print(res)
