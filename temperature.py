'''Unit3 Lesson2'''

import pandas as pd
import requests
import datetime
import sqlite3 as lite
import matplotlib.pyplot as plt

cities = {"Austin": ['30.303936', '-97.754355'],
             "Chicago": ['41.837551', '-87.681844'],
             "Denver": ['39.761850', '-104.881105'],
             "New_York": ['40.663619', '-73.938589'],
             "San_Francisco": ['37.727239', '-123.032229'],
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
Austin FLOAT, Chicago FLOAT, Denver FLOAT, New_York FLOAT, San_Francisco FLOAT, Seattle FLOAT)')
    
    
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
            cur.execute('INSERT INTO temperature_max (day, Austin, Chicago, Denver, New_York, San_Francisco, Seattle) \
            VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6})'.format(
            time_key, max_temp['Austin'], max_temp['Chicago'], max_temp['Denver'], max_temp['New_York'], 
            max_temp['San_Francisco'], max_temp['Seattle']))
    
    
def explore_data(con, cur):
    df = pd.read_sql_query('SELECT * FROM temperature_max ORDER BY day DESC;',
    con, index_col='day')
    # print(df.head())
    cities_list = cities.keys()
    cities_list.sort()
    
    fig = plt.figure('Histogram of maximum daily temperature over the 30 days preceding October 13th of 2016')
    for index in xrange(6):
        plt.subplot(2,3,index+1)
        plt.hist(df[cities_list[index]])
        plt.xlim([50, 100])
        mean_max_T = round(df[cities_list[index]].mean(),1)
        median_max_T = round(df[cities_list[index]].median(),1)
        plt.title('{0} (mean={1}F, median={2}F)'.format(cities_list[index], str(mean_max_T), str(median_max_T)))
    fig = plt.figure('Maximum temperature over the past 30 days preceding October 13th of 2016')
    for index in xrange(6):
        plt.subplot(2,3,index+1)
        days = [i for i in xrange(30)]
        plt.plot(days, df[cities_list[index]])
        plt.ylim([50, 100])
        plt.xlabel('# of days before October 13th of 2016')
        mean_max_T = round(df[cities_list[index]].mean(),1)
        median_max_T = round(df[cities_list[index]].median(),1)
        plt.title('{0} (mean={1}F, median={2}F)'.format(cities_list[index], str(mean_max_T), str(median_max_T)))
        plt.gca().invert_xaxis()
    plt.show()
    
    range_T = {}
    print('Overall temperature amplitude over the 30 days preceding October 13th of 2016:')
    for city in cities_list:
        range_T[city] = df[city].max() - df[city].min()
        print('\t-{0}: {1}F.'.format(
        city, round(range_T[city], 1)))
        
    daily_T_variation = abs(df - df.shift(-1))
    daily_T_variation_max = daily_T_variation.max()
    # print(df.head())
    # print(daily_T_variation.head())
    print('\nMaximum temperature variation from one day to the next over the 30 days preceding October 13th of 2016:')
    for city in cities_list:
        print('\t-{0}: {1}F.'.format(
        city, daily_T_variation[city].max()))
    print('\nThe city with the highest temperature variation from one day to the next over the past month is {0} with\
 a variation of {1}F.'.format(daily_T_variation_max.idxmax(), daily_T_variation_max[daily_T_variation_max.idxmax()]))
        
    
def main():
    # data_structure()
    # create_weather_table()
    con = lite.connect('weather.db')
    cur = con.cursor()
    # test_weather_table(con, cur)
    # clean_table(con, cur, 'temperature_max')
    # get_temperature_max_from_last_30_days(con, cur)
    explore_data(con, cur)
    
    con.close()
    
    
main()