"""Task 1: User Input"""

from shapely.geometry import Point, Polygon
from shapely.geometry import Point
import geopandas as gpd


def get_ext_poly(bb=(430000, 80000, 465000, 95000)):
    radius = 5000
    iow_extent = Polygon([[bb[0], bb[1]], [bb[0], bb[3]], [bb[3], bb[4]], [bb[3], bb[1]]])
    iow_5k_extent = iow_extent.buffer(-radius)
    return [iow_extent, iow_5k_extent]


def user_input():
    inp = input("Press ENTER to begin\n")
    print("Please provide your current location in BNG coordinates\n\nPress 'q' at any time to quit\n")
    while inp.lower() != 'q':
        inp = input("Please enter a space-separated coordinate pair: ")
        if inp.lower() != 'q':
            if len(inp.split()) != 2:
                print("You did not enter a correctly formatted coordinate pair!\nPlease try again")
            else:
                for i in [i for i in inp if i not in "1234567890 "]:
                    inp = inp.replace(i, "")
                if len(inp.split()[0]) != 6 or len(inp.split()[1]) != 6:
                    print("Each coordinate must contain 6 digits\nPlease try again\n"
                          "\x1B[3mTip: If one of your coordinates has 5 digits, try preceding it with 0\x1B[23m")
                else:
                    coords = [int(i) for i in inp.split()]
                    return Point(coords)


# test if user is within box extent aka not closer than 5km to the raster edge
def check_extent(user, extent, extent_5k):
    inside, extend = False, False
    if extent.contains(user):
        inside = True
    else:
        print('You are too close to the edge - cannot calculate quickest route to the highest point')
        exit()  # stop application if user is outside box extent
    if extent_5k.contains(user):
        extend = True
    if not extend and inside:
        # We must extend the region, put the function in here
        pass


# test if user is on the isle of wight and not in the sea
# adjusted from https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html

def on_land(user):
    island = gpd.GeoDataFrame.from_file('isle_of_wight.shp')
    if (island.contains(user)).bool():
        land = True
    else:
        land = False
        print('you are not on the island')
        exit()  # stop application if user is outside box extent
    return land
