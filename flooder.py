import rasterio
import numpy as np
from rasterio import features
from shapely.geometry import Polygon, MultiPolygon

# ds_path = 'data/elevation/sz.asc'
# flood_height = 100


def make_flood_poly(dataset, flood_height):
    """Takes in dataset and a flood height then returns a MultiPolygon
    of coerced raster values above the flood height.
    """
    el = dataset.read(1)

    flood = el > flood_height

    shape = list(features.shapes(flood.astype(int), transform=dataset.transform))  # list of tuples

    shapes = [s for s in shape if s[1] == 1.0]

    polys = [Polygon(s[0]['coordinates'][0]) for s in shapes]
    flood_poly = MultiPolygon(polys)
    return flood_poly


