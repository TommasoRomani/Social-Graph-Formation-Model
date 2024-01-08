# Function that adds a link to nodes with high degree nodes using some link prediction algorithm
import networkx as nx
import math
from pref_attachment import preferential_attachment

def adamic_adar(G, node):
    # Initialize a set to store the nodes at distance two
    neighbours  = set()
    # Perform BFS from the start node
    for nodes, distance in nx.single_source_shortest_path_length(G, node).items():
        # If the distance is two, add the node to the set
        if distance == 2:
            neighbours.add(nodes)

    maximum = None

    if len(neighbours) == 0:
        # adds link trough preferential attachment
        G = preferential_attachment(G, node)
        return G
    else:
        for nodes in neighbours:
            # Compute the Adamic-Adar index
            try:
                score = sum(1 / math.log(G.degree(v)) for v in G[nodes])
            except ZeroDivisionError:
                # adds link trough preferential attachment
                G = preferential_attachment(G, node)
                return G
            # Add the score as a node attribute
            G.nodes[nodes]['score'] = score
            # Update maximum if it's None or if the current node has a higher score
            if maximum is None or G.nodes[nodes]['score'] > G.nodes[maximum]['score']:
                maximum = nodes
        G.add_edge(node, maximum)
    # Return node with maximum score
    return G