
# import modules
import arcpy as ap
from arcpy.nax import *

# workspace
ap.env.workspace = "C:/student/Accessibility.gdb/HamiltonFCs"
ap.env.overwriteOutput = True

ap.Select_analysis("CommunityBoundaries_NoLakes", "FHamilton", "COMMUNITY_ = 'Hamilton'")
ap.Clip_analysis("Residential_DAs", "FHamilton", "ResDAs_FHamilton")

# Find grocery store
ap.Select_analysis("Stores", "Grocery_store", "USER_Primary_SIC_Description = 'Grocers-Retail'"
                                              "Or USER_Primary_SIC_Description = 'Food Products-Retail'"
                                              "Or USER_Primary_SIC_Description = 'Food Markets'")

# # Find convenience store
ap.Select_analysis("Stores", "Convenience_store", "USER_Primary_SIC_Description = 'Convenience Stores'")
ap.FeatureToPoint_management("ResDAs_FHamilton", "Res_ce", "CENTROID")

# # Measure 1, 2, 3 ,4
nds = "C:/student/Accessibility.gdb/HamiltonNetwork/HamNet_ND"
nd_layer_name = "HamNet_ND"

input_incident = "Res_ce"
input_fa = ["Convenience_store", "Grocery_store"]
ap.env.workspace = "C:/student/Accessibility.gdb"
A = ["Car", "Walk"]
for fc in input_fa:
    for mod in A:
        ap.env.overwriteOutput = True
        MakeNetworkDatasetLayer(nds, nd_layer_name)
        close = ClosestFacility(nds)
        close.travelMode = mod
        close.load(ClosestFacilityInputDataType.Incidents, "Res_ce")
        close.load(ClosestFacilityInputDataType.Facilities, fc)
        B = close.solve()
        B.export(ClosestFacilityOutputDataType.Routes, "C:/student/Accessibility.gdb/" + fc + "Close_" + mod)

# measure 5, 6, 7, 8
Z = ["Car", "Walk"]
for mod1 in Z:
    ap.env.overwriteOutput = True
    MakeNetworkDatasetLayer(nds, nd_layer_name)
    service_are = ServiceArea(nd_layer_name)
    service_are.timeUnits = TimeUnits.Minutes
    service_are.defaultImpedanceCutoffs = 5
    service_are.travelMode = mod1
    service_are.load(ServiceAreaInputDataType.Facilities, input_incident)
    C = service_are.solve()
    C.export(ServiceAreaOutputDataType.Polygons, "C:/student/Accessibility.gdb/Service_area_by_" + mod1)
target = ["C:/student/Accessibility.gdb/Service_area_by_Car", "C:/student/Accessibility.gdb/Service_area_by_Walk"]
ap.env.workspace = "C:/student/Accessibility.gdb/HamiltonFCs"
FF = ["Convenience_store", "Grocery_store"]
for ta in target:
    for F in FF:
        output = ap.Describe(ta).name
        ap.SpatialJoin_analysis(ta, F, "C:/student/Accessibility.gdb/" + output + F + "_num", "",
                                "", "", "COMPLETELY_CONTAINS")
ap.env.workspace = "C:/student/Accessibility.gdb"
in_data = "Res_ce"
in_field = "ORIG_FID"
join_table = ["Convenience_storeClose_Car", "Convenience_storeClose_Walk", "Grocery_storeClose_Car",
              "Grocery_storeClose_Walk"]
for join in join_table:
    ap.JoinField_management(in_data, in_field, join, "IncidentOID", ["Total_Minutes"])
join_2 = ["Service_area_by_CarConvenience_store_num", "Service_area_by_CarGrocery_store_num",
          "Service_area_by_WalkConvenience_store_num", "Service_area_by_WalkGrocery_store_num"]
for join2 in join_2:
    ap.JoinField_management(in_data, in_field, join2, "FacilityOID", ["Join_Count"])
Dict = {"Total_Minutes": "Convenience_store_close_by_car", "Total_Minutes_12": "Grocery_store_close_by_car",
        "Total_Minutes_1": "Convenience_store_close_by_walk", "Total_Minutes_12_13": "Grocery_store_close_by_walk",
        "Join_Count": "Convenience_store_by_Car_num", "Join_Count_1":
            "Grocery_store_by_Car_num", "Join_Count_12": "Convenience_store_by_Walk_num",
        "Join_Count_12_13": "Grocery_store_by_Walk_num"}
for field_name in Dict:
    ap.AlterField_management("Res_ce", field_name, Dict[field_name])
ap.CopyRows_management("Res_ce", "C:/student/Accessibility.gdb/Final_table")
ap.TableToExcel_conversion("Final_table", "Final_table.xls")
