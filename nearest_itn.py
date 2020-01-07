"""Task 3: Nearest Integrated Transport Network"""

from shapely.geometry import Point
import geopandas as gpd
from rtree import index


def nearest_itn(target_location, idx):
    """Takes in location and index of nodes
    Returns list(object name, Point(node location)).
    """
    obj = list(idx.nearest((target_location.xy[0][0], target_location.xy[1][0]), 1, objects=True))[0]
    start_name = obj.object
    start_p = Point((obj.bounds[0], obj.bounds[2]))
    print("\nThe nearest itn node to " + str(target_location.bounds[0:2]) + " is " +
          str(start_name) + " at " + str(start_p.bounds[0:2]))
    return [start_name, start_p]


def make_index(node_shape_path='data/roads/nodes.shp'):
    """Reads in a shp. of nodes and returns an rtree index"""
    print("\nMaking index...")
    nodes = gpd.read_file(node_shape_path)

    idx = index.Index()

    # loop though points in nodes and insert
    for i, j in enumerate(nodes.iterrows()):
        pbr = j[1][2].xy[0][0], j[1][2].xy[1][0], j[1][2].xy[0][0], j[1][2].xy[1][0]
        idx.insert(i, pbr, obj=j[1][0])
    return idx

