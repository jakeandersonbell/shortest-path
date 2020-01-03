"""Task 2: Highest Point Identification"""

# import required packages
import rasterio
import rasterio.mask
import fiona
import numpy as np
from shapely.geometry import Polygon, Point, mapping
from rasterio import features, transform


def high_point(user_location, extend):

    dataset = rasterio.open('data/elevation/SZ.asc')
    poly = user_location.buffer(5000)
    # Rasterize the buffered user_location. Covered cells are 1, else 0
    shapes = features.rasterize([(poly, 1)], out_shape=dataset.shape, transform=dataset.transform, fill=0)

    elevation = get_elevation(extend, dataset)  # Function to test whether or not we need to extend
    elevation = dataset.read(1)  # Get the elevation band
    elevation_clip = elevation.copy()  # Make a copy so we can clip it
    elevation_clip = np.multiply(elevation_clip, shapes)  # Elementwise multiplier; keep the values within the buffer

    # identify location of highest point
    highest_point_row_col = np.argwhere(elevation_clip == np.max(elevation_clip))  # list(list(row, column))

    highest_point_row = highest_point_row_col[0][0]
    highest_point_col = highest_point_row_col[0][1]

    # Save geographic location of highest point
    highest_point = Point(dataset.xy(highest_point_row, highest_point_col))  # Array index --> Geographic Coordinates
    return [np.max(elevation_clip), highest_point, dataset]  # Max height, highest point


def get_elevation(extend, dataset):
    if extend:
        print("You're close to the edge\nHaving to extend the raster...")
        bb = dataset.bounds
        elevation = np.pad(dataset.read(1), (500, 500), mode='constant', constant_values=(0, 0))
    else:
        elevation = dataset.read(1)
    return elevation

