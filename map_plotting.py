# Task 5: Map Plotting
# bnackground and the map extent
background = rasterio.open('raster-50k_2724246.tif')
back_array = background.read(1)
palette = np.array([value for key, value in background.colormap(1).items()])
background_image = palette[back_array]

bounds = background.bounds
extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
display_extent = [((East + Highest_point_east) / 2) - 5000, ((East + Highest_point_east) / 2) + 5000,
                  ((North + Highest_point_north) / 2) - 5000, ((North + Highest_point_north) / 2) + 5000]
orgion_p = [East, North]

# In[ ]:


# Task 5: Map Plotting
# defining the walking path between the user and the nearest NIT node
# and defining the walking path between highest point and its nearest NIT node
waking_route_user_node_lons = [East, user_node_corrdinate_east]
waking_route_user_node_lons_lats = [North, user_node_corrdinate_north]
waking_route_Highest_point_lons = [Highest_point_east, Highest_point_node_corrdinate_east]
waking_route_Highest_point_lats = [Highest_point_north, Highest_point_node_corrdinate_north]

# In[ ]:


# Task 5: Map Plotting


fig = plt.figure(figsize=(3, 3), dpi=300)
ax = fig.add_subplot(1, 1, 1, projection=ccrs.OSGB())
ax.set_extent(display_extent, crs=ccrs.OSGB())
# 1) inshow for the background
ax.imshow(background_image, origin="upper", extent=extent, zorder=0)
# sjer_plot_locations.plot()
nx.draw(g, node_size=1, origin="upper", extent=extent, zorder=0)
# 2) inshow for the elevation raster
im = plt.imshow(elv.read(1), cmap='Greens_r', origin="upper", extent=extent, zorder=0, alpha=0.3, resample='True',
                vmax=elv_max, vmin=elv_min)
# 3) plotting the shortest path
shortest_path_gpd.plot(ax=ax, edgecolor="blue", linewidth=0.5, zorder=2, label='ITN shorest path')
# 4) scattering the user point the highest elevation point
ax.scatter(East, North, s=1.5, c='r', label='Your location')
ax.scatter(Highest_point_east, Highest_point_north, s=1.5, c='k', label='Highest_point', marker='*')
# 5) north arrow
x, y, arrow_length = 0.9, 0.95, 0.18
ax.annotate('N', xy=(x, y), xytext=(x, y - arrow_length), arrowprops=dict(facecolor='black', width=2, headwidth=8),
            ha='center', va='center', fontsize=9, xycoords=ax.transAxes)
# 6) plotting the colorbar
cbar = plt.colorbar(fraction=0.03, pad=0.03)
cbar.set_label(r"Elevation", size=8)
cbar.ax.tick_params(labelsize=5)
# 7) plotting the walking pathes
ax.plot(waking_route_user_node_lons, waking_route_user_node_lons_lats, c='k', label='walking route', linewidth=0.5,
        linestyle='dashed')
plt.legend(fontsize=3, loc=2)
ax.plot(waking_route_Highest_point_lons, waking_route_Highest_point_lats, c='k', label='walking route', linewidth=0.5,
        linestyle='dashed')

# sjer_plot_locations.plot


# In[ ]:
