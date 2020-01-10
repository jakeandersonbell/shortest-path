"""Task 1: User Input"""

from shapely.geometry import Point, Polygon
import geopandas as gpd


def get_ext_poly(bb=(430000, 80000, 465000, 95000)):
    """Returns a Shapely Polygon for the extent of the area of interest.
    Also return a radius negatively buffered Polygon for the extent.
    """
    iow_extent = Polygon([[bb[0], bb[1]], [bb[0], bb[3]], [bb[2], bb[3]], [bb[0], bb[3]]])
    iow_5k_extent = Polygon([[bb[0] + 5000, bb[1] + 5000], [bb[0] + 5000, bb[3] - 5000],
                             [bb[2] - 5000, bb[3] - 5000], [bb[0] + 5000, bb[3] - 5000]])
    return [iow_extent, iow_5k_extent]


def user_input():
    """Prompt user for input of coordinates along with some simple
    error handling. Returns coords as Shapely Point feature.
    """
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
                    return Point(coords), input_flood()


def input_flood():
    flood = input("\nIs there any coastal flooding?\n"
                  "(coastal flooding setting will restrict the route to non-flooded areas\nand will take some time)\n\n"
                  " [Y]/N ")
    yes, flood_height, skip = ["y", "yes", "yeah", "ye", "yep", ""], "void", ["s", "S"]
    if str(flood).lower() in yes:
        while flood_height not in skip and not isinstance(flood_height, int):
            try:
                flood_height = input("What is the height of the flood (metres above sea level?) ")
                if flood_height not in skip:
                    flood_height = int(flood_height)
            except ValueError:
                print("\nYou did not input a number\nPlease try again or press S to skip: ")
    flood_height = flood_height if isinstance(flood_height, int) else False
    return flood_height


# test if user is within box extent aka not closer than 5km to the raster edge
def check_extent(user_location, extent, extent_5k):
    """Checks location of user to establish whether the raster needs extending.
    Also performs on land check"""
    extend = False
    if extent.contains(user_location):
        pass
    else:
        print('You are not within the islands extent\n\nexiting application...')
        exit()  # stop application if user is outside box extent
    if not extent_5k.contains(user_location):
        # We must extend the region
        extend = True
    on_land(user_location)
    return extend


def on_land(user_location, boundary_shp='data/shape/isle_of_wight.shp'):
    """Checks whether user is within the confines of the area of interest
    IOW shp. as default
    ."""
    island = gpd.GeoDataFrame.from_file(boundary_shp)
    if not (island.contains(user_location)).bool():
        print("You are already in the water")
        exit()  # stop application if user is outside box extent
