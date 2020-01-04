"""Task 2: Highest Point Identification"""

# import required packages
import rasterio
import rasterio.mask
import fiona
import numpy as np
from shapely.geometry import Polygon, Point, mapping
from rasterio import features, transform
from rasterio.warp import reproject, aligned_target


def get_high_point(user_location, extend):

    dataset = rasterio.open('data/elevation/SZ.asc')
    if extend:
        pass
        # user_location = Point((user_location.x + ))
    poly = user_location.buffer(5000)
    # Rasterize the buffered user_location. Covered cells are 1, else 0
    shapes = features.rasterize([(poly, 1)], out_shape=dataset.shape, transform=dataset.transform, fill=0)
    if extend:
        shapes = np.pad(shapes, (1000, 1000), mode='constant', constant_values=(0, 0))

    elevation = get_elevation(extend, dataset)  # Get the elevation band
    elevation_clip = elevation.copy()  # Make a copy so we can clip it
    elevation_clip = np.multiply(elevation_clip, shapes)  # Elementwise multiplier; keep the values within the buffer

    # identify location of highest point
    highest_point_row_col = np.argwhere(elevation_clip == np.max(elevation_clip))  # list(list(row, column))

    highest_point_row = highest_point_row_col[0][0]
    highest_point_col = highest_point_row_col[0][1]

    max_height = np.max(elevation_clip)
    # Save geographic location of highest point
    if extend:
        highest_point = Point(dataset.xy(highest_point_row - 1000, highest_point_col - 1000))
        elevation = dataset.read(1)
    else:
        highest_point = Point(dataset.xy(highest_point_row, highest_point_col))  # Array index --> Geographic Coordinates
    print('The highest point within 5km radius of you is ', max_height, 'm high.')
    print('The highest point is located at: ', highest_point)
    return [max_height, highest_point, dataset]  # Max height, highest point


def get_elevation(extend, dataset):
    if extend:
        print("You're close to the edge\nHaving to extend the raster...")
        # elevation = rasterio.pad(dataset.read(1), dataset.transform, 1000, mode='minimum')
        elevation = np.pad(dataset.read(1), (1000, 1000), mode='constant', constant_values=(0, 0))
    else:
        elevation = dataset.read(1)
    return elevation

