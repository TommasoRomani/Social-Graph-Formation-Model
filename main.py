from time import sleep
import networkx as nx
import random
import matplotlib.pyplot as plt
import argparse
from run import *
from metrics import *

def add_random_edges(G, num_edges=8):

    # Ensure there are enough nodes in the graph
    if G.number_of_nodes() < 4:
        raise ValueError("Graph must contain at least 4 nodes")

    # Convert NodeView to list and select 4 unique nodes
    nodes = random.sample(list(G.nodes()), 4)
    print(len(nodes))
    # Add edges between the 4 nodes randomly
    for i in range(num_edges):
        index = random.randint(0,3)
        G.add_edge(nodes[index], nodes[(index+random.randint(1,3))%4])

    return G


# Function that given initial parameters, initializes the starting graph
def initializer(n: int):
    # Initialize graph
    G = nx.Graph()

    # Add nodes
    for i in range(n):
        G.add_node(i)
    # Add edges randomly to 4 nodes of the starting graph
    G = add_random_edges(G, random.randint(4, 16))

    return G
    

def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='Graph generator')

    parser.add_argument('--n', type=int, default=40,
                        help='Number of nodes in the graph')
    parser.add_argument('--k', type=int, default=100,
                        help='Number of iterations')
    parser.add_argument('--c', type=float, default=1,
                        help='parameter to differentiate preferential attachment from link prediction')
    parser.add_argument('--input', type=str, default=None,
                        help='Input file name')
    args = parser.parse_args()

    if args.input is not None:
        # Load graph
        G = load_graph(parser.parse_args().input)
        #compute metrics
        
        degreeCount, max_cc, diameter, avg_path_length, clustering_coefficient = compute_metrics(G)
        print(f'Degree distribution: {degreeCount}')
        print(f'Maximum connected components: {max_cc}')
        print(f'Network diameter: {diameter}')
        print(f'Average path length: {avg_path_length}')
        print(f'Clustering coefficient: {clustering_coefficient}')
        print(f'Average degree connectivity: {nx.average_degree_connectivity(G)}')

        print(G)
        
    else:
        # Initialize graph
        G = initializer(args.n) 
        # Draw graph
        print(G)

        # Iterate over graph
        G = iterate_and_animate(G, args.n ,args.k, args.c)

        #compute metrics
        degreeCount, max_cc, diameter, avg_path_length, clustering_coefficient = compute_metrics(G)
        print(f'Degree distribution: {degreeCount}')
        print(f'Maximum connected components: {max_cc}')
        print(f'Network diameter: {diameter}')
        print(f'Average path length: {avg_path_length}')
        print(f'Clustering coefficient: {clustering_coefficient}')

        # Save graph
        save_graph(G, degreeCount, max_cc, diameter, clustering_coefficient, f'graph_{args.n}_{args.k}_{args.c}.csv')
        print(G)


if __name__ == "__main__":
    main()