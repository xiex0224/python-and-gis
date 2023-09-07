import arcpy
arcpy.env.overwriteOutput = True
FeaturePathName = input("Feature path and name: ")
GeoPathName = input("Stored database Path and Name: ")
LinearUnit = input("Linear Unit(only meters and feet): ")
numBuffer = input("buffer number: ")
Radius = input("Radius of buffer: ")
increment = input("Increment: ")
x = int(numBuffer)
y = int(Radius)
z = int(increment)
listA = list(range(y, y + (x * z), z))
for element in listA:
    arcpy.MultipleRingBuffer_analysis(FeaturePathName, GeoPathName + "_" + str(element), [element], LinearUnit)
