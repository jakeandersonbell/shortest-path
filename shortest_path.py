"""Task 4: Shortest Path"""

import json
import networkx as nx
import rasterio
import time
from progress_bar import printprogressbar

dataset = rasterio.open('data/elevation/sz.asc')


# make some functions that can colour network paths when using draw
def colour_path(graph, path, colour='blue'):
    result = graph.copy()
    first = path[0]
    for node in path[1:]:
        result.edges[first, node, 0]['color'] = colour
        first = node
    return result


def get_colours(graph, default_node='blue', default_edge='blue'):
    node_colour = [graph.nodes[node].get('color', default_node) for node in graph.nodes]
    edge_colour = [graph.edges[u, v, k].get('color', default_edge) for u, v, k in graph.edges]
    return node_colour, edge_colour


print("Opening ITN\n")
# open the itn json and access the 'roadlinks' layer
with open('data/itn/solent_itn.json', 'r') as f:
    road_links = json.load(f)['roadlinks']

# initialise a MultiDiGraph object
g = nx.MultiDiGraph()

# This gets the height at a given point
# coords = road_links[next(iter(road_links))]['coords'][0]
# list(dataset.sample([(coords[0], coords[1])], 1))

# make uphill directed edges adhere to Naismith's rule
#   Naismith's rule will be implemented as a ratio between vertical and horizontal travel weight
# Make downhill edges just have length weight
print("Calculating Naismith's Weights")
for i, link in enumerate(road_links):
    prev_coords = road_links[link]['coords'][0]  # Coordinates of first node of edge
    next_coords = road_links[link]['coords'][-1]  # Coordinates of second node
    # Implement sample() to access array of band values at given location
    prev_elev = list(dataset.sample([(prev_coords[0], prev_coords[1])], 1))[0][0]
    next_elev = list(dataset.sample([(next_coords[0], next_coords[1])], 1))[0][0]
    elev_diff = next_elev - prev_elev  # Change in elevation
    forward, backward = 0, 0  # The default for no change in elevation
    # if elev_diff > 0:  # Going uphill
    #     forward = elev_diff * 8.333  # The vert/horiz ratio multiplier
    # elif elev_diff < 0:  # Downhill
    #     backward = (elev_diff * -1) * 8.333
    g.add_edge(road_links[link]['start'], road_links[link]['end'], fid=link,
               weight=(road_links[link]['length'] + forward))
    g.add_edge(road_links[link]['end'], road_links[link]['start'], fid=link,
               weight=(road_links[link]['length'] + backward))
    # print(road_links[link]['start'])


start = 'osgb4000000026213564'
end = 'osgb5000005101239096'

# do dijkstra path method on user location and high point
path = nx.dijkstra_path(g, source=start, target=end, weight="weight")
print(path)

# Display the path
# g_1 = colour_path(g, path, "red")
# node_colors, edge_colors = get_colours(g_1)
# nx.draw(g_1, node_size=1, edge_color=edge_colors, node_color=node_colors)

print("Plotting path")
nx.draw(g.subgraph(path), node_size=1)




