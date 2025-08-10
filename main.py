import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def normalize_partition(parts):
    # Sort parts by their smallest element to have canonical form
    sorted_parts = [tuple(sorted(p)) for p in parts]
    sorted_parts.sort(key=lambda x: x[0] if x else -1)
    return tuple(sorted_parts)

def build_adjacency_list(n, edges):
    adj = [[] for _ in range(n)]
    for u,v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def find_neighbour_partitions(n, adj, partition, vertices_to_move):
    parts = [set(p) for p in partition]
    neighbours = set()
    for v in vertices_to_move:
        # Find which part v belongs to
        idx_v = next(i for i, p in enumerate(parts) if v in p)
        # Try moving v to other parts without neighbours of v
        for i, p in enumerate(parts):
            if i == idx_v:
                continue
            if all(neigh not in p for neigh in adj[v]):
                new_parts = [set(x) for x in parts]
                new_parts[idx_v].remove(v)
                new_parts[i].add(v)
                # Remove empty parts
                new_parts = [p for p in new_parts if p]
                neighbours.add(normalize_partition(new_parts))
        # Also consider putting v alone if current part size > 1
        if len(parts[idx_v]) > 1:
            new_parts = [set(x) for x in parts]
            new_parts[idx_v].remove(v)
            new_parts.append({v})
            neighbours.add(normalize_partition(new_parts))
    return neighbours

def find_partitions_within_steps(n, adj, start_partition, vertices_to_move, steps):
    visited = {start_partition: 0}
    queue = deque([start_partition])

    while queue:
        current = queue.popleft()
        depth = visited[current]
        if depth == steps:
            continue
        new_partitions = find_neighbour_partitions(n, adj, current, vertices_to_move)
        for p in new_partitions:
            if p not in visited:
                visited[p] = depth + 1
                queue.append(p)
    return set(visited.keys()), visited

def build_meta_graph(all_partitions, adj, n):
    G = nx.Graph()
    partitions_list = list(all_partitions)
    for p in partitions_list:
        G.add_node(p)
    for i, A in enumerate(partitions_list):
        for j in range(i + 1, len(partitions_list)):
            B = partitions_list[j]
            # Check all vertices (0..n-1), not just vertices_to_move
            for v in range(n):
                if B in find_neighbour_partitions(n, adj, A, [v]):
                    G.add_edge(A, B)
                    break
    return G

def partition_to_label(partition):
    # Format partition nicely as string like: {0,1,2} | {3,4,5} | ...
    return " | ".join("{" + ",".join(str(x) for x in sorted(p)) + "}" for p in partition)

def visualize_graph_and_meta_graph(n, edges, start_partition, all_partitions, depth_dict, meta_graph, show_original=True):
    plt.figure(figsize=(16,7))

    # Original graph plot
    ax1 = plt.subplot(121)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', ax=ax1)
    ax1.set_title("Original Graph")

    # Meta graph plot
    ax2 = plt.subplot(122)
    meta_to_draw = meta_graph.copy()
    depth_for_draw = depth_dict.copy()

    if not show_original:
        if start_partition in meta_to_draw:
            meta_to_draw.remove_node(start_partition)
            depth_for_draw.pop(start_partition, None)

    pos_meta = nx.spring_layout(meta_to_draw, seed=42)
    depths = [depth_for_draw.get(node, 0) for node in meta_to_draw.nodes()]
    cmap = plt.cm.viridis
    colors = [cmap(d / max(depths) if max(depths) > 0 else 0) for d in depths]

    labels = {node: partition_to_label(node) for node in meta_to_draw.nodes()}

    nx.draw(meta_to_draw, pos_meta, with_labels=False, node_color=colors, edge_color='gray', node_size=500, ax=ax2)
    nx.draw_networkx_labels(meta_to_draw, pos_meta, labels=labels, font_size=7, ax=ax2)

    if show_original and start_partition in meta_to_draw:
        nx.draw_networkx_nodes(meta_to_draw, pos_meta, nodelist=[start_partition], node_color='red', node_size=700, ax=ax2)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=max(depths) if max(depths) > 0 else 1))
    sm.set_array([])
    plt.colorbar(sm, ax=ax2, fraction=0.046, pad=0.04).set_label("Distance from original partition")

    ax2.set_title("Meta Graph of Partitions")

    plt.tight_layout()
    plt.show()


def main():
    # Example graph on 15 vertices with parts of size 3
    n = 21
    parts = [
        {0,1},
        {2,3,4,5},
        {6,7,8},
        {9,10,11},
        {12,13,14},
        {15,16,17},
        (18,19,20)
    ]
    # Create edges to connect parts to make graph interesting
    edges = []
    # Fully connect consecutive parts (like a 5-part chain)
    for i in range(len(parts)):
        a = parts[i]
        b = parts[(i+1)%len(parts)]
        for u in a:
            for v in b:
                if u!= 0:
                    edges.append((u,v))
    adj = build_adjacency_list(n, edges)
    start_partition = normalize_partition(parts)

    # Control which vertices are allowed to move during BFS expansion (search)
    vertices_to_move = [0, 1, 2]
    steps = 1
    show_original = False

    all_partitions, depth_dict = find_partitions_within_steps(n, adj, start_partition, vertices_to_move, steps)

    meta_graph = build_meta_graph(all_partitions, adj, n)  # pass full n here to check all vertices for edges

    visualize_graph_and_meta_graph(n, edges, start_partition, all_partitions, depth_dict, meta_graph, show_original=show_original)

if __name__ == "__main__":
    main()
