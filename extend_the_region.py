"""Task 6: Extend the Region"""
import rasterio
from rasterio.transform import from_origin
from rasterio.merge import merge
from rasterio import plot
import numpy as np

# function to create new raster
# adjusted/based on: Bryce Frank 18-04-18 https://gis.stackexchange.com/questions/279953/numpy-array-to-gtiff-using-rasterio-without-source-raster
def new_raster(min_x, max_y, max_easting, min_northing, out_raster):
    pixel_size = 5
    dif_x_cell = int((max_easting - min_x)/5)
    dif_y_cell = int((max_y - min_northing)/5)
    arr = np.zeros((dif_y_cell, dif_x_cell))  # raster value set to 0 because raster extension should be at sea level
    transform = from_origin(min_x, max_y, pixel_size, pixel_size)
    extension = rasterio.open(out_raster, 'w', driver='GTiff',
                                height=arr.shape[0], width=arr.shape[1],
                                count=1, dtype=str(arr.dtype),
                                crs='+init=epsg:27700',
                                transform=transform)
    extension.write(arr, 1)
    extension.close()


# find extend of new raster
min_easting, min_northing, max_easting, max_northing = 430000, 80000, 465000, 95000 # storing box extent
min_from_edge = 5000
elev_min_easting, elev_min_northing, elev_max_easting, elev_max_northing = min_easting - min_from_edge , min_northing - min_from_edge, max_easting + min_from_edge, max_northing + min_from_edge # coordinates of elevation raster
ext_min_easting, ext_min_northing, ext_max_easting, ext_max_northing = elev_min_easting - min_from_edge, elev_min_northing- min_from_edge, elev_max_easting + min_from_edge, elev_max_northing + min_from_edge # max outer coordinates of extended raster


# create new raster
new_raster(ext_min_easting, elev_min_northing, ext_max_easting, ext_min_northing,'extension_a.tif') # raster a: extent below elevation raster
new_raster(ext_min_easting, elev_max_northing, elev_min_easting, elev_min_northing,'extension_b.tif') # raster b: extent left to elevation raster
new_raster(ext_min_easting, ext_max_northing, ext_max_easting, elev_max_northing, 'extension_c.tif') # raster c: extent above elevation raster
new_raster(elev_max_easting, elev_max_northing, ext_max_easting, elev_min_northing, 'extension_d.tif') # raster d: extent right to elevation raster


# merge new rasters
# source https://rasterio.readthedocs.io/en/latest/api/rasterio.merge.html
extension_a = rasterio.open('extension_a.tif')
extension_b = rasterio.open('extension_b.tif')
extension_c = rasterio.open('extension_c.tif')
extension_d = rasterio.open('extension_d.tif')
elevation = rasterio.open('sz.asc')

extension_raster = [extension_a, extension_b, extension_c, extension_d, elevation] # list of extension rasters

extension_merged, out_trans = merge(extension_raster) # merge extension rasters

rasterio.open('extension_merged.tif', 'w', driver='GTiff',
                                height=extension_merged.shape[0], width=extension_merged.shape[1],
                                count=1, dtype=str(extension_merged.dtype),
                                crs='+init=epsg:27700',
                                transform=out_trans) # write merged extension raster
extension = rasterio.open('extension_merged.tif')
rasterio.plot.show(extension)



# test if user is on the isle of wight
# adjusted from https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html

#island = gpd.GeoDataFrame.from_file('isle_of_wight.shp')

#if (island.contains(user_location)).bool():
#    location = 'on land'
#else:
#    location = 'in the sea'
#    print ('you are not on the island')
#    exit()  # stop application if user input not on land