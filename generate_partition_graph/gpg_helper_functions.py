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