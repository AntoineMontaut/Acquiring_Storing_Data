'''
Download data from http://www.citibikenyc.com/stations/json every minute and 
stores it in table available_bikes in database citi_bike.db
'''

import requests
import sqlite3 as lite
import datetime
from dateutil.parser import parse
import collections
import time
import pandas as pd

url = 'http://www.citibikenyc.com/stations/json'
db_name = 'citi_bike.db'
table_name = 'available_bikes'
avail_bikes = collections.defaultdict(int)
# stations = requests.get(url).json()['stationBeanList']
# id_list = []
# for station in stations:
    # id_list.append(station['id'])


def clean_table(db_name, table_name):
    '''remove all rows from the table'''
    con = lite.connect(db_name)
    cur = con.cursor()
    with con:
        cur.execute('DELETE FROM {0};'.format(table_name))
        cur.execute('VACUUM;')


def get_and_store_data():
    '''get execution time and download numbers of available bikes and store them into avail_bikes dictionary'''
    r = requests.get(url).json()
    exec_time = parse(r['executionTime'])
    epoch_time = int((exec_time - datetime.datetime(1970, 1, 1)).total_seconds())
    
    for station in r['stationBeanList']:
        avail_bikes[station['id']] = station['availableBikes']
        
    con = lite.connect(db_name) #could connect at start of main but I prefer not to leave the connexion to the db open for an hour
    cur = con.cursor()
    with con:
        cur.execute('INSERT INTO available_bikes (execution_time) VALUES ({0})'.format(epoch_time))
        for k, v in avail_bikes.iteritems():
            cur.execute('UPDATE available_bikes SET _{0}={1} WHERE execution_time={2};'.format(k, v, epoch_time))
    

def select_data():
    con = lite.connect(db_name)
    cur = con.cursor()
    with con:
        cur.execute('SELECT execution_time, _{}, _{}, _{} FROM available_bikes'.format(id_list[0], id_list[1], id_list[2]))
        print(cur.fetchall())
    
    
def test_timer():
    '''test timer method'''
    now = datetime.datetime.now()
    print('test_timer starting at: {0}'.format(now.strftime('%Hh %Mmin %Ssec')))
    i = 0
    start = time.time()
    while i < 5:
        time.sleep(5)
        print('\nCurrent time: {0}'.format(now.strftime('%Hh %Mmin %Ssec')))
        print('Time from start: {0}sec'.format(time.time() - start))
        i += 1

   
def main_acquire_for_1hr():
    '''acquire available bikes at stations every minute for 1 hour'''
    #CAUTION: clean_table() will erase all rows in the db!
    # clean_table(db_name, table_name) 
    
    print('Data acquisition starting...')
    entry = 0
    while entry < 60:
        start = time.time()
        now = datetime.datetime.now()
        print('\t{1}: processing entry {0}'.format(entry, now.strftime('%H:%M:%S')))
        entry += 1
        get_and_store_data()
        processing_time = time.time() - start
        time.sleep(60 - processing_time)
    print('End of data acquisition')
    
# main_acquire_for_1hr()
# select_data()


'''DATA ANALYSIS'''

def get_reference_for_station(station_id):
    '''Get reference info for a specific station and return a DataFrame with information'''
    con = lite.connect(db_name)
    cur = con.cursor()
    with con:
        cur.execute('SELECT * FROM citibike_reference WHERE id={0}'.format(station_id))
        cols = [desc[0] for desc in cur.description]
        df_ref = pd.DataFrame(cur.fetchall(), columns=cols)
    return df_ref


def sql_to_DataFrame():
    '''create a DataFrame with previously acquired data stored in database'''
    con = lite.connect(db_name)
    df = pd.read_sql_query('SELECT * FROM available_bikes ORDER BY execution_time', con, index_col='execution_time')
    stations = (df.columns.values)
    
    '''get activity for each station: both bikes in and bikes out count positively towards activity'''
    df_activity = abs(df - df.shift(1))
    # df_activity.loc[df.index[0]] = 0
    activity = df_activity.sum()
    def verification():
        print(df[[stations[0], stations[1], stations[2]]])
        print(activity[[stations[0], stations[1], stations[2]]])
    # verification()
    
    most_active_station = activity.idxmax()
    most_active_station_activity = int(activity[most_active_station])
    df_ref = get_reference_for_station(most_active_station[1:])
    print(df_ref.info())
    
    initial_time = int(df.index[0]) + 5*60*60 # because epoch time is at gmt 0 and time of acquisition was at gmt -5
    initial_time = datetime.datetime.fromtimestamp(initial_time) #+ datetime.datetime(1970, 1, 1)
    finish_time = int(df.index[-1]) + 5*60*60
    finish_time = datetime.datetime.fromtimestamp(finish_time)
    
    print('\nOn {0}, from {1} to {2}, the most active station was station {3} with a total activity of {4}.\n\
\nNote: activity is defined as the sum of the absolute value of the variation of the number of available bikes \
every minute for an hour.'.format(
    initial_time.strftime('%m-%d-%Y'), initial_time.strftime('%H:%M:%S'), finish_time.strftime('%H:%M:%S'),
    most_active_station[1:], most_active_station_activity))
    
    
    
    
def main_data_analysis():
    sql_to_DataFrame()
    
main_data_analysis()