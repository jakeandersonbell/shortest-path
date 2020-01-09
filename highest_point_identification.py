"""Task 2: Highest Point Identification"""

# import required packages
import rasterio
import rasterio.mask
import numpy as np
from shapely.geometry import Polygon, Point, mapping
from rasterio import features, transform


def get_high_point(user_location, extend, flood_height, dataset_path='data/elevation/SZ.asc', radius=5000):
    """Given a user location, extend bool, dataset path (optional) and radius (optional) this function will
    return the dataset of the parameterised path in addition to the value and Point(location) of the
    highest elevation within a parameterised radius of the user in form of list[value, location, dataset].
    """
    print("\nOpening elevation data...")
    dataset = rasterio.open(dataset_path)
    array_radius = int(radius / dataset.transform[0])
    # Rasterize the buffered user_location. Covered cells are 1, else 0
    print("\nRasterizing location buffer...")
    radius_clipper = features.rasterize([(user_location.buffer(radius), 1)], out_shape=dataset.shape,
                                        transform=dataset.transform, fill=0)

    elevation = get_elevation(extend, dataset, array_radius)  # Get the elevation band
    user_height = list(dataset.sample([(user_location.xy[0][0], user_location.xy[1][0])], 1))[0][0]

    print("\nYou are at a height of " + str(int(user_height)) + "m.")

    if flood_height:  # If the user has specified coastal flooding
        if user_height <= flood_height:
            print("\nIt looks like the flood has got you already\nYou had better get some help")
            exit()

    if extend:  # If the elevation array is padded ensure that the user radius array is also padded to same dimension
        radius_clipper = np.pad(radius_clipper, (array_radius, array_radius), mode='constant', constant_values=(0, 0))
    elevation_clip = elevation.copy()  # Make a copy so we can clip it
    elevation_clip = np.multiply(elevation_clip, radius_clipper)  # Elementwise multiplier; keep values within buffer

    if flood_height:
        flood_mask = elevation_clip > float(flood_height)
        elevation_clip = np.multiply(elevation_clip, flood_mask.astype(int))

    # identify location of highest point
    highest_point_row_col = np.argwhere(elevation_clip == np.max(elevation_clip))  # list(list(row, column))

    highest_point_row, highest_point_col = highest_point_row_col[0][0], highest_point_row_col[0][1]

    max_height = np.max(elevation_clip)
    # Save geographic location of highest point
    if extend:  # Offset array coordinates if elevation has been extended (distance/resolution)
        highest_point = Point(dataset.xy(highest_point_row - array_radius, highest_point_col - array_radius))
    else:
        highest_point = Point(dataset.xy(highest_point_row, highest_point_col))  # Array index -> Geographic Coordinates
    print('The highest point within 5km radius of you is', int(max_height), 'm high.')
    print('The highest point is located at: ', highest_point.bounds[0:2])
    return [highest_point, dataset]  # Max height, highest point


def get_elevation(extend, dataset, array_radius):
    if extend:
        print("\nYou're close to the edge\nHaving to extend the raster...")
        elevation = np.pad(dataset.read(1), (array_radius, array_radius), mode='constant', constant_values=(0, 0))
    else:
        elevation = dataset.read(1)
    return elevation


