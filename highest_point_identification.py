"""Task 2: Highest Point Identification"""

## import required packages
import rasterio
from rasterio.windows import Window
from matplotlib import pyplot

import numpy as np

import pyproj

## store data
elevation = rasterio.open('sz.asc')

## create 5km buffer around user location
# test user location and box extents from task 1
user_location_easting = 449825 # coords for testing, close to centroid of isle of wight shapefile
user_location_northing = 86492
min_easting = 430000
min_northing = 80000
max_easting = 465000
max_northing = 95000

# generate a rasterio 5km window based on user location
# basic code from https://rasterio.readthedocs.io/en/stable/topics/reading.html
# basic code from https://rasterio.readthedocs.io/en/stable/topics/windowed-rw.html#windowrw

user_easting_cell = round(((user_location_easting - (min_easting - 5000)) / 5) - 500)  # user location x coord transformed to asc file row off cell location
user_northing_cell = round(((user_location_northing - (min_northing - 5000)) / 5) - 500)
col_off = user_easting_cell - 500  # 2.5km west of user location to generate 5km window around user location
row_off = user_northing_cell - 500
if col_off < 1:  # to ensure that col_off is within elevation raster, hence search radius might be less than 5km
    col_off = 1
if row_off < 1:
    row_off = 1

width = 1000  # cellsize = 5m, window 5km around user point
height = 1000
with rasterio.open('SZ.asc') as src:
    user_window = src.read(1, window=Window(col_off, row_off, width, height))

pyplot.imshow(user_window, cmap='pink')
#pyplot.show()

# create a rasterised 5km buffer

## clip elevation array to 5km buffer


## identify highest point
elevation_np = np.loadtxt("SZ.asc", skiprows=6) # replace with buffer
highest_point = np.amax(elevation_np) # find and localise max z value
