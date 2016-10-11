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

url = 'http://www.citibikenyc.com/stations/json'
db_name = 'citi_bike.db'
table_name = 'available_bikes'
avail_bikes = collections.defaultdict(int)


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
        cur.execute('SELECT execution_time, _{}, _{}, _{} FROM available_bikes'.format(avail_bikes.keys()[0], avail_bikes.keys()[1], avail_bikes.keys()[2]))
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

   
def main():
    '''main'''
    #CAUTION: clean_table() will erase all rows in the db!
    clean_table(db_name, table_name) 
    
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
    
    
    
main()
# select_data()
# test_timer()