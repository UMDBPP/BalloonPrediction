"""
Created on Jan 22, 2018

@author: Zach
"""

from collections import OrderedDict

import os

for var in os.environ:
    print("{}: {}".format(var, os.environ[var]))

# from BalloonPrediction import Processing_ArcPy
from BalloonPrediction import Processing_PyQGIS

workspace_dir = r"B:\Workspaces\Python\BalloonPrediction\output"
launch_date = '2018-05-22'
launch_time = '08:30:00'
launch_timezone = '-05:00'
output_feature_class = 'prediction.shp'

# longitude, latitude, elevation (meters)
launch_locations = OrderedDict([
    ('Clear Spring Elementary School', [-77.934144, 39.657178, 174.1]),
    ('Hagerstown Community College', [-77.672274, 39.629549, 166]),
    ('Valley Elementary School', [-77.547824, 39.359031, 161]),
    ('Waverly Elementary School', [-77.462469, 39.427118, 120]),
    ('Hancock Elementary School', [-78.196146, 39.699886, 172]),
    ('Emittsburg Elementary School', [-77.329201, 39.703497, 128]),
    ('James Buchanan Middle School', [-77.897955, 39.850029, 178]),
    ('Benjamin Chambers Elementary School', [-77.667712, 39.944190, 203]),
    ('Everett Elementary School', [-78.358934, 40.004937, 314])
])

if __name__ == '__main__':
    launch_datetime = '{}T{}{}'.format(launch_date, launch_time, launch_timezone)

    # Processing_ArcPy.create_polylines(workspace_dir, launch_datetime, output_feature_class, launch_locations)
    Processing_PyQGIS.create_polylines(workspace_dir, launch_datetime, output_feature_class, launch_locations)

    print('done')
