# task 3: Nearest Integrated Transport Network
# open the solent_int.json file
with open('solent_itn.json') as json_data:
    d = json.load(json_data)
road_nodes = d['roadnodes']


# In[ ]:


# task 3: Nearest Integrated Transport Network
# identeifing the nearst nodes to the user, output the node coordinate and name

def neaest_node(x, y):
    dist_node_total = []
    coordinate_total = []
    node_name_user = []
    for coords in road_nodes:
        road_node = road_nodes[coords]
        value_idx = road_node['coords'][0:]
        coordinate_total.append(value_idx)
        dist_node = (((value_idx[0] - x) ** 2 + (value_idx[1] - y) ** 2) ** (1 / 2))
        dist_node_total.append(dist_node)
        node_name_user.append(coords)

    node_min_distanse_user = np.amin(dist_node_total)
    node_corrdinate_user = int(np.where(dist_node_total == node_min_distanse_user)[0])
    node_corrdinate_user_d = coordinate_total[node_corrdinate_user]

    node_corrdinate_user_east = node_corrdinate_user_d[0]
    node_corrdinate_user_north = node_corrdinate_user_d[1]
    node_name_user_nearest = node_name_user[node_corrdinate_user]
    return node_name_user_nearest, node_corrdinate_user_east, node_corrdinate_user_north


user_node_name_nearest, user_node_corrdinate_east, user_node_corrdinate_north = neaest_node(East, North)
Highest_point_node_name_nearest, Highest_point_node_corrdinate_east, Highest_point_node_corrdinate_north = neaest_node(
    Highest_point_east, Highest_point_north)

# distance-based searching is used in this task to get a high accuracy results


# In[ ]:


# task 3: Nearest Integrated Transport Network
# printing the results
print(color.BOLD + 'Nearst ITN node to your location:' + color.END)
print('Node name', '"', user_node_name_nearest, '"', '  Coordinate', '  East:', user_node_corrdinate_east, '     North',
      user_node_corrdinate_north)
print(color.BOLD + 'Nearst ITN node to the highest point:' + color.END)
print('Node name', '"', Highest_point_node_name_nearest, '"', '  Coordinate', '  East:',
      Highest_point_node_corrdinate_east, '   North', Highest_point_node_corrdinate_north)

# In[ ]: