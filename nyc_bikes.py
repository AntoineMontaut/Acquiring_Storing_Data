'''
Unit3 Lesson1: download, clean, store, and analyze data
'''

import requests # package that allows us to download data from any online ressource
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt

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
    
plot_data()
'''Few available bikes and few available docks could mean that many bikes are being currently used and
in many places the stations are full or almost full'''

