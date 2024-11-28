def create_graph(graph):
    """
    Create an adjacency matrix for a directed graph.

    Parameters:
    graph (dict): A dictionary representing the directed graph.

    Returns:
    list: The adjacency matrix of the graph.
    """
    # Detect all nodes (keys and values)
    all_nodes = set(graph.keys()) | set(node for neighbors in graph.values() for node in neighbors)
    vertices = sorted(all_nodes)  # Sort all nodes
    num_vertices = len(vertices)

    # Initialize the adjacency matrix with zeros
    adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    # Fill the adjacency matrix based on the edges in the graph
    for i, vertex in enumerate(vertices):
        # Use `graph.get(vertex, [])` to avoid KeyError for nodes without outgoing edges
        for neighbor in graph.get(vertex, []):
            j = vertices.index(neighbor)
            adj_matrix[i][j] = 1

    return adj_matrix
