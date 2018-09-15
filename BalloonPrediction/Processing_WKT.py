"""
Created on May 21, 2018

@author: Zach
"""

from BalloonPrediction import CUSFPredictionAPI


def json_to_csv_line(query_json, launch_location_name, predict_id):
    query_prediction = query_json['prediction']

    print(f'Using dataset {query_json["request"]["dataset"].replace("-", "").replace(":", "")[0:13]}')

    points = []

    # add field values and make points for each entry
    for stage in query_prediction:
        for entry in stage['trajectory']:
            # convert to [-180, 180] longitude
            entry['longitude'] = entry['longitude'] - 360

            point_entry = (entry['longitude'], entry['latitude'], entry['altitude'])

            # add point to array
            points.append(point_entry)

    polyline_wkt = f'POLYLINE ({",".join([" ".join(entry) for entry in points])})'

    csv_line = ','.join([launch_location_name,
                         polyline_wkt, query_json['request']['launch_datetime'],
                         query_json['request']['dataset'],
                         query_json['request']['launch_longitude'],
                         query_json['request']['launch_latitude'],
                         query_json['request']['launch_altitude'],
                         query_json['request']['ascent_rate'],
                         query_json['request']['burst_altitude'],
                         query_json['request']['descent_rate']
                         ])

    return csv_line


columns = ['Name', 'geom', 'Launch_Time', 'Dataset', 'Launch_Longitude', 'Launch_Latitude', 'Launch_Altitude_m',
           'Ascent_Rate_m_s', 'Burst_Altitude_m', 'Descent_Rate_m_s']


def write_polylines_csv(output_filename, launch_datetime, launch_locations):
    with open(output_filename, 'w') as output_text_file:
        output_text_file.write('')

        # set predict Id
        current_predict_id = 1

        # populate fields for each launch location predict
        for name, launch_location in launch_locations.items():
            print(f'Getting prediction for {name}')
            query_json = CUSFPredictionAPI.request_prediction(launch_longitude=launch_location[0],
                                                              launch_latitude=launch_location[1],
                                                              launch_datetime=launch_datetime)

            output_text_file.write(json_to_csv_line(query_json, name, current_predict_id))
