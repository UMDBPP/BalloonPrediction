"""
Created on May 21, 2018

@author: Zach
"""

import calendar
import datetime

from PyQt5.QtCore import QVariant
from qgis.core import QgsGeometry, QgsPoint, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsField, QgsFeature

from BalloonPrediction import CUSFPredictionAPI

spatial_reference = QgsCoordinateReferenceSystem()
spatial_reference.createFromSrsId(3452)  # EPSG:4326


def json_to_polylines(query_json, lines_feature_class, launch_location_name, predict_id):
    query_prediction = query_json['prediction']

    print(f'Using dataset {query_json["request"]["dataset"].replace("-", "").replace(":", "")[0:13]}')

    points = []

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

            point_object = QgsPoint(
                x=entry['longitude'], y=entry['latitude'], z=entry['altitude'], m=unix_timestamp)

            # add point to array
            points.append(point_object)

    # create polyline of points (cannot use parameter names here)
    polyline = QgsGeometry.fromPolyline(points)

    # add a feature
    feature = QgsFeature()
    feature.setGeometry(polyline)
    feature.setAttributes(
        [predict_id,
         launch_location_name,
         query_json['request']['launch_datetime'],
         query_json['request']['dataset'],
         query_json['request']['launch_longitude'],
         query_json['request']['launch_latitude'],
         query_json['request']['launch_altitude'],
         query_json['request']['ascent_rate'],
         query_json['request']['burst_altitude'],
         query_json['request']['descent_rate'],
         polyline.length()]
    )

    return feature


def create_polylines(workspace_dir, launch_datetime, output_feature_class, launch_locations):
    # create output feature class
    lines_layer = QgsVectorLayer(output_feature_class)

    lines_layer.startEditing()

    # create fields in new feature class
    lines_layer.addAttribute(QgsField("Name", QVariant.String))
    lines_layer.addAttribute(QgsField("Lnch_Time", QVariant.String))
    lines_layer.addAttribute(QgsField("Dataset", QVariant.String))
    lines_layer.addAttribute(QgsField("Lnch_Lon", QVariant.Double))
    lines_layer.addAttribute(QgsField("Lnch_Lat", QVariant.Double))
    lines_layer.addAttribute(QgsField("Lnch_Alt_m", QVariant.Double))
    lines_layer.addAttribute(QgsField("Ascnt_m_s", QVariant.Double))
    lines_layer.addAttribute(QgsField("Brst_Alt_m", QVariant.Double))
    lines_layer.addAttribute(QgsField("Dscnt_m_s", QVariant.Double))
    lines_layer.addAttribute(QgsField("Length_m", QVariant.Double))

    features = []

    # set predict Id
    current_predict_id = 1

    # populate fields for each launch location predict
    for name, launch_location in launch_locations.items():
        print(f'Getting prediction for {name}')
        query_json = CUSFPredictionAPI.request_prediction(launch_longitude=launch_location[0],
                                                          launch_latitude=launch_location[1],
                                                          launch_datetime=launch_datetime)

        features.append(json_to_polylines(query_json, output_feature_class, name, current_predict_id))

        current_predict_id += 1

    # insert polylines into layer
    lines_layer.addFeatures(features)

    # insert polyline
    lines_layer.commitChanges()
