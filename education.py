'''Unit3 Lesson2'''

from bs4 import BeautifulSoup
import requests
# import pandas as pd
# import datetime
# import sqlite3 as lite
# import matplotlib.pyplot as plt

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
        for col in cols:
            content.append(col.find(text=True))
        print('Country: {0}, year: {1}, total: {2}, men: {3}, women: {4}'.format(content[0], content[1], content[-3], content[-2], content[-1]))
    
    
        
    
    
def main():
    url = 'http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    explore_soup(soup)
    

main()