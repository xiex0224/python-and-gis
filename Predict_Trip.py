import arcpy as ap

import os

# Part A
ap.env.workspace = "C:/student"
ap.env.overwriteOutput = True
ap.CreateFileGDB_management("C:/student", "Hamilton.gdb")
FD1 = ap.CreateFeatureDataset_management("C:/student/Hamilton.gdb", "Hamilton",
                                         "C:/student/HamiltonShapefiles/Bikeways.prj")
FD2 = ap.CreateFeatureDataset_management("C:/student/Hamilton.gdb", "Canada",
                                         "C:/student/DACensusShapefile/lda_000b16a_e.prj")
ap.env.workspace = "C:/student/HamiltonShapefiles"
feature_class = ap.ListFeatureClasses()
print(feature_class)
out_workspace = "C:/student/Hamilton.gdb/Hamilton"
for FC in feature_class:
    des1 = ap.Describe(FC)
    out_Feature = os.path.join(out_workspace, des1.baseName)
    ap.CopyFeatures_management(FC, out_Feature)
    ap.AddMessage(des1.baseName + " has been copies to Hamilton")

ap.env.workspace = "C:/student/DACensusShapefile"
feature_class1 = ap.ListFeatureClasses()
print(feature_class1)
out_workspace = "C:/student/Hamilton.gdb/Canada"
for FC1 in feature_class1:
    des2 = ap.Describe(FC1)
    out_Feature = os.path.join(out_workspace, des2.baseName)
    ap.CopyFeatures_management(FC1, out_Feature)
    ap.AddMessage(des2.baseName + " has been copies to Hamilton")
ap.env.workspace = "C:/student/DACensusData"
for csv in ap.ListFiles("*.csv"):
    des3 = ap.Describe(csv)
    ap.TableToDBASE_conversion(csv, "C:/student/Hamilton.gdb")
    ap.AddMessage(des3.baseName + " has been copies to Hamilton.gdb")
# Part B
ap.env.workspace = "C:/student/Hamilton.gdb/Hamilton"
ap.Select_analysis("SoBi_Service_Areas", "Core_Service_Area", "AREA_NAME = 'Core Service Area'")
extent = ap.Describe("Core_Service_Area").extent
ap.GenerateTessellation_management("C:/student/Hamilton.gdb/Hamilton" + "/CoreServiceArea_Hexagon", extent,
                                   "HEXAGON", "125664 SquareMeters")
ap.FeatureToPoint_management("CoreServiceArea_Hexagon", "C:/student/Hamilton.gdb/Hamilton/Core_Hexagon_centroids",
                             "CENTROID")

# Part C
ap.Select_analysis("Street_Centreline", "Major_roads", "ROAD_TYPE = 'Major'")
ap.Select_analysis("Street_Centreline", "Minor_roads", "Road_TYPE = 'Minor'")

ap.UnsplitLine_management("Major_roads", "C:/student/Hamilton.gdb/Hamilton/Major_Roads_Merge", "STREET_N_1")
ap.UnsplitLine_management("Major_roads", "C:/student/Hamilton.gdb/Hamilton/Major_Roads_Coincident", "STREET_NAM")
ap.Intersect_analysis(["Major_Roads_Merge", "Major_Roads_Coincident"], "Major_RoadsIntersect", "", "", "point")
ap.DeleteIdentical_management("Major_RoadsIntersect", ["STREET_N_1", "FID_Major_Roads_Merge"])
gdb = "C:/student/Hamilton.gdb"
ap.TabulateIntersection_analysis("CoreServiceArea_Hexagon", "GRID_ID", "Major_RoadsIntersect",
                                 gdb + "/Hexagon_Intersections")
ap.GenerateNearTable_analysis("Core_Hexagon_centroids", "Bikeways", gdb + "/NearBikeways")
ap.TabulateIntersection_analysis("CoreServiceArea_Hexagon", "GRID_ID", "Minor_roads", gdb + "/length_minor")

ap.env.workspace = "C:/student/Hamilton.gdb"
ap.JoinField_management("NearBikeways", "IN_FID", "Core_Hexagon_centroids", "ORIG_FID", "GRID_ID")
Table_list = ["Hexagon_Intersections", "NearBikeways", "length_minor"]
for table in Table_list:
    ap.JoinField_management("CoreServiceArea_Hexagon", "GRID_ID", table, "GRID_ID")

ap.env.workspace = "C:/student/Hamilton.gdb/Hamilton"
ap.AlterField_management("CoreServiceArea_Hexagon", "PNT_COUNT", "MajRdInt")
ap.AlterField_management("CoreServiceArea_Hexagon", "Near_DIST+"
                                                    "", "DisBikeway")
ap.AlterField_management("CoreServiceArea_Hexagon", "LENGTH", " LenMinRd")
delete_element = ["GRID_ID_1", "GRID_ID_2", "PERCENTAGE", "IN_FID", "NEAR_FID", "GRID_ID_12", "GRID_ID_12_13",
                  "PERCENTAGE_1"]
