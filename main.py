<<<<<<< HEAD

"""Flood Emergency Planning"""

from user_input import *

"""Task 1: User Input"""

user_location = user_input()  #
iow_extent, iow_5k_extent = get_ext_poly()
if check_extent(user_location, iow_extent, iow_5k_extent):
    # We don't need to extend the region
    pass

if on_land(user_location):
    # The user is on land
    pass


"""Task 2: Highest Point Identification"""


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
=======
#!/usr/bin/env python
# coding: utf-8

# In[1]:


# For printing  
class color:
    BOLD = '\033[1m'
    END = '\033[0m'


# In[2]:


########  task 1: User Input 
# the output of this task, East and North corrdinate of the User 
print ("Please insert your location coordinate in a British National Grid coordinate system (Easting,Northing)")
East = float (input(" Insert ( Easting coordinate X) of your location: "))
North = float (input(" Insert ( Northing coordinate Y) of your location: "))


# In[3]:


# task 1 and task 7: ensuring that the user in the Isle of Wight region  
if East < 425000 or East > 470000 or North < 75000 or North > 100000:
    print (color.BOLD + "You are outside the Isle of Wight, pleases check your coordinate and try again" + color.END) 
    import sys 
    sys.exit()
    
# Note: #### This part is written in this way to cover the limitation which is mentioned in task 6 
# Without considering the limitation in task 6, the command can be written as following 
#         if East < 430000 or East > 965000 or North < 80000 or North > 95000:
#   print ("You are outside the Isle of Wight, pleases check your coordinate and try again") 
#   import sys 
#    sys.exit()


# In[ ]:





# In[ ]:


import numpy as np
import pandas as pd
import rasterio 
import geopandas as gpd
import json
import matplotlib.pyplot as plt
import cartopy.crs as ccrs 


# In[ ]:


# Task 2 : Highest Point Identifcation 
# 2.1 open the elevation raster 
elv =[]
elv  = rasterio.open("SZ.asc")


# In[ ]:


# Task 2: 
# 2.2: define the window function
def elv_window_subset_function(x,y):
    import numpy as np
    from rasterio.windows import Window
    col_off = int((((x - 5000 - 425000)/5) )) 
    row_off = int((100000- (y+5000))/5) 
    width = 2000 
    height = 2000 
    elv_window_subset = np.array(elv.read(1, window=Window(col_off, row_off, width, height)))
    return elv_window_subset , col_off , row_off


# In[ ]:


# task 2 and task 7: 
if East < 430000 or East > 465000 or North < 80000 or North > 95000:
    if East < 430000 and North < 80000:
        elv_window_subset , col_off , row_off = elv_window_subset_function(430000,80000)
    elif  East < 430000 and North > 95000:
        elv_window_subset , col_off , row_off = elv_window_subset_function(430000,95000)
    elif  East > 465000 and North < 80000:
        elv_window_subset , col_off , row_off = elv_window_subset_function(465000,80000)
    elif  East > 465000 and North > 95000:
        elv_window_subset , col_off , row_off= elv_window_subset_function(465000,95000)
else:
    elv_window_subset , col_off , row_off = elv_window_subset_function(East,North)
    
#Notes
# the condition statments have been used to cover the limitation which is mentioned in task 7 
# - col off refer to column offset (number)
# - row off refer to row offset (number)
# - width of the created window 
# - height of the created window 


# In[ ]:


elv_max = np.amax(elv_window_subset)
elv_min = np.amin(elv_window_subset) #will used in the graphs, the min value 
elv_max_idx = np.where(elv_window_subset == elv_max)
print(elv_max)
print(elv_max_idx)
print(col_off ,row_off)


# In[ ]:


# Task 2: : Highest Point Identifcation 
# 2.3: identeify the highest point corrdinate

elv_min = np.amin(elv_window_subset) #will used in the graphs, the min value 

