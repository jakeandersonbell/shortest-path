
"""Task 5: Map Plotting"""

import rasterio
import numpy
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs


def map_plot(user_location, user_node, high_point, high_node, dataset, shortest_path_gpd):
    """This function plots a map of the user_location, highest point and shortest path gpd df
    over an OS Explorer and elevation raster basemap.
    """
    # background and the map extent
    background = rasterio.open('data/background/raster-50k_2724246.tif')
    back_array = background.read(1)
    palette = np.array([value for key, value in background.colormap(1).items()])
    background_image = palette[back_array]

    bg_extent = [background.bounds.left, background.bounds.right, background.bounds.bottom, background.bounds.top]
    el_extent = [dataset.bounds.left, dataset.bounds.right, dataset.bounds.bottom, dataset.bounds.top]

    display_extent = [((user_location.x + high_point.x) / 2) - 5000,
                      ((user_location.x + high_point.x) / 2) + 5000,
                      ((user_location.y + high_point.y) / 2) - 5000,
                      ((user_location.y + high_point.y) / 2) + 5000]
    # Task 5: Map Plotting
    # defining the walking path between the user and the nearest NIT node
    # and defining the walking path between highest point and its nearest NIT node
    waking_route_user_node_lons = [user_location.x, user_node.x]
    waking_route_user_node_lats = [user_location.y, user_node.y]
    waking_route_highest_point_lons = [high_point.x, high_node.x]
    waking_route_highest_point_lats = [high_point.y, high_node.y]

    # Set up figure and extent
    fig = plt.figure(figsize=(3, 3), dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.OSGB())
    ax.set_extent(display_extent, crs=ccrs.OSGB())

    # imshow for the background
    ax.imshow(background_image, origin="upper", extent=bg_extent, zorder=0)

    # imshow for the elevation raster
    im = plt.imshow(dataset.read(1), extent=el_extent, cmap='terrain', origin='upper', zorder=0, alpha=0.6,
                    resample='True', vmax=numpy.amax(dataset.read(1)), vmin=numpy.amin(dataset.read(1)))

    # plotting the shortest path
    shortest_path_gpd.plot(ax=ax, edgecolor="blue", linewidth=0.5, zorder=2, label='ITN shorest path')

    # scattering the user point the highest elevation point
    ax.scatter(user_location.x, user_location.y, s=1.5, c='r', label='Your location')
    ax.scatter(high_point.x, high_point.y, s=1.5, c='k', label='Highest_point', marker='*')
    # user_location.xy()[1] arrow
    x, y, arrow_length = 0.9, 0.95, 0.18
    ax.annotate('N', xy=(x, y), xytext=(x, y - arrow_length), arrowprops=dict(facecolor='black', width=2, headwidth=8),
                ha='center', va='center', fontsize=9, xycoords=ax.transAxes)

    # 6) plotting the color bar
    cbar = plt.colorbar(fraction=0.03, pad=0.03)
    cbar.set_label(r"Elevation", size=8)
    cbar.ax.tick_params(labelsize=5)
    # 7) plotting the walking paths
    ax.plot(waking_route_user_node_lons, waking_route_user_node_lats, c='k', label='walking route', linewidth=0.5,
            linestyle='dashed')
    plt.legend(fontsize=3, loc=2)
    ax.plot(waking_route_highest_point_lons, waking_route_highest_point_lats, c='k', label='walking route', linewidth=0.5,
            linestyle='dashed')

    plt.show()

