
# For printing
class color:
    BOLD = '\033[1m'
    END = '\033[0m'


# In[2]:


########  task 1: User Input
# the output of this task, East and North corrdinate of the User
print("Please insert your location coordinate in a British National Grid coordinate system (Easting,Northing)")
East = float(input(" Insert (Easting coordinate X) of your location: "))
North = float(input(" Insert (Northing coordinate Y) of your location: "))

# In[3]:


# task 1 and task 7: ensuring that the user in the Isle of Wight region
if East < 425000 or East > 470000 or North < 75000 or North > 100000:
    print(color.BOLD + "You are outside the Isle of Wight, pleases check your coordinate and try again" + color.END)
    import sys

    sys.exit()

# Note: #### This part is written in this way to cover the limitation which is mentioned in task 6
# Without considering the limitation in task 6, the command can be written as following
#         if East < 430000 or East > 965000 or North < 80000 or North > 95000:
#   print ("You are outside the Isle of Wight, pleases check your coordinate and try again")
#   import sys
#    sys.exit()


# In[ ]: