import networkx as nx
import matplotlib.pyplot as plt

def build_adjacency_list(n, edges):
    adj = [set() for _ in range(n)]
    for u,v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj

def normalize_partition(partition):
    # Normalize partition to tuple of frozensets, sorted
    return tuple(sorted((frozenset(p) for p in partition), key=lambda s: sorted(s)))

def pretty_partition(partition):
    return " | ".join("{" + ",".join(str(x) for x in sorted(p)) + "}" for p in partition)

def move_vertex_once(n, adj, partition, vertex):
    vertex_to_part = {}
    for i,p in enumerate(partition):
        for v in p:
            vertex_to_part[v] = i

    current_part_index = vertex_to_part[vertex]
    current_part = partition[current_part_index]

    # If vertex is in a singleton part, no moves possible
    if len(current_part) == 1:
        return set()

    result = set()

    # Try moving vertex to any part without neighbors of vertex
    for i, part in enumerate(partition):
        if i == current_part_index:
            continue
        if adj[vertex].isdisjoint(part):
            new_partition = [set(p) for p in partition]
            new_partition[current_part_index].remove(vertex)
            new_partition[i].add(vertex)
            new_partition = [p for p in new_partition if p]
            result.add(normalize_partition(new_partition))

    # Also consider moving vertex to a new singleton part
    new_partition = [set(p) for p in partition]
    new_partition[current_part_index].remove(vertex)
    if len(new_partition[current_part_index]) == 0:
        new_partition.pop(current_part_index)
    new_partition.append({vertex})
    result.add(normalize_partition(new_partition))

    return result

def build_meta_graph(partitions, n, adj, vertices_to_move):
    G = nx.Graph()
    partitions = list(partitions)
    G.add_nodes_from(partitions)
    partition_set = set(partitions)

    # For each partition, consider moves of vertices in vertices_to_move
    for A in partitions:
        for v in vertices_to_move:
            neighbors = move_vertex_once(n, adj, A, v)
            for B in neighbors:
                if B in partition_set:
                    G.add_edge(A, B)

    return G

def main():
    n = 15
    parts = [
        {0,1,2},
        {3,4,5},
        {6,7,8},
        {9,10,11},
        {12,13,14}
    ]

    # Construct edges between consecutive parts (cycle)
    edges = []
    for i in range(len(parts)):
        a = parts[i]
        b = parts[(i+1)%len(parts)]
        for u in a:
            for v in b:
                edges.append((u,v))

    adj = build_adjacency_list(n, edges)
    start_partition = normalize_partition(parts)

    vertices_to_move = [0, 1]

    # Find all partitions obtained by moving vertices in vertices_to_move once from start_partition
    all_new_partitions = set()
    for v in vertices_to_move:
        moved = move_vertex_once(n, adj, start_partition, v)
        all_new_partitions.update(moved)

    all_partitions = set([start_partition]) | all_new_partitions

    # Build meta graph using your new logic
    meta_graph = build_meta_graph(all_partitions, n, adj, vertices_to_move)

    # Print partitions info
    print("Original partition:")
    print(" ", pretty_partition(start_partition))
    print("\nPartitions obtained by moving exactly one vertex from vertices_to_move:")
    for i, p in enumerate(sorted(all_new_partitions), 1):
        print(f"{i}. {pretty_partition(p)}")

    print("\nMeta-graph edges:")
    for u,v in meta_graph.edges():
        print(f"{pretty_partition(u)} <--> {pretty_partition(v)}")

    # Visualize
    plt.figure(figsize=(14,6))

    # Original graph plot
    plt.subplot(1,2,1)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=700, font_size=10, edge_color='gray')
    plt.title("Original Graph")

    # Meta graph plot
    plt.subplot(1,2,2)
    pos_meta = nx.spring_layout(meta_graph, seed=42)
    node_colors = ["red" if node == start_partition else "green" for node in meta_graph.nodes()]
    node_sizes = [1400 if node == start_partition else 1000 for node in meta_graph.nodes()]
    labels = {node: pretty_partition(node) for node in meta_graph.nodes()}

    nx.draw(meta_graph, pos_meta, with_labels=False, node_color=node_colors, node_size=node_sizes, edge_color='black')
    nx.draw_networkx_labels(meta_graph, pos_meta, labels=labels, font_size=7)

    plt.title("Meta-graph (Partitions reachable by moving vertices 0 or 1)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
