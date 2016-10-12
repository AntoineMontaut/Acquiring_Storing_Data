'''Unit3 Lesson2'''

import pandas as pd
import requests
import datetime

cities = {"Austin": ['30.303936', '-97.754355'],
             "Chicago": ['41.837551', '-87.681844'],
             "Denver": ['39.761850', '-104.881105'],
             "New York": ['40.663619', '-73.938589'],
             "San Francisco": ['37.727239', '-123.032229'],
             "Seattle": ['47.620499', '-122.350876']}
             
dark_sky_key = '0a8ab052a6eac4bda7f97a4499e72166'

def create_request_url(city, time, exclude=[]):
    '''assemble the base API address, key, city location, and time
    API format: https://api.darksky.net/forecast/[key]/[latitude],[longitude],[time]
    time format: UNIX time or [YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]
    provide exclude as a list. Can contain: currently, minutely, hourly, daily, alerts, flags'''
    
    exclude = ','.join(exclude)
    
    if exclude == []:
        url = 'https://api.darksky.net/forecast/{0}/{1},{2},{3}'.format(
        dark_sky_key, cities[city][0], cities[city][1], time)
    else:
        url = 'https://api.darksky.net/forecast/{0}/{1},{2},{3}?exclude={4}'.format(
        dark_sky_key, cities[city][0], cities[city][1], time, exclude)
    
    return url
    

request_time = datetime.datetime.now() - datetime.timedelta(days=1)
format_time = lambda x: x.strftime('%Y-%m-%dT%H:%M:%S')
request_time = format_time(request_time)

def data_structure():
    '''see how data from request is organized'''
    test_url = create_request_url('Austin', request_time)
    # test_url = create_request_url('Austin', request_time, ['minutely', 'hourly', 'daily', 'alerts', 'flags'])
    # test_url = create_request_url('Austin', request_time, ['minutely', 'hourly'])
    r = requests.get(test_url).json()
    print(r.keys())
    try:
        print(r['currently'].keys())
        print(r['flags'].keys())
        print(r['daily'].keys())
        # daily_keys = r['daily']['data'][0].keys()
        # daily_keys.sort()
        # for key in daily_keys:
            # print(key)
        # print(r['daily']['data'][0].keys())
        # print(r['currently']['summary'])
    except:
        print("Something didn't work, try again! :)")
    

def main():
    # data_structure()
    
main()