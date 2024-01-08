import networkx as nx
import random
from link_pred import *
from pref_attachment import preferential_attachment
from plot import *
import plotly.graph_objects as go
import plotly.io as pio

from plot import create_frame

# function that iterates a K(numbero of iterations) times and at each iteration samples a random node and adds a link to it
def graph_iterator(G:nx.Graph, c:int):
       
    # Select a random node
    node = random.choice(list(G.nodes()))
    p = probability(G, node, c)

    if random.random() < p:
        #computese adamic adar index
        G = adamic_adar(G, node)
    else:
        #adds link by preferential attachment
        G = preferential_attachment(G, node)

    # TODO: function thath given cardinality of sampled nodes adds link by preferential attachment or by other link prediction method
    return G

# function that given a node calculates the probability of generating a link through preferential attachment or trough other link prediction method
def probability(G:nx.Graph, node:int, c:int):
    p = G.degree(node)/(G.degree(node)+c)
    return p    


# Function that saves the output graph in a csv file
def save_graph(G:nx.Graph, degreeCount, max_cc, diameter, clustering_coefficient , output_file:str):
    with open(output_file, 'w') as f:
        i=0
        f.write('node1;node2;degreeCount;max_cc;diameter;clustering_coefficient\n')
        for edge in G.edges():
            f.write(f'{edge[0]};{edge[1]};')
            if i==0:
                f.write(f'{degreeCount};{max_cc};{diameter};{clustering_coefficient};')
                i+=1
            f.write('\n')

    return


# Fucntion that loads a previously saved graph
def load_graph(input_file:str):
    G = nx.Graph()
    with open(input_file, 'r') as f:
        next(f)  # Skip the header row
        for line in f.readlines():
            edge = line.strip().split(';')
            G.add_edge(int(edge[0]), int(edge[1]))
    return G

def iterate_and_animate(G,n,k,c):
    frames = []
    pos = nx.spring_layout(G, k=2, iterations=50)
    nx.set_node_attributes(G, pos, 'pos')
    for i in range(k):
        # Generate the graph for the current iteration
        G = graph_iterator(G,c)  

        node_trace, edge_trace, G = create_frame(G,pos) 

        frames.append(go.Frame(
            data=[edge_trace, node_trace],
            name=str(i)
        ))

    steps = []
    for i in range(len(frames)):
        step = dict(
            method="animate",
            args=[[frames[i]['name']], 
                {"mode": "immediate",
                "frame": {"duration": 300, "redraw": True},
                "transition": {"duration": 300}}],
            label=frames[i]['name']
        )
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Iteration: "},
        pad={"t": 50},
        steps=steps
    )]

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title='Social network graph formation model',
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002 ) ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            sliders=sliders
        ),
        frames=frames
    )

    pio.write_html(fig, f'figure_{n}_{k}_{c}.html')


    return G