def highest_point_corrdinate(elv_window_subset, col_off ,row_off):
    elv_max = np.amax(elv_window_subset)
    elv_max_idx = np.where(elv_window_subset == elv_max)
    Highest_point_east =  (elv_max_idx[1] * 5 )+ 2.5 + 425000 + (col_off*5)
    Highest_point_north =  100000 - ((elv_max_idx[0] * 5 ) + 2.5 + (row_off*5))
    dis_to_user_highest = ((Highest_point_east - East)**2 + (Highest_point_north - North)**2)**(1/2)
    min_dis_to_user_highest = float(np.amin(dis_to_user_highest))
    # the following expression will cover the limitation of having more than one point with the equal maximum elevation
    if len(Highest_point_east) > 1:
        idx_min_dis_to_user_highest= int(np.where(dis_to_user_highest == min_dis_to_user_highest)[0])
        Highest_point_east = Highest_point_east[idx_min_dis_to_user_highest]
        Highest_point_north = Highest_point_north[idx_min_dis_to_user_highest] 
    return elv_max, Highest_point_east , Highest_point_north , min_dis_to_user_highest

elv_max, Highest_point_east , Highest_point_north , min_dis_to_user_highest = highest_point_corrdinate(elv_window_subset, col_off ,row_off)

# the following expression esures that the highest point within 5km radious
#     - and searches for a new value to be within 5km from the user coordinate
#     - because the highest point might be in distance more than 5km - inside the 5km*5km window
while min_dis_to_user_highest > 5000: 
    elv_window_subset= np.where(elv_window_subset==elv_max, -100, elv_window_subset)
    elv_max, Highest_point_east , Highest_point_north , min_dis_to_user_highest = highest_point_corrdinate(elv_window_subset, col_off ,row_off)


# In[ ]:


# Task 2: : Highest Point Identifcation 
# printing the results form task two 
print(color.BOLD + 'The highest point coordinate' + color.END)
print('East:', Highest_point_east, '    North:', Highest_point_north, '    Hight:',elv_max,'m') 
print ('The straight line distance to the highest point as integer:',int(min_dis_to_user_highest),'m')


# In[ ]:


# task 3: Nearest Integrated Transport Network 
# open the solent_int.json file 
with open('solent_itn.json') as json_data:
    d = json.load(json_data)
road_nodes = d['roadnodes']


# In[ ]:


# task 3: Nearest Integrated Transport Network ITN
# identeifing the nearst nodes to the user, output the node coordinate and name 

def neaest_node (x , y):
    dist_node_total = []
    coordinate_total =[] 
    node_name_user = []
    for coords in road_nodes:
        road_node = road_nodes[coords]
        value_idx = road_node['coords'][0:]
        coordinate_total.append(value_idx)
        dist_node = (((value_idx[0] - x )**2 + (value_idx[1] - y)**2)**(1/2)) 
        dist_node_total.append(dist_node)
        node_name_user.append(coords)
        
    node_min_distanse_user = np.amin(dist_node_total )
    node_corrdinate_user = int(np.where(dist_node_total == node_min_distanse_user)[0])
    node_corrdinate_user_d = coordinate_total[node_corrdinate_user]
        
    node_corrdinate_user_east = node_corrdinate_user_d[0]
    node_corrdinate_user_north = node_corrdinate_user_d[1]
    node_name_user_nearest = node_name_user[node_corrdinate_user]
    return node_name_user_nearest, node_corrdinate_user_east , node_corrdinate_user_north
    
user_node_name_nearest, user_node_corrdinate_east , user_node_corrdinate_north = neaest_node (East , North)
Highest_point_node_name_nearest, Highest_point_node_corrdinate_east , Highest_point_node_corrdinate_north = neaest_node (Highest_point_east , Highest_point_north)

# distance-based searching is used in this task to get a high accuracy results


# In[ ]:


# task 3: Nearest Integrated Transport Network
# printing the results 
print( color.BOLD + 'Nearst ITN node to you:' + color.END)
print('Node name','"',user_node_name_nearest,'"','  Coordinate','  East:', user_node_corrdinate_east ,'     North',user_node_corrdinate_north)
print( color.BOLD +'Nearst ITN node to the highest point:'+ color.END)
print('Node name','"',Highest_point_node_name_nearest,'"','  Coordinate','  East:', Highest_point_node_corrdinate_east ,'   North',Highest_point_node_corrdinate_north)


# In[ ]:


