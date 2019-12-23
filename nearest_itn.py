"""Task 3: Nearest Integrated Transport Network"""

import rasterio
import geopandas as gpd
from rtree import index

# Read elevation
elevation = rasterio.open('sz.asc')
# Read in the ITN nodes
nodes = gpd.read_file('data/roads/nodes.shp')

# create and index, bounding box
idx = index.Index()
br = elevation.bounds[0], elevation.bounds[1], elevation.bounds[2], elevation.bounds[3]

# loop though points in nodes and insert - I think this works
for i, j in enumerate(nodes.iterrows()):
    pbr = j[1][2].xy[0][0], j[1][2].xy[1][0], j[1][2].xy[0][0], j[1][2].xy[1][0]
    idx.insert(i, pbr, obj=j[1][0])

for i in idx.nearest((450000, 87000), objects=True):
    print(i.object)


