"""Additional Task: Simulate Coastal Flooding"""

from rasterio import features
from shapely.geometry import Polygon, MultiPolygon


def make_flood_poly(dataset, flood_height):
    """Takes in dataset and a flood height then returns a MultiPolygon
    of coerced raster values above the flood height.
    """
    if flood_height:
        el = dataset.read(1)
        bb = dataset.bounds
        bounds = Polygon([(bb[0], bb[1]), (bb[0], bb[3]), (bb[2], bb[3]), (bb[2], bb[1])])
        shape = list(features.shapes((el > flood_height).astype(int), transform=dataset.transform))  # list of tuples
        shapes = [s for s in shape if s[1] == 1.0]
        poly = [Polygon(s[0]['coordinates'][0]) for s in shapes]
        dry = MultiPolygon(poly)
        return dry
    else:
        return False
