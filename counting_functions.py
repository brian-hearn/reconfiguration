from generate_partition_graph import *

def count_mutual_neighbours_at_next_depth_old(meta_graph, depth_dict, part1, part2):
    print('Counting mutual neighbours of the following partitions:')
    print(part1)
    print(part2)
    depth1 = depth_dict.get(part1)
    depth2 = depth_dict.get(part2)
    print('Depth of partition 1: ' + str(depth1))
    print('Depth of partition 2: ' + str(depth2))
    # Step 1: Check if both partitions exist and have same depth
    if depth1 is None or depth2 is None:
        print("Error: One or both partitions not found in depth dictionary.")
        return None
    if depth1 != depth2:
        print("Error: Specified partitions do not have the same depth.")
        return None

    d = depth1

    # Step 2: Find neighbours of each
    neigh1 = set(meta_graph.neighbors(part1))
    neigh2 = set(meta_graph.neighbors(part2))

    # Step 3: Mutual neighbours at depth d+1
    mutual_next_depth = [n for n in (neigh1 & neigh2) if depth_dict.get(n) == d + 1]

    # print(f"Depth of both partitions: {d}")
    print(f"Number of mutual neighbours at depth {d+1}: {len(mutual_next_depth)}")
    if mutual_next_depth:
        print("Mutual neighbours:")
        for node in mutual_next_depth:
            print(" ", partition_to_label(node))

    return len(mutual_next_depth), mutual_next_depth

from itertools import combinations, product

def count_mutual_neighbours_at_next_depth(meta_graph, depth_dict, partition_a, partition_b):
    if partition_a not in meta_graph or partition_b not in meta_graph:
        raise ValueError("One or both partitions not found in meta_graph.")

    depth_a = depth_dict[partition_a]
    depth_b = depth_dict[partition_b]

    if depth_a != depth_b:
        raise ValueError("Error: Specified partitions do not have the same depth")

    next_depth = depth_a + 1

    neighbours_a = {n for n in meta_graph.neighbors(partition_a) if depth_dict[n] == next_depth}
    neighbours_b = {n for n in meta_graph.neighbors(partition_b) if depth_dict[n] == next_depth}

    mutual = neighbours_a & neighbours_b
    return len(mutual), mutual


from itertools import combinations

def advanced_three_level_search(meta_graph, depth_dict, special_vertex):
    """
    meta_graph: networkx graph of partitions
    depth_dict: dictionary mapping partition -> depth
    special_vertex: the vertex i as described
    """
    # Step 1: Identify the unique partition P of depth 0
    depth0_partitions = [p for p, d in depth_dict.items() if d == 0]
    if len(depth0_partitions) != 1:
        raise ValueError("There should be exactly one partition of depth 0")
    P = depth0_partitions[0]

    # Check if special_vertex is in a part of size 1
    for part in P:
        if special_vertex in part:
            if len(part) == 1:
                raise ValueError(f"Vertex {special_vertex} is in a singleton part in P, cannot proceed")
            break

    # Step 2: Generate all P_v by moving vertices to their own part
    candidate_P_vs = {}
    for part in P:
        if len(part) == 1:
            continue  # cannot move vertices already in singleton parts
        for v in part:
            if v == special_vertex:
                continue
            new_parts = [set(p) for p in P]
            # Remove v from its current part
            for np in new_parts:
                if v in np:
                    np.remove(v)
                    break
            new_parts.append({v})
            # Remove empty parts
            new_parts = [p for p in new_parts if p]
            P_v = tuple(tuple(sorted(p)) for p in new_parts)
            candidate_P_vs[v] = normalize_partition(P_v)

    # Filter out any P_v not in meta_graph and skip duplicates or P_i
    P_i_parts = [set(p) for p in P]
    for np in P_i_parts:
        if special_vertex in np:
            break
    P_i = P  # original partition
    P_vs = {}
    for v, P_v in candidate_P_vs.items():
        if P_v in meta_graph and P_v != P_i:
            P_vs[v] = P_v

    if P_i not in meta_graph:
        raise ValueError("P_i (special vertex's partition) not found in meta_graph")

    # Step 3: S = all vertices for which we obtained P_v, excluding special_vertex
    S = list(P_vs.keys())

    # Step 4: Compute results for all pairs (u,v) from S
    output = []
    for u, v in combinations(S, 2):
        P_u = P_vs[u]
        P_v_ = P_vs[v]

        # Use the count_mutual_neighbours_at_next_depth function
        X_u_count = count_mutual_neighbours_at_next_depth(meta_graph, depth_dict, P_i, P_u)
        X_v_count = count_mutual_neighbours_at_next_depth(meta_graph, depth_dict, P_i, P_v_)

        # Compute all mutual neighbours between elements of X_u and X_v
        mutual_counts = {}
        for a in X_u_count:
            for b in X_v_count:
                mutual_counts[(a,b)] = count_mutual_neighbours_at_next_depth(meta_graph, depth_dict, a, b)

        # Nicely format the result
        output.append({
            "pair": (u, v),
            "X_u_count": len(X_u_count),
            "X_v_count": len(X_v_count),
            "mutual_counts": mutual_counts
        })

    # Print nicely
    for entry in output:
        u, v = entry["pair"]
        print(f"Pair of vertices: ({u}, {v})")
        print(f"  Partitions at depth d+1 connected to P_{special_vertex} and P_{u}: {entry['X_u_count']}")
        print(f"  Partitions at depth d+1 connected to P_{special_vertex} and P_{v}: {entry['X_v_count']}")
        print("  Mutual neighbours between elements of X_u and X_v:")
        for (a,b), count in entry["mutual_counts"].items():
            print(f"    ({partition_to_label(a)}, {partition_to_label(b)}): {count}")
        print("-----------------------------------------------------")

    return output

def get_mutual_neighbours_at_next_depth(meta_graph, depth_dict, partA, partB):
    """Return the actual mutual neighbour partitions at the next depth."""
    if partA not in meta_graph or partB not in meta_graph:
        raise ValueError("One or both partitions not found in meta_graph.")

    depthA = depth_dict[partA]
    depthB = depth_dict[partB]
    if depthA != depthB:
        raise ValueError("Specified partitions do not have the same depth.")
    d = depthA

    neighA = [n for n in meta_graph.neighbors(partA) if depth_dict[n] == d + 1]
    neighB = [n for n in meta_graph.neighbors(partB) if depth_dict[n] == d + 1]
    return list(set(neighA) & set(neighB))




