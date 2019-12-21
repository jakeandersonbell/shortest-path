"""Task 1: User Input"""

import shapely
from shapely.geometry import Point
import geopandas as gpd

# storing box extent
min_easting = 430000
min_northing = 80000
max_easting = 465000
max_northing = 95000

# getting user input
print('Please provide your current location in BNG coordinates')
user_location_easting = float(input('Insert Easting (x coordinate) of your location: '))
user_location_northing = float(input('Insert Northing (y coordinate) of your location: '))

user_location = Point(user_location_easting, user_location_northing)

# test if user is within box extent aka not closer than 5km to the raster edge
if min_easting <= user_location_easting <= max_easting and min_northing <= user_location_northing <= max_northing:
    location = 'inside'
else:
    location = 'outside'
    print('You are too close to the edge - cannot calculate quickest route to the highest point')
    exit()  # stop application if user is outside box extent

# test if user is on the isle of wight and not in the sea
# adjusted from https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html

island = gpd.GeoDataFrame.from_file('isle_of_wight.shp')

if (island.contains(user_location)).bool():
    location = 'on land'
else:
    location = 'in the sea'
    print ('you are not on the island')
    exit()  # stop application if user is outside box extent