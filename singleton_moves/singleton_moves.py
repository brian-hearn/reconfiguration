import networkx as nx
import json
from helper_functions import *
from counting_functions import *
import ast  # safe literal_eval for tuples

# Load the meta_graph
meta_graph = nx.read_gexf("data/meta_graph.gexf")
meta_graph = convert_node_strings_to_tuples(meta_graph)


with open("data/depth_dict.json", "r") as f:
    depth_dict_raw = json.load(f)

# Convert string keys back into tuples
depth_dict = {ast.literal_eval(k): v for k, v in depth_dict_raw.items()}

with open("data/vertices_to_move.json", "r") as f:
    vertices_to_move = json.load(f)

print("Meta graph has", meta_graph.number_of_nodes(), "nodes and", meta_graph.number_of_edges(), "edges.")
# print("Depth dict keys:", list(depth_dict.keys())[:5], "...")
# print("Depth dict keys:")
# for key in depth_dict.keys():
#     print(key)

start_partition = find_unique_depth_0_partition(depth_dict)
print(f"Depth-0 partition:\n{start_partition}")

# if check_if_vertex_is_a_singleton(start_partition, i):
singleton_moves = generate_singleton_moves(start_partition, vertices_to_move)
singleton_moves = [normalize_partition(p) for p in singleton_moves]
print(f"Singleton moves:\n{singleton_moves}")
i = 0
P_i = recognise_P_i(singleton_moves, i)
print(f"P_i:\n{P_i}")
# j = 1
# P_j = recognise_P_i(singleton_moves, j)
# print(f"P_j:\n{P_j}")

# mutual_neighbours = mutual_neighbours_at_next_depth(meta_graph, depth_dict, P_i, P_j)


mutual_neighbours_dict = {}
for partition in singleton_moves:
    if partition != P_i:
        print(f"Analysing {partition} and {P_i}")
        mutual_neighbours_dict[partition] = mutual_neighbours_at_next_depth(meta_graph, depth_dict, P_i, partition)
        print('Mutual Neighbours:')
        for neighbour in mutual_neighbours_dict[partition]:
            print(neighbour)

from itertools import combinations, product

countlist = []

for key1, key2 in combinations(mutual_neighbours_dict, 2):  # all unique key pairs
    print('------------ KEYS ------------')
    print('Key 1')
    print(key1)
    print('Key 2')
    print(key2)
    for a, b in product(mutual_neighbours_dict[key1], mutual_neighbours_dict[key2]):
        print('Analysing:')
        print(a)
        print(b)
        print('Mutual neighbours:')
        mutual_neighbours = mutual_neighbours_at_next_depth(meta_graph, depth_dict, a, b)
        for neighbour in mutual_neighbours:
            print(neighbour)
        print('---')
        countlist.append(len(mutual_neighbours))

print(countlist)