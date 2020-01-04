
"""Flood Emergency Planning"""

from user_input import user_input, get_ext_poly, check_extent
from highest_point_identification import get_high_point
from nearest_itn import make_index, nearest_itn
from shortest_path import naismiths_network, dijkstra_path
from map_plotting import map_plot
from shapely.geometry import Point

"""Task 1: User Input"""


user_location = user_input()  # Returns shapely Point feature of user_location
iow_extent, iow_5k_extent = get_ext_poly()
extend = check_extent(user_location, iow_extent, iow_5k_extent)  # Returns True if raster region requires extending


"""Task 2: Highest Point Identification"""

idx = make_index()
high_point = get_high_point(user_location, extend)
dataset = high_point[2]  # pop?
end_node = nearest_itn(high_point[1], idx)

"""Task 3: Nearest Integrated Transport Network"""


start_node = nearest_itn(user_location, idx)  # Nearest


"""Task 4: Shortest Path"""


# We can load the network in first and then if the user wants to route again they can without loading it all again
network, road_links = naismiths_network(dataset)
shortest_path_gpd = dijkstra_path(start_node, end_node, network, road_links)


"""Task 5: Map Plotting"""


map_plot(user_location, start_node[1], high_point[1], end_node[1], dataset, shortest_path_gpd, extend)

