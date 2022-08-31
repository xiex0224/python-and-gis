import arcpy as ap

ap.env.workspace = "C:/student/Pedestrian Injuries.gdb"
ap.env.overwriteOutput = True
fc = "Census"
out_feature = "C:/student/Pedestrian Injuries.gdb/Census_Project"
out_coordinate_system = ap.SpatialReference('NAD 1983 UTM Zone 17N')
ap.Project_management(fc, out_feature, out_coordinate_system)

fc1 = "CensusTracts_1"
ap.Select_analysis(fc1, "Toronto_CTs", "CMANAME = 'Toronto'")
fc2 = "Toronto_CTs"
ap.AddField_management(fc2, "Area", "Double")
ap.CalculateField_management(fc2, "Area", "!Shape_Area!")
fc3 = "CensusData"
ap.AddField_management(fc3, "CTT_ID", "Text")
ap.CalculateField_management(fc3, "CTT_ID", "!CT_ID!")
ap.JoinField_management(fc2, "CTUID", fc3, "CTT_ID", ["POP", "HHINC_MED"])
fc4 = "Pedestrians"
ap.AddField_management(fc4, "Period", "Text")
ap.AddField_management(fc4, "Time_1", "Long")
ap.CalculateField_management(fc4, "Time_1", "!Time!")
with ap.da.UpdateCursor(fc4, ["Period", "Time_1"]) as time_cursor:
    for row in time_cursor:
        if 600 <= row[1] <= 859:
            row[0] = "Morning Peak"
        elif 900 <= row[1] <= 1559:
            row[0] = "Day"
        elif 1600 <= row[1] <= 1859:
            row[0] = "Evening Peak"
        else:
            row[0] = "Night"
        time_cursor.updateRow(row)
ap.AddField_management(fc4, "Morning_Peak", "Long")
ap.AddField_management(fc4, "Day", "Long")
ap.AddField_management(fc4, "Evening_Peak", "Long")
ap.AddField_management(fc4, "Night", "Long")
with ap.da.UpdateCursor(fc4, ["Morning_Peak", "Period"]) as count_cursor:
    for row1 in count_cursor:
        if row1[1] == "Morning Peak":
            row1[0] = 1
        else:
            row1[0] = 0
        count_cursor.updateRow(row1)
with ap.da.UpdateCursor(fc4, ["Day", "Period"]) as count_cursor1:
    for row2 in count_cursor1:
        if row2[1] == "Day":
            row2[0] = 1
        else:
            row2[0] = 0
        count_cursor1.updateRow(row2)

with ap.da.UpdateCursor(fc4, ["Evening_Peak", "Period"]) as count_cursor2:
    for row3 in count_cursor2:
        if row3[1] == "Evening Peak":
            row3[0] = 1
        else:
            row3[0] = 0
        count_cursor2.updateRow(row3)

with ap.da.UpdateCursor(fc4, ["Night", "Period"]) as count_cursor3:
    for row4 in count_cursor3:
        if row4[1] == "Night":
            row4[0] = 1
        else:
            row4[0] = 0
        count_cursor3.updateRow(row4)
ap.SpatialJoin_analysis(fc4, fc2, "Join_data")
ap.DeleteField_management("Join_data", ["Join_Count", "Target_FID", "Index_", "CMATYPE"])
ap.Delete_management(fc2, fc4)
ap.Delete_management("Census_Project")
ap.TableToExcel_conversion("Join_data", "Join_data.xls")
