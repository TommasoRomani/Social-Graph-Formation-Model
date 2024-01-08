import networkx as nx

# function that calculates the metrics given the resulting network
# degree distribution
# maximim connected components
# network diameter
# average path length
# clustering coefficient

def compute_metrics(G:nx.Graph):
    # Degree distribution
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = {}
    for degree in degree_sequence:
        if degree in degreeCount:
            degreeCount[degree] += 1
        else:
            degreeCount[degree] = 1
    # Maximum connected components
    max_cc = max(nx.connected_components(G), key=len)
    
    # if the graph is not connected, the diameter and average path lenght cannot be computed
    if nx.is_connected(G):
        diameter = nx.diameter(G)    # Network diameter
        avg_path_length = nx.average_shortest_path_length(G)# Average path length
    else:
        diameter = None
        avg_path_length = None
        print("Graph is not connected, cannot compute diameter")    
    # Clustering coefficient
    clustering_coefficient = nx.average_clustering(G)

    return degreeCount, max_cc, diameter, avg_path_length, clustering_coefficient