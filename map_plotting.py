
"""Task 5: Map Plotting"""

import rasterio
import numpy
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import networkx as nx
from shapely.geometry import Point

# user_location = Point((450000, 87000))
# user_location_node = Point((448523, 96635))
# high_point = Point((447532, 83442))
# high_point_node = Point(())


def map_plot(user_location, user_node, high_point, high_node, elevation, shortest_path_gpd):
    # background and the map extent
    background = rasterio.open('raster-50k_2724246.tif')
    back_array = background.read(1)
    palette = np.array([value for key, value in background.colormap(1).items()])
    background_image = palette[back_array]

    bounds = background.bounds
    extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
    display_extent = [((user_location.xy()[0] + high_point.xy()[0]) / 2) - 5000,
                      ((user_location.xy()[0] + high_point.xy()[0]) / 2) + 5000,
                      ((user_location.xy()[1] + high_point.xy()[1]) / 2) - 5000,
                      ((user_location.xy()[1] + high_point.xy()[1]) / 2) + 5000]
    origin_p = [user_location.xy()[0], user_location.xy()[1]]

    # Task 5: Map Plotting
    # defining the walking path between the user and the nearest NIT node
    # and defining the walking path between highest point and its nearest NIT node
    waking_route_user_node_lons = [user_location.xy()[0], user_node.xy()[0]]
    waking_route_user_node_lats = [user_location.xy()[1], user_node.xy()[1]]
    waking_route_highest_point_lons = [high_point.xy()[0], high_node.xy()[0]]
    waking_route_highest_point_lats = [high_point.xy()[1], high_node.xy()[1]]

    # Set up figure and extent
    fig = plt.figure(figsize=(3, 3), dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.OSGB())
    ax.set_extent(display_extent, crs=ccrs.OSGB())

    # 1) imshow for the background
    ax.imshow(background_image, origin="upper", extent=extent, zorder=0)

    # sjer_plot_locations.plot()
    """AS far as I am aware, we do not need to plot the graph in this task"""
    # nx.draw(g, node_size=1, origin="upper", extent=extent, zorder=0)

    # 2) imshow for the elevation raster
    im = plt.imshow(elevation.read(1), cmap='Greens_r', origin="upper", extent=extent, zorder=0, alpha=0.3, resample='True',
                    vmax=numpy.amax(elevation.read(1)), vmin=numpy.amin(elevation.read(1)))

    # 3) plotting the shortest path
    shortest_path_gpd.plot(ax=ax, edgecolor="blue", linewidth=0.5, zorder=2, label='ITN shorest path')

    # 4) scattering the user point the highest elevation point
    ax.scatter(user_location.xy()[0], user_location.xy()[1], s=1.5, c='r', label='Your location')

    ax.scatter(high_point.xy()[0], high_point.xy()[1], s=1.5, c='k', label='Highest_point', marker='*')
    # 5) user_location.xy()[1] arrow
    x, y, arrow_length = 0.9, 0.95, 0.18
    ax.annotate('N', xy=(x, y), xytext=(x, y - arrow_length), arrowprops=dict(facecolor='black', width=2, headwidth=8),
                ha='center', va='center', fontsize=9, xycoords=ax.transAxes)

    # 6) plotting the colorbar
    cbar = plt.colorbar(fraction=0.03, pad=0.03)
    cbar.set_label(r"Elevation", size=8)
    cbar.ax.tick_params(labelsize=5)
    # 7) plotting the walking pathes
    ax.plot(waking_route_user_node_lons, waking_route_user_node_lats, c='k', label='walking route', linewidth=0.5,
            linestyle='dashed')
    plt.legend(fontsize=3, loc=2)
    ax.plot(waking_route_highest_point_lons, waking_route_highest_point_lats, c='k', label='walking route', linewidth=0.5,
            linestyle='dashed')

    # sjer_plot_locations.plot

