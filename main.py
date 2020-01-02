
"""Flood Emergency Planning"""

from user_input import user_input, get_ext_poly, check_extent
from highest_point_identification import high_point
from nearest_itn import make_index, nearest_itn
from shortest_path import naismith_path
from map_plotting import map_plot
from shapely.geometry import Point

"""Task 1: User Input"""


user_location = user_input()  # Returns shapely Point feature of user_location
iow_extent, iow_5k_extent = get_ext_poly()
check_extent(user_location, iow_extent, iow_5k_extent)


"""Task 2: Highest Point Identification"""

idx = make_index()
high_point = high_point(user_location)
dataset = high_point[2]  # pop?
end_node = nearest_itn(high_point[1], idx)
print('The highest point within 5km radius of you is ', high_point[0], 'm high.')
print('The highest point is located at: ', high_point[1])
print('The nearest node to this is: ', end_node[0])
print('This point is located at: ', end_node[1])


"""Task 3: Nearest Integrated Transport Network"""


start_node = nearest_itn(user_location, idx)  # Nearest


"""Task 4: Shortest Path"""


shortest_path_gpd = naismith_path(start_node, end_node, dataset)


"""Task 5: Map Plotting"""


map_plot(user_location, start_node[0], high_point[1], end_node[0], dataset, shortest_path_gpd)


"""Task 6: Extend the Region"""

# Buffer the original raster?

