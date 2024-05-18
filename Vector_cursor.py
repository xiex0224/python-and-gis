# -----------------------------------------------------------------------------
# Name:     Make coordniates to points with information checking tool
# Purpose:  This script input the CSV file and output a point feature class with WGS 1984 coordinate system. If the error like run out of storage space. It will return the error
# It could check the total number of survey locations at which the species was present
# The SurveyIDs and coordinates of the three most northern and three most southern observations of the species (note: an observation is indicated as Presence = 1).
# The SurveyIDs and coordinates of the three furthest west and three furthest east observations of the species.

#
#
# Author:   Xiaosong Xie
#
# Version:  1.00
# Created:  2022-11-23
#
# Inputs:   csv file, output location and name of point feature class
# Outputs:
# A Geodatabase and point feature classes
# Total number of point feature class
# The SurveyIDs and coordinates of the three most northern and three most southern observations of the species (note: an observation is indicated as Presence = 1).
# The SurveyIDs and coordinates of the three furthest west and three furthest east observations of the species.


# Import system modules
import arcpy
import os

# Set environment settings

arcpy.env.overwriteOutput = True

# Set parameters
csv_file = arcpy.GetParameterAsText(0)
output_table_location = arcpy.GetParameterAsText(1)
output_fc_name = arcpy.GetParameterAsText(2)

# Check the existance of the geodatabase (If not create one)
gdb_path = os.path.join(output_table_location, "lab10.gdb")

# Check the existance of the geodatabase (If not create one)
# error handling routine
try:
    if not arcpy.Exists(gdb_path):
        arcpy.CreateFileGDB_management(output_table_location, "lab10.gdb")
# could be no space to create folder
except arcpy.ExecuteError:
    arcpy.AddMessage(arcpy.GetMessages(2))

# import csv file to geodatabse
csv = arcpy.conversion.TableToTable(csv_file, gdb_path, "Routess")


# Create two new fields

arcpy.AddField_management(csv, "Latitude_DD", "DOUBLE")
arcpy.AddField_management(csv, "Longitude_DD", "DOUBLE")

# Define function of concert DMS to DD and Seprate the DMS to number


def dms_to_dd(dms):
    degrees, minutes, seconds = extract_dms_values(dms)
    if degrees > 0:
        dd = degrees + minutes/60 + seconds/3600
    else:
        dd = (degrees*-1) + minutes/60 + seconds/3600
    return dd


def extract_dms_values(dms):
    # Extract numerical values from DMS string
    parts = str(dms).split('-')
    degrees = float(parts[0].replace("D", ""))
    minutes = float(parts[1].replace("M", ""))
    seconds = float(parts[2].replace("S", ""))
    return degrees, minutes, seconds


# Update cursor to add value in Latitude_DD and Longtitude_DD
fields = ["sLatitude", "sLongitude", "Latitude_DD", "Longitude_DD"]
up_cursor = arcpy.da.UpdateCursor(csv, fields)
for rows in up_cursor:
    rows[2] = dms_to_dd(rows[0])
    rows[3] = dms_to_dd(rows[1])
    up_cursor.updateRow(rows)

# Create point feature using WGS 1984
spRef = arcpy.SpatialReference(4326)

output_fc_path = os.path.join(gdb_path, output_fc_name)
point = arcpy.management.XYTableToPoint(
    csv, output_fc_path, "Longitude_DD", "Latitude_DD")

# Resaech cursor for counting total number of points
total_points = 0
south_north = []
west_east = []
res_cursor = arcpy.da.SearchCursor(point, "*")
for row in res_cursor:
    total_points += 1

arcpy.AddMessage(f"The number of points is {total_points}")
res_cursor.reset

# Resaech cursor Presence = 1, and sort the data from lowest to highest for row[7]


res_cursor1 = arcpy.da.SearchCursor(point, "*", "Presence = 1")
for row1 in res_cursor1:
    south_north.append(row1)
sorted_data = sorted(south_north, key=lambda x: x[7])

# Find the first three "Latitude_DD" and last three "Latitude_DD" and print with Survey ID
southest_3 = sorted_data[:3]
northest_3 = sorted_data[-3:]

info_list_sou = []
info_list_nor = []


for things in southest_3:
    info_sou = [things[3], things[7], things[8]]
    info_list_sou.append(info_sou)
arcpy.AddMessage(
    f"The SurveyIDs, latitude and longtitude of the of furthest south are {info_list_sou}")
for thingss in northest_3:
    info_nor = [thingss[3], thingss[7], thingss[8]]
    info_list_nor.append(info_nor)

arcpy.AddMessage(
    f"The SurveyIDs, latitude and longtitude of the of furthest south are {info_list_nor}")

# Resaech cursor Presence = 1, and sort the data from lowest to highest for row[8]
res_cursor2 = arcpy.da.SearchCursor(point, "*", "Presence = 1")
for row2 in res_cursor2:
    west_east.append(row2)
sorted_data1 = sorted(west_east, key=lambda x: x[8])

# Find the first three "Latitude_DD"and last three "Latitude_DD"" and print with Survey ID
westest_3 = sorted_data1[:3]
eastest_3 = sorted_data1[-3:]

info_list_west = []
info_list_east = []

for things1 in westest_3:
    info_west = [things1[3], things1[7], things1[8]]
    info_list_west.append(info_west)
arcpy.AddMessage(
    f"The SurveyIDs, latitude and longtitude of the of furthest west are {info_list_west}")

for things2 in eastest_3:
    info_east = [things2[3], things2[7], things2[8]]
    info_list_east.append(info_east)
arcpy.AddMessage(
    f"The SurveyIDs, latitude and longtitude of the of furthest east are {info_list_east}")