# Task 4: Shortest Path 
import networkx as nx
g = nx.Graph()
road_links = d['roadlinks']
for link in road_links:
    g.add_edge(road_links[link]['start'], road_links[link]['end'], fid = link, weight = road_links[link]['length'])


# In[ ]:


# Task 4: Shortest Path 
path = nx.dijkstra_path(g, source=user_node_name_nearest, target=Highest_point_node_name_nearest, weight="weight")


# In[ ]:


# Task 4: Shortest Path 
from shapely.geometry import LineString
links = []
geom = []
first_node = path[0]
for node in path[1:]:
    link_fid = g.edges[first_node, node]['fid']
    links.append(link_fid)
    geom.append(LineString(road_links[link_fid]['coords']))
    first_node = node
shortest_path_gpd = gpd.GeoDataFrame({"fid": links, "geometry": geom})


# In[ ]:


# Task 5: Map Plotting 
# bnackground and the map extent 
background = rasterio.open('raster-50k_2724246.tif')
back_array = background.read(1)
palette = np.array([value for key, value in background.colormap(1).items()])
background_image = palette[back_array]





bounds = background.bounds
extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
display_extent = [((East + Highest_point_east)/2)-5000, ((East + Highest_point_east)/2)+5000, ((North+ Highest_point_north)/2)-5000, ((North+ Highest_point_north)/2)+5000]
orgion_p = [East , North]



# In[ ]:


# Task 5: Map Plotting 
# defining the walking path between the user and the nearest ITN node
# and defining the walking path between highest point and its nearest NIT node
waking_route_user_node_lons = [East, user_node_corrdinate_east]
waking_route_user_node_lons_lats = [North , user_node_corrdinate_north]
waking_route_Highest_point_lons = [Highest_point_east, Highest_point_node_corrdinate_east]
waking_route_Highest_point_lats = [Highest_point_north , Highest_point_node_corrdinate_north]


# In[ ]:


# Task 5: Map Plotting 

   


fig = plt.figure(figsize=(3,3), dpi=300)
ax = fig.add_subplot(1,1,1, projection=ccrs.OSGB())
ax.set_extent(display_extent, crs=ccrs.OSGB())
# 1) inshow for the background 
ax.imshow(background_image, origin="upper", extent=extent, zorder=0 ) 
#sjer_plot_locations.plot()
nx.draw(g, node_size=1, origin="upper", extent=extent, zorder=0)
# 2) inshow for the elevation raster 
im = plt.imshow(elv.read(1), cmap='Greens_r' , origin="upper", extent=extent, zorder=0 , alpha = 0.3 , resample = 'True',  vmax = elv_max , vmin= elv_min  )
# 3) plotting the shortest path 
shortest_path_gpd.plot(ax=ax, edgecolor="blue", linewidth=0.5, zorder=2 , label ='ITN shorest path')
# 4) scattering the user point the highest elevation point
ax.scatter(East, North , s = 1.5 , c='r' , label ='Your location' )
ax.scatter(Highest_point_east , Highest_point_north , s = 1.5 , c='k' , label ='Highest_point', marker ='*' )
# 5) north arrow 
x, y, arrow_length = 0.9, 0.95, 0.18
ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),arrowprops=dict(facecolor='black', width=2, headwidth=8),ha='center', va='center', fontsize=9, xycoords=ax.transAxes)
# 6) plotting the colorbar 
cbar = plt.colorbar( fraction=0.03, pad=0.03 )
cbar.set_label(r"Elevation", size=8)
cbar.ax.tick_params(labelsize=5) 
# 7) plotting the walking pathes  
ax.plot(waking_route_user_node_lons, waking_route_user_node_lons_lats,c ='k', label='walking route', linewidth=0.5 , linestyle='dashed' )
plt.legend(fontsize=3 , loc=2  )
ax.plot(waking_route_Highest_point_lons, waking_route_Highest_point_lats,c ='k', label='walking route', linewidth=0.5 , linestyle='dashed' )



#sjer_plot_locations.plot


# In[ ]:





# In[ ]:



>>>>>>> 9d8f880088b28a907c73baa1c8e7d5d66c1a2a61

