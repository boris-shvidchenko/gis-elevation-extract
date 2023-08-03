import arcpy

# Parameters
dem = arcpy.GetParameterAsText(0)
outputDB = arcpy.GetParameterAsText(1)
elevationStart = arcpy.GetParameterAsText(2)
elevationEnd = arcpy.GetParameterAsText(3)
clipExtent = arcpy.GetParameterAsText(4)
deleteFiles = arcpy.GetParameterAsText(5)

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
arcpy.AddMessage('Extracting attributes...')
elevations = arcpy.sa.ExtractByAttributes(dem, sql)
elevations.save(elevationExtract)
arcpy.AddMessage('Attributes successfully extracted.')

# === 2. Convert raster to INT type ===
arcpy.AddMessage('Converting to type INT...')
elevations_int = arcpy.sa.Int(elevations)
elevations_int.save(elevationExtract_Int)
arcpy.AddMessage('Successfully converted to type INT.')

# === 3. Raster to Polygon ===
arcpy.AddMessage('Exporting to polygon...')
arcpy.conversion.RasterToPolygon(elevations_int, elevationExtract_Poly)
arcpy.AddMessage('Polygon exported.')

# === 4. Dissolve polygon ===
arcpy.AddMessage('Dissolving polygon...')
arcpy.management.Dissolve(elevationExtract_Poly, elevationExtract_Dis)
arcpy.AddMessage('Polygon dissolved')
 
# === 5. Clip polygon (Optional) ===

# === 6. Add/calculate an 'Acres' field to final polygon  ===

# === 7. Delete Features (Optional) ===

# ==============================

# test
# arcpy.AddMessage()
