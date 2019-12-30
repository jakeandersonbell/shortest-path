
"""Flood Emergency Planning"""

from user_input import *
from highest_point_identification import *

"""Task 1: User Input"""

user_location = user_input()  # Returns shapely Point feature of user_location
iow_extent, iow_5k_extent = get_ext_poly()
check_extent(user_location, iow_extent, iow_5k_extent)


"""Task 2: Highest Point Identification"""

high_point = high_point(user_location)
print('the highest point within 5km radius of you is ', high_point[0], 'm high.')
print('the highest point is located at: ', high_point[1])
# Use window function to limit size of raster around the buffered point

# Get the elevation band
# elevation = dataset.read(1)

# Somehow get the location of the highest point in the window
# numpy.amax(elevation)  # gets the highest point
# res = numpy.where(elevation == numpy.amax(elevation))  # gets the array index

# Translate the numpy array position into a geo coord
# dataset.xy(res[0][0], res[1][0])

"""Task 3: Nearest Integrated Transport Network"""

# Read in the ITN nodes
# nodes = gpd.read_file('data/roads/nodes.shp')

# create and index, bounding box
# idx = index.Index()
# br = dataset.bounds[0], dataset.bounds[1], dataset.bounds[2], dataset.bounds[3]
# idx.insert(0, br)  # don't do this

# loop though points in nodes and insert - I think this works
# for i, j in enumerate(nodes['geometry'].iteritems()):  # Syntactic sugar
#     pbr = j[1].xy[0][0], j[1].xy[1][0], j[1].xy[0][0], j[1].xy[1][0]
#     idx.insert(i, pbr)

# for i in idx.nearest((450000,87000), num_result=1, objects=True):
#     print(i)

# Identify the nearest ITN node to input point - r-trees

"""Task 4: Shortest Path"""

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

