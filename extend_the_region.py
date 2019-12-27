"""Task 6: Extend the Region"""
import rasterio
from rasterio.transform import from_origin
import numpy as np



# find extend of new raster
min_easting, min_northing, max_easting, max_northing = 430000, 80000, 465000, 95000 # storing box extent
min_from_edge = 5000
elev_min_easting, elev_min_northing, elev_max_easting, elev_max_northing = min_easting - min_from_edge , min_northing - min_from_edge, max_easting + min_from_edge, max_northing + min_from_edge # coordinates of elevation raster
ext_min_easting, ext_min_northing, ext_max_easting, ext_max_northing = elev_min_easting - min_from_edge, elev_min_northing- min_from_edge, elev_max_easting + min_from_edge, elev_max_northing + min_from_edge # max outer coordinates of extended raster


# create new raster
# adjusted, source: Bryce Frank 18-04-18 https://gis.stackexchange.com/questions/279953/numpy-array-to-gtiff-using-rasterio-without-source-raster
# raster a: extent below elevation raster
min_x = ext_min_easting
max_y = elev_min_northing

dif_x_cell = int((ext_max_easting - min_x)/5)
dif_y_cell = int((max_y - ext_min_northing)/5)

pixel_size = 5
arr = np.zeros((dif_y_cell, dif_x_cell)) # raster value set to 0 because raster extension should be at sea level
transform = from_origin(min_x, max_y, pixel_size, pixel_size)
extension_a = rasterio.open('extension_a.tif', 'w', driver='GTiff',
                            height = arr.shape[0], width = arr.shape[1],
                            count=1, dtype=str(arr.dtype),
                            crs='+init=epsg:27700',
                            transform=transform)
extension_a.write(arr, 1)
extension_a.close()

# raster b: extent left to elevation raster
# raster c: extent above elevation raster
# raster d: extent right to elevation raster


# merge new rasters and elevation raster



# test if user is on the isle of wight
# adjusted from https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html

#island = gpd.GeoDataFrame.from_file('isle_of_wight.shp')

#if (island.contains(user_location)).bool():
#    location = 'on land'
#else:
#    location = 'in the sea'
#    print ('you are not on the island')
#    exit()  # stop application if user input not on land