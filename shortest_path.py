"""Task 4: Shortest Path"""

import json
import rasterio
import networkx as nx
import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point


def naismiths_network(dataset, restriction=False):
    """Takes in rasterio elevation object and optional public road restriction bool and
    returns list(naismith weighted nx.MultiDiGraph, dict(road_links))

    Naismith's rule states that a reasonably fit person can walk at 5km/hr and an additional
    minute should be added for each 10 m of climb. Walking speed is therefor 83.3metres/min and
    climb component 10metres/min. Edge weight is penalised by elevation difference to a factor of the
    walking:climbing speed ratio (8.3). This serves as a high resolution Naismith's weighting.
    """
    print("Opening ITN\n")
    # open the itn json and access the 'roadlinks' layer
    with open('data/itn/solent_itn.json', 'r') as f:
        road_links = json.load(f)['roadlinks']

    if restriction:  # Extra marks; This feature can restrict the user to public roads
        road_links = [k for k in road_links if 'private' not in road_links[k]['descriptiveTerm'].lower()]

    g = nx.MultiDiGraph()  # initialise a MultiDiGraph object

    print("Calculating Naismith's Weights\n")
    for i, link in enumerate(road_links):
        prev_coords = road_links[link]['coords'][0]  # Coordinates of start node of edge
        next_coords = road_links[link]['coords'][-1]  # Coordinates of end node of edge
        # Implement sample() to access band values at given array coordinates
        prev_elev = list(dataset.sample([(prev_coords[0], prev_coords[1])], 1))[0][0]
        next_elev = list(dataset.sample([(next_coords[0], next_coords[1])], 1))[0][0]
        elev_diff = next_elev - prev_elev  # Change in elevation from start -> end nodes
        forward, backward = 0, 0  # The default naismith's component for no change in elevation
        if elev_diff > 0:  # Going uphill
            forward = elev_diff * 8.333  # The vert/horiz ratio multiplier
        elif elev_diff < 0:  # Downhill
            backward = (elev_diff * -1) * 8.333  # Ensure weight is always increasing with elevation along edge
        # Add edges in both directions; naismith's only contributes to uphill directed edges
        g.add_edge(road_links[link]['start'], road_links[link]['end'], fid=link,
                   weight=(road_links[link]['length'] + forward), st_height=prev_elev)
        g.add_edge(road_links[link]['end'], road_links[link]['start'], fid=link,
                   weight=(road_links[link]['length'] + backward), st_height=next_elev)
    return [g, road_links]


def dijkstra_path(start, end, g, road_links):
    """Takes in a start and  and end list(node name, Point(node location)) object,
    a networkx graph and a dictionary of network links and returns a gpd df of
    the shortest dijkstra path with geometry, length, weight and travel time.
    """
    print("Calculating shortest path\n")
    path = nx.dijkstra_path(g, source=start[0], target=end[0], weight="weight")

    df = pd.DataFrame({"A": path[:-1]})
    coords, lengths, weights = [], [], []  # Initailise a list to store LineString data
    # getting the coords
    for i, p in enumerate(path[:-1]):
        coord = [tuple(l) for l in road_links[g.get_edge_data(p, path[i + 1])[0]['fid']]['coords']]
        coords.append(LineString(coord))
        lengths.append(road_links[g.get_edge_data(p, path[i + 1])[0]['fid']]['length'])
        weights.append(g.get_edge_data(p, path[i + 1])[0]['weight'])

    df['geometry'] = coords
    df['length'] = lengths  # Define new columns for the Dataframe
    df['weights'] = weights
    df['travel_t'] = [i * 1.388 for i in weights]
    gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:27700'}, geometry=df['geometry'])
    return gdf
