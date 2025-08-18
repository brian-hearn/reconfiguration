from helper_functions import *

# def count_mutual_neighbours_at_next_depth(meta_graph, depth_dict, part1, part2):
#     print('Counting mutual neighbours of the following partitions:')
#     print(part1)
#     print(part2)
#     depth1 = depth_dict.get(part1)
#     depth2 = depth_dict.get(part2)
#     print('Depth of partition 1: ' + str(depth1))
#     print('Depth of partition 2: ' + str(depth2))
#     # Step 1: Check if both partitions exist and have same depth
#     if depth1 is None or depth2 is None:
#         print("Error: One or both partitions not found in depth dictionary.")
#         return None
#     if depth1 != depth2:
#         print("Error: Specified partitions do not have the same depth.")
#         return None

#     d = depth1

#     # Step 2: Find neighbours of each
#     neigh1 = set(meta_graph.neighbors(part1))
#     neigh2 = set(meta_graph.neighbors(part2))

#     # Step 3: Mutual neighbours at depth d+1
#     mutual_next_depth = [n for n in (neigh1 & neigh2) if depth_dict.get(n) == d + 1]

#     # print(f"Depth of both partitions: {d}")
#     print(f"Number of mutual neighbours at depth {d+1}: {len(mutual_next_depth)}")
#     if mutual_next_depth:
#         print("Mutual neighbours:")
#         for node in mutual_next_depth:
#             print(" ", partition_to_label(node))

#     return len(mutual_next_depth), mutual_next_depth

# from itertools import combinations, product

# def count_mutual_neighbours_at_next_depth(meta_graph, depth_dict, partition_a, partition_b):
#     if partition_a not in meta_graph or partition_b not in meta_graph:
#         raise ValueError("One or both partitions not found in meta_graph.")

#     depth_a = depth_dict[partition_a]
#     depth_b = depth_dict[partition_b]

#     if depth_a != depth_b:
#         raise ValueError("Error: Specified partitions do not have the same depth")

#     next_depth = depth_a + 1

#     neighbours_a = {n for n in meta_graph.neighbors(partition_a) if depth_dict[n] == next_depth}
#     neighbours_b = {n for n in meta_graph.neighbors(partition_b) if depth_dict[n] == next_depth}

#     mutual = neighbours_a & neighbours_b
#     return len(mutual), mutual

# def get_mutual_neighbours_at_next_depth(meta_graph, depth_dict, partA, partB):
#     """Return the actual mutual neighbour partitions at the next depth."""
#     if partA not in meta_graph or partB not in meta_graph:
#         raise ValueError("One or both partitions not found in meta_graph.")

#     depthA = depth_dict[partA]
#     depthB = depth_dict[partB]
#     if depthA != depthB:
#         raise ValueError("Specified partitions do not have the same depth.")
#     d = depthA

#     neighA = [n for n in meta_graph.neighbors(partA) if depth_dict[n] == d + 1]
#     neighB = [n for n in meta_graph.neighbors(partB) if depth_dict[n] == d + 1]
#     return list(set(neighA) & set(neighB))

def mutual_neighbours_at_next_depth(meta_graph, depth_dict, P, Q):
    """
    Given two partitions P and Q, return the set of mutual neighbours 
    that lie at depth d+1, where d is the common depth of P and Q.
    """
    if P not in depth_dict or Q not in depth_dict:
        raise ValueError("One or both partitions not found in depth_dict")

    dP = depth_dict[P]
    dQ = depth_dict[Q]

    if dP != dQ:
        raise ValueError("Error: Specified partitions do not have the same depth")

    d = dP  # common depth

    # Neighbours of P and Q
    neigh_P = {nbr for nbr in meta_graph.neighbors(P) if depth_dict.get(nbr) == d+1}
    neigh_Q = {nbr for nbr in meta_graph.neighbors(Q) if depth_dict.get(nbr) == d+1}
    # print('Neighbours of P')
    # for neighbour in neigh_P:
    #     print(neighbour)
    # print('Neighbours of Q')
    # for neighbour in neigh_Q:
    #     print(neighbour)
    # print(neigh_Q)

    # Mutual neighbours
    mutual = neigh_P.intersection(neigh_Q)
    return mutual

def analyse_singleton_moves_for_vertex(i, meta_graph, depth_dict, vertices_to_move):
    start_partition = find_unique_depth_0_partition(depth_dict)
    if check_if_vertex_is_a_singleton(start_partition, i):
        singleton_moves = generate_singleton_moves(start_partition, vertices_to_move)
        singleton_moves = [normalize_partition(p) for p in singleton_moves]
        P_i = recognise_P_i(singleton_moves, i)
        
        # Step 3: For each P_j != P_i, compute mutual neighbours
        results = {}
        for P_j in singleton_moves:
            if P_j != P_i:
                print(f"\n=== Analysing pair (P_{i}, P_j) ===")
                res = mutual_neighbours_at_next_depth(
                    meta_graph, depth_dict, P_i, P_j
                )
                if res is None:
                    print("Skipping this pair due to depth mismatch or missing partition.")
                    continue
                count, mutuals = res
                results[P_j] = count

        return P_i, results


