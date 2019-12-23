
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