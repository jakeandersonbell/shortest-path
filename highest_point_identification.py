"""Task 2: Highest Point Identification"""

## import required packages
import rasterio
from rasterio import plot

import shapely
from shapely.geometry import Point

import numpy as np

import pyproj

## store data
elevation = rasterio.open('sz.asc')

## create 5km buffer around user location
# test user location
user_location_easting = 450000
user_location_northing = 85000
user_location = Point(user_location_easting, user_location_northing)



# generate a rasterio 5km window based on user location

# create a rasterised 5km buffer

## clip elevation array to 5km buffer


## identify highest point
elevation_np = np.loadtxt("SZ.asc", skiprows=6) # replace with buffer
highest_point = np.amax(elevation_np) # find and localise max z value
