"""Task 3: Nearest Integrated Transport Network"""

import rasterio
from shapely.geometry import Point
import geopandas as gpd
from rtree import index


def nearest_itn(target_location, idx):
    # find nearest
    obj = list(idx.nearest((target_location.xy[0][0], target_location.xy[1][0]), 1, objects=True))[0]
    start = obj.object
    start_p = Point((obj.bounds[0], obj.bounds[2]))
    print("The nearest itn node to " + str(target_location.bounds[0:2]) + " is: " +
          str(start) + " at: " + str(start_p.bounds[0:2]))
    return [start, start_p]


def make_index():
    # Read in the ITN nodes
    nodes = gpd.read_file('data/roads/nodes.shp')

    # create and index, bounding box
    idx = index.Index()

    # loop though points in nodes and insert - I think this works
    for i, j in enumerate(nodes.iterrows()):
        pbr = j[1][2].xy[0][0], j[1][2].xy[1][0], j[1][2].xy[0][0], j[1][2].xy[1][0]
        idx.insert(i, pbr, obj=j[1][0])
    return idx

