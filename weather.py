'''Unit3 Lesson2'''

import pandas as pd
import requests
import datetime
import sqlite3 as lite

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
    

# request_time = datetime.datetime.now() - datetime.timedelta(days=1)
request_time = datetime.datetime.now()
format_time = lambda x: x.strftime('%Y-%m-%dT%H:%M:%S')
request_time = format_time(request_time)

def data_structure():
    '''see how data from request is organized'''
    test_url = create_request_url('Austin', request_time)
    # test_url = create_request_url('Austin', request_time, ['minutely', 'hourly', 'daily', 'alerts', 'flags'])
    # test_url = create_request_url('Austin', request_time, ['minutely', 'hourly'])
    r = requests.get(test_url).json()
    # print(r.keys())
    try:
        # print(r['currently'].keys())
        # print(r['flags'].keys())
        # print(r['daily'].keys())
        # # print(r['daily']['data'])
        daily_keys = r['daily']['data'][0].keys()
        print(type(r['daily']['data'][0]))
        daily_keys.sort()
        for key in daily_keys:
            print(key)
        print('\n')
        # # print(r['daily']['data'][0].keys())
        # # print(r['currently']['summary'])
    except:
        print("Something didn't work, try again! :)")
    for city in cities.keys():
        r = requests.get(create_request_url(city, request_time)).json()
        max_temp = r['daily']['data'][0]['temperatureMax']
        print('{0}: {1}'.format(city, max_temp))
    
    
    
def create_weather_table():
    '''create the weather.db table'''
    con = lite.connect('weather.db')
    cur = con.cursor()
    with con:
        cur.execute('CREATE TABLE temperature_max (day INT PRIMARY KEY,\
Austin FLOAT, Chicago FLOAT, Denver FLOAT, New_York FLOAT, San_Fransisco FLOAT, Seattle FLOAT)')
    
    
def test_weather_table(con, cur):
    with con:
        cur.execute('INSERT INTO temperature_max VALUES (?,?,?,?,?,?,?)', (1, 10, 20, 30, 40, 50, 60))
        cur.execute('SELECT * FROM temperature_max')
        print(cur.fetchall())
        
        
def clean_table(con, cur, table):
    with con:
        cur.execute('DELETE FROM {0};'.format(table))
        cur.execute('VACUUM;')
    print('Table {0} cleaned'.format(table))
    
    
def get_temperature_max_from_last_30_days(con, cur):
    '''get the maximum temperature for each city for the past 30 days'''
    for delta_days in xrange(30):
        request_time = datetime.datetime.now() - datetime.timedelta(days=29-delta_days)
        time_key = int(request_time.strftime('%Y%m%d'))
        max_temp = {}
        print('Acquiring maximum temperatures for {0} ({1} days remaining)'.format(request_time.strftime('%Y-%m-%d'), 29-delta_days))
        for city in cities.keys():
            r = requests.get(create_request_url(city, format_time(request_time))).json()
            max_temp[city] = r['daily']['data'][0]['temperatureMax']
        with con:
            cur.execute('INSERT INTO temperature_max (day, Austin, Chicago, Denver, New_York, San_Fransisco, Seattle) \
            VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6})'.format(
            time_key, max_temp['Austin'], max_temp['Chicago'], max_temp['Denver'], max_temp['New York'], 
            max_temp['San Francisco'], max_temp['Seattle']))
    
    
    
def main():
    # data_structure()
    # create_weather_table()
    con = lite.connect('weather.db')
    cur = con.cursor()
    # test_weather_table(con, cur)
    # clean_table(con, cur, 'temperature_max')
    # get_temperature_max_from_last_30_days(con, cur)
    
    
main()