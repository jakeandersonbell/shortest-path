
# Task 2 : Highest Point Identifcation
# 2.1 open the elevation raster
elv =[]
elv = rasterio.open("SZ.asc")


# In[ ]:


# Task 2:
# 2.2: define the window function
def elv_window_subset_function(x, y):
    import numpy as np
    from rasterio.windows import Window
    col_off = int((((x - 5000 - 425000) / 5)))
    row_off = int((100000 - (y + 5000)) / 5)
    width = 2000
    height = 2000
    elv_window_subset = np.array(elv.read(1, window=Window(col_off, row_off, width, height)))
    return elv_window_subset, col_off, row_off


# In[ ]:


# task 2 and task 7:
if East < 430000 or East > 465000 or North < 80000 or North > 95000:
    if East < 430000 and North < 80000:
        elv_window_subset, col_off, row_off = elv_window_subset_function(430000, 80000)
    elif East < 430000 and North > 95000:
        elv_window_subset, col_off, row_off = elv_window_subset_function(430000, 95000)
    elif East > 465000 and North < 80000:
        elv_window_subset, col_off, row_off = elv_window_subset_function(465000, 80000)
    elif East > 465000 and North > 95000:
        elv_window_subset, col_off, row_off = elv_window_subset_function(465000, 95000)
else:
    elv_window_subset, col_off, row_off = elv_window_subset_function(East, North)

# Notes
# the condition statments have been used to cover the limitation which is mentioned in task 7
# - col off refer to column offset (number)
# - row off refer to row offset (number)
# - width of the created window
# - height of the created window


# In[ ]:


elv_max = np.amax(elv_window_subset)
elv_min = np.amin(elv_window_subset)  # will used in the graphs, the min value
elv_max_idx = np.where(elv_window_subset == elv_max)
print(elv_max)
print(elv_max_idx)
print(col_off, row_off)

# In[ ]:


# Task 2: : Highest Point Identifcation
# 2.3: identeify the highest point corrdinate

elv_min = np.amin(elv_window_subset)  # will used in the graphs, the min value


def highest_point_corrdinate(elv_window_subset, col_off, row_off):
    elv_max = np.amax(elv_window_subset)
    elv_max_idx = np.where(elv_window_subset == elv_max)
    Highest_point_east = (elv_max_idx[1] * 5) + 2.5 + 425000 + (col_off * 5)
    Highest_point_north = 100000 - ((elv_max_idx[0] * 5) + 2.5 + (row_off * 5))
    dis_to_user_highest = ((Highest_point_east - East) ** 2 + (Highest_point_north - North) ** 2) ** (1 / 2)
    min_dis_to_user_highest = float(np.amin(dis_to_user_highest))
    # the following expression will cover the limitation of having more than one point with the equal maximum elevation
    if len(Highest_point_east) > 1:
        idx_min_dis_to_user_highest = int(np.where(dis_to_user_highest == min_dis_to_user_highest)[0])
        Highest_point_east = Highest_point_east[idx_min_dis_to_user_highest]
        Highest_point_north = Highest_point_north[idx_min_dis_to_user_highest]
    return elv_max, Highest_point_east, Highest_point_north, min_dis_to_user_highest


elv_max, Highest_point_east, Highest_point_north, min_dis_to_user_highest = highest_point_corrdinate(elv_window_subset,
                                                                                                     col_off, row_off)

# the following expression esures that the highest point within 5km radious
#     - and searches for a new value to be within 5km from the user coordinate
#     - because the highest point might be in distance more than 5km - inside the 5km*5km window
while min_dis_to_user_highest > 5000:
    elv_window_subset = np.where(elv_window_subset == elv_max, -100, elv_window_subset)
    elv_max, Highest_point_east, Highest_point_north, min_dis_to_user_highest = highest_point_corrdinate(
        elv_window_subset, col_off, row_off)

# In[ ]:


# Task 2: : Highest Point Identifcation
# printing the results form task two
print(color.BOLD + 'The highest point coordinate' + color.END)
print('East:', Highest_point_east, '    North:', Highest_point_north, '    Hight:', elv_max, 'm')
print('The straight line distance to the highest point as integer:', int(min_dis_to_user_highest), 'm')

# In[ ]:

