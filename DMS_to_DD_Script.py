Latitude_D = int(input("Please input Latitude Degree: "))
Latitude_M = int(input("Please input Latitude Minute: "))
Latitude_S = float(input("Please input Latitude Second: "))
Longitude_D = int(input("Please input Longtitude Degree: "))
Longitude_M = int(input("Please input Longitude Minute: "))
Longitude_S = float(input("Please input Longitude Second: "))

if Latitude_D > 0:
    DD_Latitude = Latitude_D + (Latitude_M/60) +(Latitude_S/3600)
else:
    DD_Latitude = (Latitude_D*-1 + (Latitude_M/60) +(Latitude_S/3600))*-1
print("The DD Latitude is: " + str(DD_Latitude))

if Longitude_D > 0:
    DD_Longitude = Longitude_D + (Longitude_M/60) +(Longitude_S/3600)
else:
    DD_Longitude = (Longitude_D*-1 + (Longitude_M/60) +(Longitude_S/3600))*-1
print("The DD Longitude is: " + str(DD_Longitude))