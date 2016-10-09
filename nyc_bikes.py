'''
Unit3 Lesson1: download, clean, store, and analyze data
'''

import requests # package that allows us to download data from any online ressource
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import sqlite3 as lite

def requests_json_basics():
    # r = requests.get('http://www.citibikenyc.com/stations/json')
    # print(r.text[:500])
    # print(r.json().keys())
    ds = requests.get('http://www.citibikenyc.com/stations/json').json()
    print('ds keys:', ds.keys())
    print('Execution time:', ds['executionTime'])
    # print(ds['stationBeanList'][0].keys())
    # station_names = set([entry['stationName'] for entry in ds['stationBeanList']])
    # print(station_names)

    '''to make sure we get all fields'''
    key_list = set()
    for station in ds['stationBeanList']:
        for k in station.keys():
            key_list.add(k)
    key_list = list(key_list)
    key_list.sort()
    print('\n')
    for k in key_list:
        print(k)
    
# requests_json_basics()
    
'''get data in a DataFrame:'''
# r = requests.get('http://www.citibikenyc.com/stations/json')
# df = json_normalize(r.json()['stationBeanList'])
df = json_normalize(requests.get('http://www.citibikenyc.com/stations/json').json()['stationBeanList'])
print(df.info())

def plot_data():
    fig = plt.figure('Histograms')
    
    ax1 = fig.add_subplot(221)
    ax1.hist(df.availableBikes)
    ax1.set_title('Available bikes')
    
    ax2 = fig.add_subplot(222)
    ax2.hist(df.availableDocks)
    ax2.set_title('Available Docks')
    
    ax3 = fig.add_subplot(223)
    ax3.hist(df.totalDocks)
    ax3.set_title('Total Docks')
    
    # plt.savefig('nyc_data_hist.png')
    plt.show()
    
# plot_data()
'''Few available bikes and few available docks could mean that many bikes are being currently used and
in many places the stations are full or almost full'''

def explore_data():
    # print(pd.Series.unique(df.statusValue))
    # print(len(pd.Series.unique(df.stationName))) #each row is a different station
    print('\nOut of {0} stations, {1} is/are in service and {2} is/are not in service.'.format(
    len(df.statusValue), len(df[df.statusValue == 'In Service']), len(df[df.statusValue != 'In Service'])))
    print('There is/are {0} test station(s).'.format(len(df[df.testStation == True])))
    print('Available bikes in all stations (in service and not in service):\n\tmean = {0}\n\tmedian = {1}'.format(
    round(df.availableBikes.mean(), 1), df.availableBikes.median()))
    print('Available bikes in stations that are in service:\n\tmean = {0}\n\tmedian = {1}'.format(
    round(df[df.statusValue=='In Service'].availableBikes.mean(), 1), df[df.statusValue=='In Service'].availableBikes.median()))
    # print('Available bikes in stations that are NOT in service:\n\tmean = {0}\n\tmedian = {1}'.format(
    # round(df[df.statusValue=='Not In Service'].availableBikes.mean(), 1), df[df.statusValue=='Not In Service'].availableBikes.median()))

    # print(pd.Series.unique(df.landMark))
    # print(len(df[df.landMark != '']))

    # print(pd.Series.unique(df.statusKey))
    # print(df[df.statusKey==3][:10]) # looks like statusKey = 1 for 'In Service', and =3 for 'Not In Service'

# explore_data()
    
'''The only fields likely to change are the availableBikes, availableDocks, statusValue, and the statusKey.
availableDocks can be determined from totalDocks - availableBikes
In this case, since our goal is to record the number of bikes available every minute for an hour across all of New York City, 
we're primarily interested in the number of available bikes, but we want to keep all this reference information as well.
We want to use 'id' as our key value'''

def create_reference_table():
    con = lite.connect('citi_bike.db')
    cur = con.cursor()
    with con:
        cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY,\
        totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT,\
        testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT)')
    
# create_reference_table()

def populate_table():
    con = lite.connect('citi_bike.db')
    cur = con.cursor()
    
    query = 'INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode,\
    testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'
    
    with con:
        for station in requests.get('http://www.citibikenyc.com/stations/json').json()['stationBeanList']:
            cur.execute(query, (station['id'], station['totalDocks'], station['city'], station['altitude'], station['stAddress2'], 
            station['longitude'], station['postalCode'], station['testStation'], station['stAddress1'], station['stationName'], 
            station['landMark'], station['latitude'], station['location']))
            
# populate_table()

def test():
    con = lite.connect('citi_bike.db')
    cur = con.cursor()
    
    with con:
        cur.execute('SELECT stationName FROM citibike_reference')
        print(cur.fetchall())

# test()

'''Because column names cannot start with a number in SQL, we must create column names from station is as "_ + station_id" '''
station_ids_temp = df['id'].tolist()
station_ids = ['_' + str(x) + ' INT' for x in station_ids_temp]

def create_availableBikes_table():
    pass

create_availableBikes_table()