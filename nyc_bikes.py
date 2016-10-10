'''
Download data from http://www.citibikenyc.com/stations/json every minute and 
stores it in table available_bikes in database citi_bike.db
'''

import requests
import sqlite3 as lite
import datetime
from dateutil.parser import parse
import collections

def clean_table():
    '''to clean the table available_bikes before 1hr-automated script is launched'''
    con = lite.connect('citi_bike.db')
    cur = con.cursor()
    with con:
        cur.execute('DELETE FROM available_bikes;')
        cur.execute('VACUUM;')
        
        cur.execute('SELECT execution_time FROM available_bikes')
        print(cur.fetchall())
        
# clean_table()

'''Initialize list of station ids'''
    
avail_bikes = collections.defaultdict(int)
    
def get_time_and_data():
    '''get execution time and download numbers of available bikes and store them into avail_bikes dictionary'''
    
    r = requests.get('http://www.citibikenyc.com/stations/json').json()
    exec_time = parse(r['executionTime'])
    print(exec_time)
    epoch_time = int((exec_time - datetime.datetime(1970, 1, 1)).total_seconds())
    
    for station in r['stationBeanList']:
        avail_bikes[station['id']] = station['availableBikes']
        
    pass
    
# get_time_and_data()