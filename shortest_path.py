"""Task 4: Shortest Path"""

import json
import networkx as nx
import rasterio

dataset = rasterio.open('data/elevation/sz.asc')

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
    road_links = json.load(f)['roadlinks']

# initialise a MultiDiGraph object
g = nx.MultiDiGraph()

# This gets the height at a given point
coords = road_links[next(iter(road_links))]['coords'][0]
list(dataset.sample([(coords[0],coords[1])], 1))

# make uphill directed edges adhere to Naismith's rule
#   Naismith's rule will be implemented as a ratio between vertical and horizontal travel weight
# Make downhill edges just have Naismith's weight

# coords = road_links[next(iter(road_links))]['coords'][0]

for link in road_links:
    prev_coords = road_links[link]['coords'][0]
    next_coords = road_links[link]['coords'][-1]
    prev_elev = list(dataset.sample([(prev_coords[0], prev_coords[1])], 1))[0][0]
    next_elev = list(dataset.sample([(next_coords[0], next_coords[1])], 1))[0][0]
    elev_diff = next_elev - prev_elev  # Change in elevation
    forward, backward = 0, 0  # The default for no change in elevation
    if elev_diff > 0:  # Going uphill
        forward = elev_diff * 8.333  # The vert/horiz multiplier
    elif elev_diff < 0:  # downhill
        backward = elev_diff * 8.333
    g.add_edge(road_links[link]['start'], road_links[link]['end'], fid=link,
               weight=(road_links[link]['length'] + forward))
    g.add_edge(road_links[link]['end'], road_links[link]['start'], fid=link,
               weight=(road_links[link]['length'] + backward))
    print(road_links[link]['start'])



# do dijkstra path method on user location and high point

# Display the path
