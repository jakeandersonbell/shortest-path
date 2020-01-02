"""Task 4: Shortest Path"""

import json
import rasterio
import networkx as nx
import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point

# start = ['osgb4000000026145382', 0]
# end = ['osgb4000000026146148', 0]
# dataset = rasterio.open('data/elevation/sz.asc')


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


def naismith_path(start, end, dataset):
    elevation = dataset.read(1)
    print("Opening ITN\n")
    # open the itn json and access the 'roadlinks' layer
    with open('data/itn/solent_itn.json', 'r') as f:
        road_links = json.load(f)['roadlinks']

    # initialise a MultiDiGraph object
    g = nx.MultiDiGraph()

    # make uphill directed edges adhere to Naismith's rule
    #   Naismith's rule will be implemented as a ratio between vertical and horizontal travel weight
    # Make downhill edges just have length weight
    print("Calculating Naismith's Weights\n")
    for i, link in enumerate(road_links):
        prev_coords = road_links[link]['coords'][0]  # Coordinates of first node of edge
        next_coords = road_links[link]['coords'][-1]  # Coordinates of second node
        # Implement sample() to access array of band values at given location
        prev_elev = list(dataset.sample([(prev_coords[0], prev_coords[1])], 1))[0][0]
        next_elev = list(dataset.sample([(next_coords[0], next_coords[1])], 1))[0][0]
        elev_diff = next_elev - prev_elev  # Change in elevation
        forward, backward = 0, 0  # The default for no change in elevation
        if elev_diff > 0:  # Going uphill
            forward = elev_diff * 8.333  # The vert/horiz ratio multiplier
        elif elev_diff < 0:  # Downhill
            backward = (elev_diff * -1) * 8.333
        g.add_edge(road_links[link]['start'], road_links[link]['end'], fid=link,
                   weight=(road_links[link]['length'] + forward), st_height=prev_elev)
        g.add_edge(road_links[link]['end'], road_links[link]['start'], fid=link,
                   weight=(road_links[link]['length'] + backward), st_height=next_elev)
        # print(road_links[link]['start'])

    # do dijkstra path method on user location and high point
    # start and end are lists of [node_name, shapely Point]
    path = nx.dijkstra_path(g, source=start[0], target=end[0], weight="weight")

    df = pd.DataFrame({"A": path[:-1]})
    coords = []  # Initailise a list to store LineString data
    # getting the coords
    for i, p in enumerate(path[:-1]):
        coord = [tuple(l) for l in road_links[g.get_edge_data(p, path[i + 1])[0]['fid']]['coords']]
        coords.append(LineString(coord))

    df['geometry'] = coords
    gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:27700'}, geometry=df['geometry'])
    return gdf

