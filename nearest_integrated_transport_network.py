"""Task 3: Nearest Integrated transport Network"""
## import required packages
import rtree
from rtree import index

import json

import networkx as nx

## index
idx = index.Index() # build index
# get min and max easting and northing of buffer
# br = (min_x, min_y, max_x. max_y) # create bounding box

## load ITN
isle_of_wight_itn_json = "solent_itn.json"
with open(isle_of_wight_itn_json, "r") as f:
    isle_of_wight_itn=json.load(f)

# create undirected graph
g = nx.Graph()
road_links = isle_of_wight_itn['roadlinks']
for link in road_links:
    g.add_edge(road_links[link]['start'], road_links[link]['end'], fid = link, weight = road_links[link]['length'])
nx.draw(g, node_size=1) # draw graph
## find nearest node

# finding nearest node to user location // if multiple items are of equal distance to the bounds, both are returned
for i in idx.nearest((0.8, 0.8), 1):
    print(i)
# finding nearest node to highest point