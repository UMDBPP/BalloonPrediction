'''
Created on Jan 17, 2018

@author: Zach
'''

# Import system modules
import arcpy
import os

# Set environment settings
arcpy.env.workspace = r"B:\Workspaces\GIS\UMDBPP\launch_site_selection\projected"
arcpy.env.overwriteOutput = True
outWorkspace = r"B:\Workspaces\GIS\UMDBPP\launch_site_selection\projected_new"

for infc in arcpy.ListFeatureClasses():

        # Determine if the input has a defined coordinate system, can't project
        # it if it does not
    dsc = arcpy.Describe(infc)

    if dsc.spatialReference.Name == "Unknown":
        print('skipped this fc due to undefined coordinate system: ' + infc)
    else:
        # Determine the new output feature class path and name
        outfc = os.path.join(outWorkspace, infc)

        # Set output coordinate system
        outCS = arcpy.SpatialReference(4326)

        # run project tool
        arcpy.Project_management(infc, outfc, outCS)

        # check messages
        print(arcpy.GetMessages())
