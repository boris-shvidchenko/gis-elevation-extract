import arcpy

# Parameters
dem = arcpy.GetParameterAsText(0)
outputDB = arcpy.GetParameterAsText(1)
elevationStart = arcpy.GetParameterAsText(2)
elevationEnd = arcpy.GetParameterAsText(3)

# Formatted elevation variables
elevStart = int(round(float(elevationStart)))
elevEnd = int(round(float(elevationEnd)))

# SQL clause
sql = 'VALUE >= {0} AND VALUE <= {1}'.format(elevationStart, elevationEnd)

# Output feature class names
elevationExtract = '{0}/Elevation_{1}_to_{2}'.format(outputDB, elevStart, elevEnd)
elevationExtract_Int = '{0}/Elevation_{1}_to_{2}_int'.format(outputDB, elevStart, elevEnd)
elevationExtract_Poly = '{0}/Elevation_{1}_to_{2}_poly'.format(outputDB, elevStart, elevEnd)
elevationExtract_Dis = '{0}/Elevation_{1}_to_{2}_dis'.format(outputDB, elevStart, elevEnd)

# === 1. Extract by Attributes ===
elevations = arcpy.sa.ExtractByAttributes(dem, sql)
elevations.save(elevationExtract)

# === 2. Convert raster to INT type ===
elevations_int = arcpy.sa.Int(elevations)
elevations_int.save(elevationExtract_Int)

# === 3. Raster to Polygon ===
arcpy.conversion.RasterToPolygon(elevations_int, elevationExtract_Poly)

# === 4. Dissolve polygon ===
#arcpy.management.Dissolve(elevations_)




# ==============================
# test
arcpy.AddMessage(dem)
arcpy.AddMessage(outputDB)
