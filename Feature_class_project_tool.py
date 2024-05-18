# -----------------------------------------------------------------------------
# Name:     Feature class project tool
# Purpose:  This script reads all type of feature class. This python script read all the features in the file and return as a list.
# It could check the total number of vector datasets(a breakdown of the number of shapefiles by geometry shape type ) and
# number of datasets in each of the following categories:
# number that were already in the NAD83 UTM 12N PCS

# number that were in another spatial reference (e.g., GCS or different datum)

# number of datasets that had no spatial reference information
#
#
# Author:   Xiaosong Xie
#
# Version:  1.00
# Created:  2022-10-31
#
# Inputs:   Feature classes
# Outputs:Total number of feature classes
# The number of point shapefiles
# The number of polyline shapefiles
# The number of polygon shapefiles
# The number of datasets that had no spatial reference information 
# The number of shapefiles were already in the NAD83 UTM 12N PCS  
# The number of shapefiles that were in another spatial reference 
#          
# -----------------------------------------------------------------------------

# Import system modules
import arcpy
import os

# Set environment settings
arcpy.env.workspace = input("Please type the workspace path: ")
arcpy.env.overwriteOutput = True


#Create a list for all the feature class
feature = arcpy.ListFeatureClasses()  # Native method

# Q1 Total number of feature classes
len_fea = len(feature)
print(f"Total number of feature classes are: {len_fea}")

#Create a fold for project processing

arcpy.CreateFolder_management(arcpy.env.workspace, "folder1")

#Set the output location to this folder
outloc = arcpy.env.workspace + "/folder1"
#Set the count for unknown, wrong coordinate, right coordinate, point, polyline and polygon
count_unknown = 0
count_right = 0
count_wrong = 0
point_count = 0
polyline_count = 0
polygon_count = 0

#For loop to count points, polylines and polygons
for shape in feature:
    des = arcpy.Describe(shape)
    if des.shapeType == 'Point':
        point_count += 1
    elif des.shapeType == 'Polyline':
        polyline_count += 1
    elif des.shapeType == 'Polygon':
        polygon_count += 1

#For loop to check the spatial Reference
for items in feature:
    desc = arcpy.Describe(items)
    spatial = desc.spatialReference
    sr = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
    out_feature = os.path.join(outloc, items)
# Unkown situation
    if spatial.Name == 'Unknown':
        arcpy.management.DefineProjection(items, sr)

        count_unknown = count_unknown + 1
# Right spatial system situation
    elif spatial.Name == "NAD_1983_UTM_Zone_12N":

        count_right = count_right + 1
# Wrong spatial system situation (output in create folder)
    else:
        arcpy.Project_management(items, out_feature, sr)
        count_wrong = count_wrong + 1
        arcpy.management.Delete(items)

# Copy the shapfiles in folder to the orginal workspace and delete everything in folder
arcpy.env.workspace = arcpy.env.workspace + "/folder1"
feature_new = arcpy.ListFeatureClasses()
outlo_new = os.path.dirname(arcpy.env.workspace)
for shape in feature_new:
    out_feature_new = os.path.join(outlo_new, shape)
    arcpy.management.CopyFeatures(shape, out_feature_new)
    arcpy.management.Delete(shape)
arcpy.management.Delete(arcpy.env.workspace)



# print result
print(f"The number of point shapefiles is {point_count}")
print(f"The number of polyline shapefiles is {polyline_count}")
print(f"The number of polygon shapefiles is {polygon_count}")
print(
    f"The number of datasets that had no spatial reference information is {count_unknown}")
print(
    f"The number of shapefiles were already in the NAD83 UTM 12N PCS  is {count_right}")
print(
    f"The number of shapefiles that were in another spatial reference is {count_wrong}")
