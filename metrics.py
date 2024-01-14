import networkx as nx

# function that calculates the metrics given the resulting network
# degree distribution
# maximim connected components
# network diameter
# average path length
# clustering coefficient

def compute_metrics(G:nx.Graph):
    """
    Compute various metrics for a given graph.

    Parameters:
    G (nx.Graph): The input graph.

    Returns:
    tuple: A tuple containing the following metrics:
        - degreeCount (dict): A dictionary representing the degree distribution of the graph.
        - max_cc (list): The largest connected component of the graph.
        - diameter (int or None): The diameter of the graph if it is connected, otherwise None.
        - avg_path_length (float or None): The average path length of the graph if it is connected, otherwise None.
        - clustering_coefficient (float): The average clustering coefficient of the graph.
    """
    # Degree distribution
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = {}
    for degree in degree_sequence:
        if degree in degreeCount:
            degreeCount[degree] += 1
        else:
            degreeCount[degree] = 1
    # Maximum connected components
    max_cc = max(maximum_connected_components(G), key=len)
    
    # if the graph is not connected, the diameter and average path length cannot be computed
    if nx.is_connected(G):
        diameter = network_diameter(G)    # Network diameter
        avg_path_length = nx.average_shpath_length(G)# Average path length
    else:
        diameter = None
        avg_path_length = None
        print("Graph is not connected, cannot compute diameter")    
    
    # individual clustering coefficient
    node_clustering_coefficients = node_clustering_coefficient(G)
    # average clustering coefficient
    clustering_coefficient = sum(node_clustering_coefficients.values()) / len(node_clustering_coefficients)

    return degreeCount, max_cc, diameter, avg_path_length, clustering_coefficient


# function that calculates network diameter
def network_diameter(G: nx.Graph):
    """
    Calculates the diameter of a network graph.

    Parameters:
    G (nx.Graph): The network graph.

    Returns:
    int: The diameter of the network graph.
    """
    max_path_length = 0
    for source in G.nodes():
        distances = {node: float('inf') for node in G.nodes()}
        distances[source] = 0
        queue = [source]
        while queue:
            current_node = queue.pop(0)
            for neighbor in G.neighbors(current_node):
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[current_node] + 1
                    queue.append(neighbor)
                    max_path_length = max(max_path_length, distances[neighbor])
    return max_path_length


# function that calculates clustering coefficient for each node
def node_clustering_coefficient(G: nx.Graph):
    """
    Calculates the clustering coefficient for each node in the given graph.

    Parameters:
    - G (nx.Graph): The input graph.

    Returns:
    - clustering_coefficients (dict): A dictionary where the keys are the nodes and the values are their corresponding clustering coefficients.
    """
    clustering_coefficients = {}
    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        num_neighbors = len(neighbors)
        if num_neighbors < 2:
            clustering_coefficients[node] = 0.0
        else:
            num_triangles = 0
            for i in range(num_neighbors):
                for j in range(i+1, num_neighbors):
                    if G.has_edge(neighbors[i], neighbors[j]):
                        num_triangles += 1
            clustering_coefficients[node] = 2.0 * num_triangles / (num_neighbors * (num_neighbors - 1))
    return clustering_coefficients


# fucntion that calculates the maximum connected components
def maximum_connected_components(G:nx.Graph):
    """
    Finds the maximum connected component in a graph.

    Parameters:
    - G (nx.Graph): The input graph.

    Returns:
    - max_cc (list): The list of nodes in the maximum connected component.
    """
    visited = set()
    max_cc = []
    for node in G.nodes():
        if node not in visited:
            cc = []
            stack = [node]
            while stack:
                current_node = stack.pop()
                if current_node not in visited:
                    cc.append(current_node)
                    visited.add(current_node)
                    stack.extend(G.neighbors(current_node))
            if len(cc) > len(max_cc):
                max_cc = cc
    return max_cc


# function that calculates the average path length
def average_shpath_length(G):
    """
    Calculate the average shortest path length in a graph.

    Parameters:
    G (dict): The input graph represented as a dictionary.

    Returns:
    float: The average shortest path length.
    """
    # Calculate shortest path lengths between all pairs of nodes
    shortest_paths = {}
    for node in G:
        shortest_paths[node] = {}
        for target in G:
            shortest_paths[node][target] = float('inf')
        shortest_paths[node][node] = 0

    for node in G:
        queue = [node]
        while queue:
            current_node = queue.pop(0)
            for neighbor in G[current_node]:
                if shortest_paths[node][neighbor] == float('inf'):
                    shortest_paths[node][neighbor] = shortest_paths[node][current_node] + 1
                    queue.append(neighbor)

    # Compute the sum of all shortest path lengths
    total_path_length = sum(sum(length.values()) for length in shortest_paths.values())

    # Compute the average path length
    num_nodes = len(G)
    avg_path_length = total_path_length / (num_nodes * (num_nodes - 1))

    return avg_path_length