import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from gpg_helper_functions import *

def find_neighbour_partitions(n, adj, partition, vertices_to_move):
    parts = [set(p) for p in partition]
    neighbours = set()
    for v in vertices_to_move:
        idx_v = next(i for i, p in enumerate(parts) if v in p)
        for i, p in enumerate(parts):
            if i == idx_v:
                continue
            if all(neigh not in p for neigh in adj[v]):
                new_parts = [set(x) for x in parts]
                new_parts[idx_v].remove(v)
                new_parts[i].add(v)
                new_parts = [p for p in new_parts if p]
                neighbours.add(normalize_partition(new_parts))
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
    partitions_list = [normalize_partition(partition) for partition in list(all_partitions)]
    for p in partitions_list:
        G.add_node(p)
    for i, A in enumerate(partitions_list):
        for j in range(i + 1, len(partitions_list)):
            B = partitions_list[j]
            for v in range(n):
                if B in find_neighbour_partitions(n, adj, A, [v]):
                    G.add_edge(A, B)
                    break
    return G

def partition_to_label(partition):
    return " | ".join("{" + ",".join(str(x) for x in sorted(p)) + "}" for p in partition)

def visualize_graph_and_meta_graph(n, edges, start_partition, depth_dict, meta_graph, show_original=True):
    plt.figure(figsize=(16, 7))

    ax1 = plt.subplot(121)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', ax=ax1)
    ax1.set_title("Original Graph")

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
    max_depth = max(depths) if depths else 1
    colors = [cmap(d / max_depth if max_depth > 0 else 0) for d in depths]

    labels = {node: partition_to_label(node) for node in meta_to_draw.nodes()}
    nx.draw(meta_to_draw, pos_meta, with_labels=False, node_color=colors, edge_color='gray', node_size=500, ax=ax2)
    nx.draw_networkx_labels(meta_to_draw, pos_meta, labels=labels, font_size=7, ax=ax2)

    if show_original and start_partition in meta_to_draw:
        nx.draw_networkx_nodes(meta_to_draw, pos_meta, nodelist=[start_partition], node_color='red', node_size=700, ax=ax2)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=max_depth))
    sm.set_array([])
    plt.colorbar(sm, ax=ax2, fraction=0.046, pad=0.04).set_label("Distance from original partition")

    ax2.set_title("Meta Graph of Partitions")

    plt.tight_layout()
    plt.savefig("data/plot.png")