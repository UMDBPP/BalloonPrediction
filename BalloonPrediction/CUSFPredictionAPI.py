'''
Created on Jan 17, 2018

@author: Zach
'''

import datetime
import requests

average_ascent_rate = 6.438535
average_burst_altitude = 27366.13
average_sea_level_descent_rate = 6.387933


def request_prediction(launch_latitude, launch_longitude, launch_altitude=None,
                       launch_datetime='{:%Y-%m-%dT%H:%M:%SZ}'.format(datetime.datetime.now()),
                       ascent_rate=average_ascent_rate, burst_altitude=average_burst_altitude,
                       sea_level_descent_rate=average_sea_level_descent_rate):
    if launch_altitude == None:
        launch_altitude_query = ''
    else:
        launch_altitude_query = 'launch_altitude={:f}&'.format(launch_altitude)

    # convert to 0 - 360 longitude
    if launch_longitude < 0:
        launch_longitude = launch_longitude + 360

    query_request = 'http://predict.cusf.co.uk/api/v1/?launch_latitude={:f}&launch_longitude={:f}&{:s}launch_datetime={:s}&ascent_rate={:f}&burst_altitude={:f}&descent_rate={:f}'.format(
        launch_latitude, launch_longitude, launch_altitude_query, launch_datetime, ascent_rate, burst_altitude,
        sea_level_descent_rate)

    query_result = requests.get(query_request)

    query_json = query_result.json()

    # check status code for error
    if query_result.status_code == 200:
        return (query_json)
    else:
        # raise exception if error found
        raise (Exception('{} {}: {}'.format(query_result.status_code, query_json['error']['type'],
                                            query_json['error']['description'])))