ap.DeleteField_management("CoreServiceArea_Hexagon", delete_element)

# Part D
ap.env.workspace = "C:/student/Hamilton.gdb/Canada"
ap.Select_analysis("lda_000b16a_e", "C:/student/Hamilton.gdb/Hamilton/Hamilton_DAs", "CDNAME = 'Hamilton'")

ap.env.workspace = "C:/student/Hamilton.gdb"
Dict = {"COL0": "GEO_UID", "COL1": "Province_code", "COL2": "Province_name", "COL3": "CD_code", "COL4": "CD_name",
        "COL5": "DA_name", "COL6": "Population",
        "COL7": "number_of_people_aged_15_to_64", "COL8": "NumHouseholds",
        "COL9": "MedIncome"}
for fieldName in Dict:
    ap.AlterField_management("DACensusData16", fieldName, Dict[fieldName])
ap.AddField_management("DACensusData16", "Total_HOU_Income", "DOUBLE")
ap.CalculateField_management("DACensusData16", "Total_HOU_Income", "!NumHouseholds! * !MedIncome!")

ap.AddField_management("Hamilton_DAs", "DAUID_1", "LONG")
ap.CalculateField_management("Hamilton_DAs", "DAUID_1", "!DAUID!")
ap.JoinField_management("Hamilton_DAs", "DAUID_1", "DACensusData16", "GEO_UID",
                        ["Province_code", "Province_name", "CD_code", "CD_name", "DA_name", "Population",
                         "number_of_people_aged_15_to_64", "NumHouseholds", "MedIncome", "Total_HOU_Income"])

ap.env.workspace = "C:/student/Hamilton.gdb/Hamilton"
ap.Select_analysis("LandUse", "Residential_Area", "LUClass = 'Residential'")
A = ap.ListFeatureClasses()
for lake in A:
    ap.Erase_analysis(lake, "Lakes", lake + "_Erase")
ap.Intersect_analysis(["Residential_Area_Erase", "Hamilton_DAs_Erase"], "ResHAM_Intersect")
ap.Dissolve_management("ResHAM_Intersect", "ResHAM_Dis", "DAUID",
                       [["Population", "First"], ["NumHouseholds", "First"], ["Total_HOU_Income", "First"]],
                       "MULTI_PART")

ap.env.workspace = "C:/student/Hamilton.gdb"
ap.TabulateIntersection_analysis("CoreServiceArea_Hexagon_Erase", "GRID_ID", "ResHAM_Dis", "Tabulate_Hexagon", "DAUID",
                                 ["FIRST_Population", "FIRST_NumHouseholds", "FIRST_Total_HOU_Income"])
ap.Statistics_analysis("Tabulate_Hexagon", "STAT_Hexagon", (["FIRST_Population", "SUM"], ["FIRST_NumHouseholds", "SUM"
                                                                                          ],
                                                            ["FIRST_Total_HOU_Income", "SUM"]), "GRID_ID")
ap.JoinField_management("CoreServiceArea_Hexagon_Erase", "GRID_ID", "STAT_Hexagon", "GRID_ID",
                        ["SUM_FIRST_Population", "SUM_FIRST_NumHouseholds", "SUM_FIRST_Total_HOU_Income"])

ap.env.workspace = "C:/student/Hamilton.gdb/Hamilton"
ap.management.AddFields("CoreServiceArea_Hexagon_Erase", [["PopDen", "DOUBLE"], ["MedIncHhldsW", "DOUBLE"]])
ap.CalculateField_management("CoreServiceArea_Hexagon_Erase", "PopDen",
                             "!SUM_FIRST_Population! / !Shape_Area! * math.pow(10, 6)")
ap.CalculateField_management("CoreServiceArea_Hexagon_Erase", "MedIncHhldsW",
                             "!SUM_FIRST_Total_HOU_Income! / !SUM_FIRST_NumHouseholds!")

# Part E
B = ["MajRdInt", "DisBikeway", "LenMinRd", "PopDen", "MedIncHhldsW"]
with ap.da.UpdateCursor("CoreServiceArea_Hexagon_Erase", B) as cursor:
    for row in cursor:
        new = [0 if x is None else x for x in row]
        cursor.updateRow(new)

ap.AddField_management("CoreServiceArea_Hexagon_Erase", "PredTrips", "DOUBLE")

ap.CalculateField_management("CoreServiceArea_Hexagon_Erase", "PredTrips",
                             "24.1387 - 0.0012 * !MajRdInt! - 0.0004 * !DisBikeway! +  0.0612 * !LenMinRd! + "
                             "0.0341 * !PopDen! + 0.0013 * !MedIncHhldsW!")

# Part F
ap.CopyRows_management("CoreServiceArea_Hexagon_Erase", "C:/student/Hamilton.gdb/WeeklyTrips")
ap.env.workspace = "C:/student/Hamilton.gdb"
ap.TableToExcel_conversion("WeeklyTrips", "WeeklyTrips.xls")
ap.AddMessage("Data processing has been completed")
