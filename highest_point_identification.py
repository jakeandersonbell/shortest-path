"""Task 2: Highest Point Identification"""

## import required packages
import rasterio
import rasterio.mask
from shapely.geometry import Polygon, Point, mapping
import fiona
import numpy as np


# create 5km buffer around user location
user_location_easting = 449825  # coords for testing, close to centroid of isle of wight shapefile
user_location_northing = 86492
user_location = Point(user_location_easting, user_location_northing)
buffer = Polygon(user_location.buffer(5000))

## mask elevation raster with buffer
# Source: adjusted Mike T 12-09-13 https://gis.stackexchange.com/questions/52705/how-to-write-shapely-geometries-to-shapefiles
# generate shapefile of shapely buffer polygon geometry
poly = buffer  # shapely geometry

schema = {
    'geometry': 'Polygon',
    'properties': {'buffer_dist_m': 'int'},
}

with fiona.open('user_buffer.shp', 'w', 'ESRI Shapefile', schema) as c:
    c.write({
        'geometry': mapping(poly),
        'properties': {'buffer_dist_m': 5000},
    })

# source:https://rasterio.readthedocs.io/en/stable/topics/masking-by-shapefile.html
with fiona.open('user_buffer.shp', 'r') as shapefile:
    shapes = [feature['geometry'] for feature in shapefile]
with rasterio.open('SZ.asc') as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta
out_meta.update({'driver': 'GTiff',
                 'height': out_image.shape[1],
                 'width': out_image.shape[2],
                 'transform': out_transform})

with rasterio.open('SZ_masked.asc', 'w', **out_meta) as dest:
    dest.write(out_image)

# identify value of highest point
sz_masked = rasterio.open('SZ_masked.asc')  # storing masked elevation asc
sz_masked_array = sz_masked.read(1)
highest_point = np.max(sz_masked_array)  # find and localise max z value

# identify location of highest point
highest_point_row_col = np.argwhere(sz_masked_array == np.max(sz_masked_array))  # row, column
highest_point_row_col_index = highest_point_row_col[0]
highest_point_row = highest_point_row_col_index[0]
highest_point_col = highest_point_row_col_index[1]

# Source: adjusted Spatial indexing and extracting values from https://geohackweek.github.io/raster/04-workingwithrasters/
highest_point_easting, highest_point_northing = sz_masked.xy(highest_point_row, highest_point_col)  # image --> spatial coordinates

# save location of highest point
highest_point = Point(highest_point_easting, highest_point_northing)

#print('the highest point within 5km radius of you is ', np.max(sz_masked_array) ,'m high.')
#print('the highest point is located at: ', highest_point)
