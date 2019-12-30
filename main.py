
"""Flood Emergency Planning"""

from user_input import user_input, get_ext_poly, check_extent
from highest_point_identification import high_point
from nearest_itn import make_index, nearest_itn
from shortest_path import naismith_path

"""Task 1: User Input"""


user_location = user_input()  # Returns shapely Point feature of user_location
iow_extent, iow_5k_extent = get_ext_poly()
check_extent(user_location, iow_extent, iow_5k_extent)


"""Task 2: Highest Point Identification"""

idx = make_index()
high_point = high_point(user_location)
dataset = high_point[2]  # pop?
end_point = nearest_itn(high_point[1], idx)
print('the highest point within 5km radius of you is ', high_point[0], 'm high.')
print('the highest point is located at: ', high_point[1])


"""Task 3: Nearest Integrated Transport Network"""


start_point = nearest_itn(user_location, idx)  # Nearest


"""Task 4: Shortest Path"""


naismith_path(start_point, end_point, dataset)
# import libraries

# make some functions that can colour network paths

# open the itn json and access the 'roadlinks' layer

# initialise a MultiDiGraph object

# make uphill directed edges adhere to Naismith's rule
#   Naismith's rule will be implemented as a ratio between vertical and horizontal travel weight
# Make downhill edges just have Naismith's weight

# do dijkstra path method on user location and high point


"""Task 5: Map Plotting"""

"""Task 6: Extend the Region"""

# Buffer the original raster?

