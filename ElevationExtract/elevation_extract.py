import arcpy

# Parameters
dem = arcpy.GetParameterAsText(0)
outputDB = arcpy.GetParameterAsText(1)
elevationStart = arcpy.GetParameterAsText(2)
elevationEnd = arcpy.GetParameterAsText(3)
clipExtent = arcpy.GetParameterAsText(4)
deleteFiles = arcpy.GetParameter(5)

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
elevationExtract_Clip = '{0}/Elevation_{1}_to_{2}_clip'.format(outputDB, elevStart, elevEnd)
elevationExtract_Final = '{0}/Elevation_{1}_to_{2}_final'.format(outputDB, elevStart, elevEnd)

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
arcpy.AddMessage('Polygon dissolved.')

# === 5. Clip polygon (Optional) ===
if clipExtent is not '':
    arcpy.AddMessage('Clipping polygon to clip extent...')
    arcpy.analysis.Clip(elevationExtract_Dis, clipExtent, elevationExtract_Clip)
    arcpy.AddMessage('Polygon clipped.')

# === 6. Rename the final feature ===
arcpy.AddMessage('Renaming feature class...')
if clipExtent is not '':
    arcpy.management.Rename(elevationExtract_Clip, elevationExtract_Final)
else:
    arcpy.management.Rename(elevationExtract_Dis, elevationExtract_Final)
arcpy.AddMessage('Feature class renamed.')

# === 7. Delete Features (Optional) ===
if deleteFiles is True:
    arcpy.AddMessage('Deleting unneeded feature classes...')
    arcpy.management.Delete([elevationExtract, elevationExtract_Int, elevationExtract_Poly])
    if clipExtent is not '':
        arcpy.management.Delete(elevationExtract_Dis)
    arcpy.AddMessage('Unneeded feature classes deleted.')

# === 8. Add an 'Acres' field to final polygon  ===
arcpy.AddMessage('Adding "Acres" field...')
arcpy.management.AddField(elevationExtract_Final, 'Acres', 'FLOAT')
arcpy.AddMessage('"Acres" field added.') 

# === 9. Calculate acres ===
arcpy.AddMessage('Calculating acres...')
arcpy.management.CalculateGeometryAttributes(elevationExtract_Final, [['Acres', 'AREA']], area_unit = 'ACRES')
arcpy.AddMessage('Acres calculated.')
