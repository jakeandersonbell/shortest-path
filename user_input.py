"""Task 1: User Input"""

import shapely
from shapely.geometry import Point

#storing box extent
min_easting = 430000
min_northing = 80000
max_easting = 465000
max_northing = 95000

# getting user input
print("Please provide your current location in BNG coordinates")
user_location_easting = float(input("Insert Easting (x coordinate) of your location: "))
user_location_northing = float(input("Insert Northing (y coordinate) of your location: "))

user_location = Point(user_location_easting, user_location_northing)

# test if user is within box extent
if min_easting <= user_location_easting <= max_easting and min_northing <= user_location_northing <= max_northing:
    location = "inside"
else:
    location = "outside"
    print("You are too close to the edge - cannot calculate quickest route to the highest point")
    exit() # stop application if user is outside box extent