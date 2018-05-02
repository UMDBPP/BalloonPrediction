"""
Created on Jan 22, 2018

@author: Zach
"""
import calendar
import datetime
from collections import OrderedDict

import arcpy

from BalloonPrediction import CUSFPredictionAPI

print 'Imported ArcPy'

workspace_dir = r"B:\Workspaces\Python\BalloonPrediction\output"
launch_datetime = '2018-03-31T08:00:00-05:00'
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

arcpy.env.workspace = workspace_dir
arcpy.env.overwriteOutput = True
spatial_reference = arcpy.SpatialReference(4326)


def json_to_points(query_json, lines_feature_class, launch_location_name, predict_id):
    query_prediction = query_json['prediction']

    print 'Using dataset {}'.format(query_json['request']['dataset'].replace('-', '').replace(':', '')[0:13])

    points = arcpy.Array()

    current_id = 0

    # add field values and make points for each entry
    for stage in query_prediction:
        for entry in stage['trajectory']:
            # convert to [-180, 180] longitude
            entry['longitude'] = entry['longitude'] - 360

            # get Unix timestamp from datetime
            date, time = entry['datetime'].split('T')
            year, month, day = date.split('-')
            hours, minutes, seconds = time.strip('Z').split(':')
            dt = datetime.datetime(
                int(year), int(month), int(day), int(hours), int(minutes), int(seconds[0:2]))
            unix_timestamp = calendar.timegm(dt.timetuple())

            point_object = arcpy.Point(
                ID=current_id, X=entry['longitude'], Y=entry['latitude'], Z=entry['altitude'], M=unix_timestamp)

            # add point to array
            points.add(point_object)

            current_id += 1

    # create polyline of points (cannot use parameter names here)
    predict_path = arcpy.Polyline(points, spatial_reference, True, True)

    # create insert cursor for entire row plus point geometry
    insert_cursor = arcpy.da.InsertCursor(
        lines_feature_class, ['Id', 'SHAPE@', 'Name', 'Lnch_Time',
                              'Dataset', 'Lnch_Lon', 'Lnch_Lat', 'Lnch_Alt_m',
                              'Ascnt_m_s', 'Brst_Alt_m', 'Dscnt_m_s', 'Length_m'])

    # insert current predict path as row
    insert_cursor.insertRow([
        predict_id,
        predict_path, launch_location_name, query_json['request']['launch_datetime'], query_json['request']['dataset'],
        query_json['request']['launch_longitude'], query_json['request']['launch_latitude'],
        query_json['request']['launch_altitude'],
        query_json['request']['ascent_rate'], query_json['request']['burst_altitude'],
        query_json['request']['descent_rate'], predict_path.getLength('GEODESIC')
    ])

    # remove lock from feature class
    del insert_cursor


if __name__ == '__main__':
    arcpy.management.CreateFeatureclass(workspace_dir, output_feature_class, 'POLYLINE', has_m='ENABLED',
                                        has_z='ENABLED', spatial_reference=spatial_reference)

    arcpy.management.AddField(output_feature_class, 'Name', 'TEXT', 50)
    arcpy.management.AddField(output_feature_class, 'Lnch_Time', 'TEXT', 20)
    arcpy.management.AddField(output_feature_class, 'Dataset', 'TEXT', 20)
    arcpy.management.AddField(output_feature_class, 'Lnch_Lon', 'DOUBLE', 10)
    arcpy.management.AddField(output_feature_class, 'Lnch_Lat', 'DOUBLE', 10)
    arcpy.management.AddField(output_feature_class, 'Lnch_Alt_m', 'DOUBLE', 10)
    arcpy.management.AddField(output_feature_class, 'Ascnt_m_s', 'DOUBLE', 10)
    arcpy.management.AddField(output_feature_class, 'Brst_Alt_m', 'DOUBLE', 10)
    arcpy.management.AddField(output_feature_class, 'Dscnt_m_s', 'DOUBLE', 10)
    arcpy.management.AddField(output_feature_class, 'Length_m', 'DOUBLE', 10)

    # set predict Id
    current_predict_id = 1

    for name, launch_location in launch_locations.iteritems():
        print 'Getting prediction for {}'.format(name)
        query_json = CUSFPredictionAPI.request_prediction(launch_longitude=launch_location[0],
                                                          launch_latitude=launch_location[1],
                                                          launch_datetime=launch_datetime)

        json_to_points(query_json, output_feature_class, name, current_predict_id)

        current_predict_id += 1

    #arcpy.management.Sort(output_feature_class, output_feature_class, 'Id')

    print 'done'
