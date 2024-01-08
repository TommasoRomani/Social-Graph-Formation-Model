# Function that adds edges to the graph using the preferential attachment algorithm
import networkx as nx
import random


def preferential_attachment(G, node):
# Get all other nodes in the graph
    
    nodes = [n for n in G.nodes() if n != node]

    # Get all combinations of the given node with the other nodes
    combinations = [(node, n) for n in nodes]

    for i, j in combinations:
        # Calculate the PA score
        G.nodes[j]['score'] = (G.degree(i) + 1) * (G.degree(j)+ 1)
        #print(G.nodes[j]['score'])

    # Stocastically select a node to add the edge to based on the PA score
    j = random.choices(nodes, weights=[G.nodes[n]['score'] for n in nodes], k=1)[0]
    # Add the edge to the graph
    G.add_edge(node, j)

    return G