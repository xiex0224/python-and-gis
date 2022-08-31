import arcpy as ap
from arcpy.sa import *

# Set your workspace and overwrite your output
ws1 = ap.env.workspace = "C:/Student"
ap.env.overwriteOutput = True

# Create a new RasterAnalysis geodatabase
out_workspace = ap.CreateFileGDB_management(ws1, "RasterAnalysis.gdb")
if ap.Exists("RasterAnalysis.gdb"):
    print("True")

ws2 = ap.env.workspace = ws1 + "/RasterAnalysis.gdb"
desWs2 = ap.Describe(ws2)

# Copy the datasets from the Assignment 8 folder to the Raster Analysis geodatabase
ws3 = ap.env.workspace = ws1 + "/A8Data"
Shapefiles = ap.ListFeatureClasses()

for shapefile in Shapefiles:
    desDS1 = ap.Describe(shapefile)
    ap.CopyFeatures_management(shapefile, ws1 + "/RasterAnalysis.gdb/" + desDS1.baseName)
    ap.AddMessage(shapefile + " has been copied to " + desWs2.baseName)

Rasters = ap.ListRasters()
for raster in Rasters:
    desDS1 = ap.Describe(raster)
    ap.CopyRaster_management(raster, ws1 + "/RasterAnalysis.gdb/" + desDS1.baseName)
    ap.AddMessage(raster + " has been copied to " + desWs2.baseName)

# Calcuate the slop of the Hamdem and save it to the geodatabase
ap.env.workspace = ws2
Name1 = "Hamslope"
slope = Slope("Hamdem")
slope.save(Name1)
ap.AddMessage(slope.name + " has been created and saved to " + desWs2.baseName)

# Calculate the aspects of the Hamdem and save it to the geodatabase
Name2 = "Hamaspect"
Asp = Aspect("Hamdem")
Asp.save(Name2)
ap.AddMessage(Asp.name + " has been created and saved to " + desWs2. baseName)

# Reclassify the aspects of Hamdem as provided and save it to the geodatabase
Name3 = "Aspect_Dir"
RemapRange = RemapRange([[0, 45, 1], [45, 135, 2], [135, 225, 3], [225, 315, 4], [315, 360, 1]])
Reclassify1 = Reclassify(Name2, "VALUE", RemapRange)
Reclassify1.save(Name3)
ap.AddMessage(Reclassify1.name + " has been created and saved to " + desWs2.baseName)

# Use map algebra to select areas with slopes between 5 and 20 degrees and western direction
slope2 = Slope(Name1)
SuitSlope = (slope2 >= 5) & (slope2 <= 20)
SuitAspect = Name3 = 4

Name4 = "Suitable"
SuitFinal = SuitSlope & SuitSlope
SuitFinal.save(Name4)
ap.AddMessage(SuitFinal.name + " has been created and saved to " + desWs2.baseName)

# Erase the Lakes from the Mun_Bundry Feature
ap.Erase_analysis("MUN_Bndry", "Lakes", "MUN_Bndry_NoLakes")

# Create zonal statistics tables for Hamilton municipalities, based on the list of rasters in the geodatabase
GDBRas = ap.ListRasters()
for rasts in GDBRas:
    desRastList = ap.Describe(rasts)
    newName = desRastList.baseName + "_Tab"
    ZonalStatisticsAsTable("MUN_Bndry_NoLakes", "NAME", rasts, newName)
    ap.AddMessage(newName + " has been created and saved to " + desWs2.baseName)

# Describe the properties of each raster in the geodatabase with print statements
for ras in GDBRas:
    ras = Raster(ras)
    print(ras.name + "'s maximum value is " + str(ras.maximum) + ".")
    print(ras.name + "'s band count is " + str(ras.bandCount) + ".")
    print(ras.name + " has " + str(ras.height) + " rows.")
    print(ras.name + " has " + str(ras.width) + " columns.")
    print(ras.name + " has a resolution of " + str(ras.meanCellHeight) + "in the Y direction.")
    print(ras.name + " has a resolution of " + str(ras.meanCellWidth) + "in the X direction.")
    print(ras.name + " has a pixel type of " + str(ras.pixelType) + ".")
    print(ras.name + "'s spatial reference is " + str(ras.spatialReference) + ".")
    print(ras.name + "'s spatial reference unit is " + str(ras.spatialReference.linearUnitName) + ".")
