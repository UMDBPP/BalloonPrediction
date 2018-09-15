"""
Created on Jan 22, 2018

@author: Zach
"""

import os
from collections import OrderedDict

# from BalloonPrediction import Processing_ArcPy
from BalloonPrediction import Processing_PyQGIS

# from BalloonPrediction import Processing_WKT

workspace_dir = r"B:\Workspaces\Python\BalloonPrediction\output"
launch_date = '2018-09-15'
launch_time = '08:30:00'
launch_timezone = '-05:00'
output_filename = 'prediction.shp'

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
    ('Everett Elementary School', [-78.358934, 40.004937, 314]),
    ('Westminster Elementary School', [-77.025882, 39.579275, 213])
])

if __name__ == '__main__':
    launch_datetime = f'{launch_date}T{launch_time}{launch_timezone}'

    # Processing_ArcPy.create_polylines(workspace_dir, output_filename, launch_datetime, launch_locations)
    Processing_PyQGIS.create_polylines(os.path.join(workspace_dir, output_filename), launch_datetime, launch_locations)
    # Processing_WKT.write_polylines_csv(os.path.join(workspace_dir, output_filename), launch_datetime, launch_locations)

    print('done')
