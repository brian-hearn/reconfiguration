def normalize_partition(parts):
    sorted_parts = [tuple(sorted(p)) for p in parts]
    sorted_parts.sort(key=lambda x: x[0] if x else -1)
    return tuple(sorted_parts)

def build_adjacency_list(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

import networkx as nx
import ast

def convert_node_strings_to_tuples(graph):
    new_G = nx.Graph()
    for node in graph.nodes():
        # Convert the string representation to an actual tuple
        tuple_node = ast.literal_eval(node) if isinstance(node, str) else node
        new_G.add_node(tuple_node)

    # Copy edges, converting nodes to tuples as well
    for u, v in graph.edges():
        u_tuple = ast.literal_eval(u) if isinstance(u, str) else u
        v_tuple = ast.literal_eval(v) if isinstance(v, str) else v
        new_G.add_edge(u_tuple, v_tuple)

    # Replace the old graph
    return new_G

def generate_singleton_moves(parts, vertices_to_move):
    # Make sure parts are sets so we can remove vertices easily
    parts = [set(p) for p in parts]
    seen = set()

    for i, part in enumerate(parts):
        if len(part) >= 2:  # can only split off if part has size ≥ 2
            for v in part:
                if v in vertices_to_move:
                    new_parts = [set(p) for p in parts]
                    new_parts[i].remove(v)
                    new_parts.append({v})
                    # Remove empty parts
                    new_parts = [p for p in new_parts if p]
                    # Normalize to avoid duplicates
                    seen.add(normalize_partition(new_parts))
    return list(seen)

# Find the unique depth-0 partition
def find_unique_depth_0_partition(depth_dict):
    depth0_parts = [p for p, d in depth_dict.items() if d == 0]
    if len(depth0_parts) != 1:
        raise ValueError("Expected exactly one partition at depth 0.")
    start_partition = depth0_parts[0]  # normalized tuple-of-tuples
    return start_partition

# Checks if vertex i is in a part of size 1
def check_if_vertex_is_a_singleton(start_partition, i):
    for part in start_partition:
        if i in part:
            if len(part) == 1:
                raise ValueError(f"Vertex {i} is already in a singleton part.")
            return True
    raise ValueError(f"Vertex {i} not found in the depth-0 partition.")

# Find the unique partition which contains vertex i in a singleton part
def recognise_P_i(singleton_moves, i):
    P_i = None
    for p in singleton_moves:
        for part in p:
            if part == (i,):
                P_i = p
                return P_i
    if P_i is None:
        raise RuntimeError(f"Could not find singleton-move partition for vertex {i}.")
    print(f"\nPartition P_{i} (singleton move of vertex {i}):\n{P_i}\n")