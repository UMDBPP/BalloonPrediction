'''
Created on Jan 17, 2018

@author: Zach
'''

import datetime

import requests

average_ascent_rate = 6.148983
average_burst_altitude = 26047.734976
average_sea_level_descent_rate = 6.040434


def request_prediction(launch_latitude, launch_longitude, launch_altitude=None,
                       launch_datetime=f'{datetime.datetime.now():%Y-%m-%dT%H:%M:%SZ}',
                       ascent_rate=average_ascent_rate, burst_altitude=average_burst_altitude,
                       sea_level_descent_rate=average_sea_level_descent_rate):
    if launch_altitude == None:
        launch_altitude_query = ''
    else:
        launch_altitude_query = f'launch_altitude={launch_altitude:f}&'

    # convert to 0 - 360 longitude
    if launch_longitude < 0:
        launch_longitude = launch_longitude + 360

    query_request = f'http://predict.cusf.co.uk/api/v1/?launch_latitude={launch_latitude:f}&launch_longitude={launch_longitude:f}&{launch_altitude_query:s}launch_datetime={launch_datetime:s}&ascent_rate={ascent_rate:f}&burst_altitude={burst_altitude:f}&descent_rate={sea_level_descent_rate:f}'

    query_result = requests.get(query_request)

    query_json = query_result.json()

    # check status code for error
    if query_result.status_code == 200:
        return (query_json)
    else:
        # raise exception if error found
        raise (Exception(
            f'{query_result.status_code} {query_json["error"]["type"]}: {query_json["error"]["description"]))}'))
