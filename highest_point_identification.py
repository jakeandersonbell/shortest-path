"""Task 2: Highest Point Identification"""

# import required packages
import rasterio
import rasterio.mask
import fiona
import numpy as np
from shapely.geometry import Polygon, Point, mapping
from rasterio import MemoryFile


def high_point(user_location, extend):
    # Mask elevation raster with buffer
    # Source: adjusted Mike T 12-09-13
    # https://gis.stackexchange.com/questions/52705/how-to-write-shapely-geometries-to-shapefiles
    # generate shapefile of shapely buffer polygon geometry
    poly = Polygon(user_location.buffer(5000))  # shapely geometry
    schema = {
        'geometry': 'Polygon',
        'properties': {'buffer_dist_m': 'int'},
    }
    with fiona.open('data/temp/user_buffer.shp', 'w', 'ESRI Shapefile', schema) as c:
        c.write({
            'geometry': mapping(poly),
            'properties': {'buffer_dist_m': 5000},
        })

    # source:https://rasterio.readthedocs.io/en/stable/topics/masking-by-shapefile.html
    with fiona.open('data/temp/user_buffer.shp', 'r') as shapefile:
        shapes = [feature['geometry'] for feature in shapefile]

    dataset = get_elevation(extend)
    out_image, out_transform = rasterio.mask.mask(dataset, shapes, crop=True)
    out_meta = dataset.meta
    out_meta.update({'driver': 'GTiff',
                     'height': out_image.shape[1],
                     'width': out_image.shape[2],
                     'transform': out_transform})

    with rasterio.open('data/temp/SZ_masked.asc', 'w', **out_meta) as dest:
        dest.write(out_image)

    # identify value of highest point
    sz_masked = rasterio.open('data/temp/SZ_masked.asc')  # storing masked elevation asc
    sz_masked_array = sz_masked.read(1)
    highest_point = np.max(sz_masked_array)  # find and localise max z value

    # identify location of highest point
    highest_point_row_col = np.argwhere(sz_masked_array == np.max(sz_masked_array))  # row, column
    highest_point_row_col_index = highest_point_row_col[0]
    highest_point_row = highest_point_row_col_index[0]
    highest_point_col = highest_point_row_col_index[1]

    # Source: adjusted Spatial indexing and extracting values from
    # https://geohackweek.github.io/raster/04-workingwithrasters/
    highest_point_easting, highest_point_northing = sz_masked.xy(highest_point_row,
                                                                 highest_point_col)  # image --> spatial coordinates

    # save location of highest point
    highest_point = Point(highest_point_easting, highest_point_northing)

    return [np.max(sz_masked_array), highest_point, dataset]  # Max height, highest point


def get_elevation(extend):
    dataset = rasterio.open('data/elevation/SZ.asc')
    if extend:
        print("You're close to the edge\nHaving to extend the raster...")
        elevation = np.pad(dataset.read(1), (2500, 2500), 'constant', constant_values=(0, 0))
        with rasterio.Env():
            profile = dataset.profile
            profile.update(dtype=rasterio.uint8, count=1)
            with MemoryFile as memf:
                with memf.open(**profile) as dataset:
                    dataset.write(elevation)
                    del elevation
                with memf.open() as dataset:
                    return dataset

    return dataset
