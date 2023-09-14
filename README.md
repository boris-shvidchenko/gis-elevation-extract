# gis-elevation-extract

Tool Name: Elevation Extract
Version: v1
Date: 20230912

This tool extracts elevation values from an existing Digital Elevation Model (DEM) and converts them into polygon feature classes. Optional clip extents can be applied to narrow down the area of extraction. Acreages are also calculated and added to the attributes of the resulting elevation polygons.

========================================

Workflow:

There are 9 total steps that are run in order to complete the process, 2 of which are optional.

  1. Extract by Attributes 

    This step scans the input raster and extracts cell values that match the user defined criteria. In the case of this tool, the elevation ranges of the DEM. The output is a new raster.

  2. Raster to Int

    The raster created in the previous step is converted to a raster of type Int (Integer), which will allow step 3 (Raster to Polygon) to run.

  3. Raster to Polygon

    The new raster is converted into a polygon.

  4. Dissolve

    In order to reduce the number of individual sections that the newly created polygon has, the dissolve tool is run. 

  5. Clip (Optional)

    If the user selected a clip extent, the dissolved elevation polygon is clipped.

  6. Rename

    The elevation polygon is then renamed to include a '_final' suffix.

  7. Delete (Optional)

    If the user selected 'Delete Output Files?', all feature classes that were created by the tool and aren't needed are deleted. Only the final elevation polygon will remain. 

  8. Add Acres Field

    A new field is added to the final elevation polygon and will store area (acre) information.

  9. Calculate Geometry

    The acreage of the newly created polygon is calculated and added to the field, created in step 8 above, in the attribute table. 

========================================

How to use:

Add the 'ElevationExtract' folder to your ArcPro project by right clicking on 'Folders' in the Catalog pane and selecting 'Add Folder Connection'. The folder contains 3 items: this README file, an empty 'Data' geodatabase to optionally store your resulting elevation polygons in, and the ElevationExtract toolbox which holds the tool script. To use the tool, double click the 'Elevation Extract' script in the toolbox. For the 'DEM' parameter select a digial elevation model raster to extract elevations from and for 'Output Database' select the geodatabase that will hold the resulting data, including the final elevation polygon. Any normal geodatabase can be used, including the 'Data' geodatabase that is provided with this tool. For 'Elevation Start' and 'Elevation End' enter a starting and ending elevation. Please be certain that the chosen elevation values are included in the DEM (if the input DEM has a range of -10 to 100, do not select a value outside of this range such as -15 or 120). Decimals, negatives, and whole numbers can be used as starting and ending values. The 'Clip Extent' parameter is optional and can include a polygon feature class that will define the clipping extent of the elevation polygon. In other words the resulting elevation polygon will be 'clipped' to be inside of the selected clip extent feature class. 'Delete Output Files?' is another optional parameter. If selected, all unnecessary features that are created by the tool will be deleted once the tool completes running. Note that the final elevation polygon will not be deleted. By default this parameter is unchecked. 

Once the parameters have been selected, click 'Run' in the bottom right corner of the window. Once the tool finishes running the elevation polygons will be added to the geodatabase that was selected by the user. A refresh of the geodatabase may be required in order to see the newly added polygon feature classes.
