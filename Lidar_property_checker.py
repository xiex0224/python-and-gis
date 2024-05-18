# -----------------------------------------------------------------------------
# Name:     Lidar file property checker
# Purpose:  This script reads all type of lidar xyz file. This python script read #     all the lines in the file and return as a list of floating points which
#     contains northing, easting and elevation. It could check the total
#     numbers of points,  max and mins for easting, northing and
#     elevation, the height of tile, the width of tile, and the average
#     of elevation.
#
# Author:   Xiaosong Xie
#
# Version:  1.00
# Created:  2022-10-19
#
# Inputs:   A UTM format DEM xyz file
# Outputs:
#          Total number of UTM points,  max and mins for easting, northing
#             elevation, the height of tile, the width of tile, and the average
#          of elevation
# -----------------------------------------------------------------------------


# open file and read lines
file_name = input("Please type the file name: ")
my_file = open(file_name, 'r')
list_xyz = my_file.readlines()

# Use len() function to see how many lines in the file: Q1

utm_points = len(list_xyz)
print(f"Total number of UTM points are: {utm_points}")

# seprate the list into 3 parts and covert string to float point

line = []
for items in list_xyz:
    item = items.split()
    float_items = [float(number) for number in item]
    line.append(float_items)


print(line[1:3])

# determine the max and min for easting: Q2, Q3
min_easting = min(items[0] for items in line)
max_easting = max(items[0] for items in line)

print(f"The minimum easting values is : {min_easting}")
print(f"The maximum easting values is : {max_easting}")

# determine the max and min for northing: Q4, Q5
min_north = min(items[1] for items in line)
max_north = max(items[1] for items in line)

print(f"The minimum northing values is : {min_north}")
print(f"The maximum northing values is : {max_north}")

# Determine the height and width: Q5, Q6
height = max_north - min_north
width = max_easting - min_easting

print(f"The height of the tile is : {height}")
print(f"The width of the tile is : {width}")

# Determine the min and max elevation which is z value: Q7
min_z = min(items[2] for items in line)
max_z = max(items[2] for items in line)

print(f"The minimum elevation values is : {min_z}")
print(f"The maximum elevation values is : {max_z}")

# Average elevation: Q8
sum_z = sum(items[2] for items in line)


def average(elevation):
    sum_z = sum(items[2] for items in line)
    return sum_z / int(len(elevation))


average_z = average(list_xyz)
print(f"The average elevation values is : {average_z}")

my_file.close()
