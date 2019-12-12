"""Task 4: Shortest Path"""

import json
import networkx as nx
import rasterio


# make some functions that can colour network paths when using draw
def colour_path(graph, path, colour):
    first = path[0]
    for node in path[1:]:
        graph.edges[first, node]['color'] = colour
        first = node
    return graph


def get_colours(graph, default_node, default_edge):
    node_colour = [graph.nodes[node].get('color', default_node) for node in graph.nodes]
    edge_colour = [graph.edges[u, v].get('color', default_edge) for u, v in graph.edges]
    return node_colour, edge_colour


# open the itn json and access the 'roadlinks' layer
with open('data/itn/solent_itn.json', 'r') as f:
    solent_itn = json.load(f)

# initialise a MultiDiGraph object

# make uphill directed edges adhere to Naismith's rule
#   Naismith's rule will be implemented as a ratio between vertical and horizontal travel weight
# Make downhill edges just have Naismith's weight

# do dijkstra path method on user location and high point

# Display the path
