'''Unit3 Lesson2'''

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from HTMLParser import HTMLParser
import sqlite3 as lite
import matplotlib.pyplot as plt

def explore_soup(soup):
    # print(type(soup))
    # print(soup('table'))
    # for row in soup('table'):
        # print(row)
    # print(soup('table')[6])
    # print(soup('table')[11])
    tables = soup.findAll('table')
    print('URL contains {0} tables'.format(len(tables)))
    # for index in xrange(len(tables)):
        # print('Table #{0} contains {1} rows'.format(index, len(tables[index])))
    rows = tables[9].find_all('tr')
    print('{0} rows in table 9 contain the attribute "tr"'.format(len(rows)))
    # print(rows[3])
    # print(rows[4])
    # print(rows[-1])
    header = rows[3]
    data = rows[4:]
    
    # print(data[0])
    header_cols = header.find_all('td', text=True)
    for index in xrange(len(header_cols)):
        content = header_cols[index].find_all(text=True)
        print('Column #{0}: {1}'.format(index, content))
    for i in xrange(5):
        cols = data[i].find_all('td', text=True)
        content = []
        print cols
        for col in cols:
            content.append(col.find(text=True))
        print('Country: {0}, year: {1}, total: {2}, men: {3}, women: {4}'.format(content[0], content[1], content[-3], content[-2], content[-1]))
    
def create_education_table():
    '''create the weather.db table'''
    con = lite.connect('education.db')
    cur = con.cursor()
    with con:
        cur.execute('CREATE TABLE school_expectancy (Country TEXT PRIMARY KEY,\
Year INT, Men INT, Women INT, Total INT)')
        
        
def clean_table(con, cur, table):
    with con:
        cur.execute('DELETE FROM {0};'.format(table))
        cur.execute('VACUUM;')
    print('Table {0} cleaned'.format(table))
    
    
def table_to_DataFrame(soup):
    tables = soup.find_all('table')
    rows = tables[9].find_all('tr')
    data = {}
    data['countries'] = []
    data['year'] = []
    data['men'] = []
    data['women'] = []
    for row in rows[4:]:
        cols = row.find_all('td', text=True)
        try:
            data['countries'].append(str(cols[0].text))
        except:
            data['countries'].append('PROBLEM')
        data['year'].append(int(cols[1].text))
        try:
            data['men'].append(int(cols[-2].text))
        except:
            data['men'].append('N/A')
        try:
            data['women'].append(int(cols[-1].text))
        except:
            data['women'].append('N/A')
    df = pd.DataFrame.from_dict(data)
    # print(df[df['countries']=='PROBLEM'])
    # print(df[df['men']=='N/A'])
    df['countries'].loc[45] = "Cote d'Ivoire"
    df['men'].loc[101] = 10
    df['men'].loc[108] = 13
    df['men'].loc[113] = 11
    df['total'] = (df['men'] + df['women'])/2
    df.total = df.total.astype(int)
    df.countries = df.countries.astype(str)
    df.year = df.year.astype(int)
    df.men = df.men.astype(int)
    df.women = df.women.astype(int)
    print(df.info())
    return df
    
    
def store_to_table(df):
    con = lite.connect('education.db')
    cur = con.cursor()
    with con:
        cur.executemany('INSERT INTO school_expectancy (country, year, men, women, total) VALUES (?,?,?,?,?);', 
        ([(df['countries'].loc[i], df['year'].loc[i], df['men'].loc[i], df['women'].loc[i], df['total'].loc[i]) for i in xrange(183)]))
        
    con.close()
    print('Data saved to table')
      

def load_data_from_db():
    con = lite.connect('education.db')
    df = pd.read_sql_query('SELECT * FROM school_expectancy;', con)
    print('Data loaded')
    return df
        
    
def explore_data(df):
    mean_med = [(round(df[x].mean(),2), df[x].median()) for x in ['Men', 'Women', 'Total']]
    
    fig = plt.figure('Histogram of school expectancy accross 183 countries')
    plt.subplot(3,1,1)
    plt.hist(df.Men)
    plt.title('Men (mean = {0}years, median = {1}years)'.format(mean_med[0][0], mean_med[0][1]))
    plt.xlim([0,25])
    plt.subplot(3,1,2)
    plt.hist(df.Women)
    plt.title('Women (mean = {0}years, median = {1}years)'.format(mean_med[1][0], mean_med[1][1]))
    plt.xlim([0,25])
    plt.subplot(3,1,3)
    plt.hist(df.Total)
    plt.title('Total (mean = {0}years, median = {1}years)'.format(mean_med[2][0], mean_med[2][1]))
    plt.xlim([0,25])
    plt.show()
    
    
def load_gdp_data():
    df_gdp = pd.read_csv('GDP_data_clean.csv')
    # print(df_gdp.head())
    return df_gdp
    

# def save_gdp_to_db(df_gdp):
    # years = ' FLOAT,'.join(['_'+str(x) for x in range(1999, 2017)]) + ' FLOAT'
    # many_values = ','.join(['?' for i in xrange(20)])
    # con = lite.connect('education.db')
    # cur = con.cursor()
    # with con:
        # # cur.execute('CREATE TABLE gdp (Country TEXT PRIMARY KEY, Country_code TEXT, {0});'.format(years))
        # cur.executemany('INSERT INTO gdp (Country, Country_code, {0}) VALUES ({1});'.format(years, many_values), 
        # ([(df_gdp['Country Name'].loc[i], df_gdp['Country Code'].loc[i], df_gdp['1999'].loc[i], df_gdp['2000'].loc[i], df_gdp['2001'].loc[i], 
        # df_gdp['2002'].loc[i], df_gdp['2003'].loc[i], df_gdp['2004'].loc[i], df_gdp['2005'].loc[i], df_gdp['2006'].loc[i], df_gdp['2007'].loc[i], 
        # df_gdp['2008'].loc[i], df_gdp['2009'].loc[i], df_gdp['2010'].loc[i], df_gdp['2011'].loc[i], df_gdp['2012'].loc[i], df_gdp['2013'].loc[i], 
        # df_gdp['2014'].loc[i], df_gdp['2015'].loc[i], df_gdp['2016'].loc[i]) for i in xrange(len(df_gdp))]))
    
  
def compare_sle_gdp(df, df_gdp):
    df['gdp'] = 'NaN'
    for i in xrange(len(df)):
        try:
            df.gdp.loc[i] = float(df_gdp[df_gdp['Country Name'] == df.Country.loc[i]][str(df.Year.loc[i])].values)
        except:
            df.gdp.loc[i] = 'NaN'
    print(df)

    
def main():
    url = 'http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    # explore_soup(soup)
    # create_education_table()
    # df = table_to_DataFrame(soup)
    df = load_data_from_db()
    # clean_table(con, cur, 'school_expectancy')
    # store_to_table(df)
    # explore_data(df)
    df_gdp = load_gdp_data()
    # save_gdp_to_db(df_gdp)
    compare_sle_gdp(df, df_gdp)
    

main()