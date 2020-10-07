# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 15:59:05 2020

@author: huyng
"""

import requests as rq
import pandas as pd
import bs4
import json
from pathlib import Path

def get_zone_dict(soup):
    zone = soup.find_all('div', attrs={'class':'trade-system-tab'})
    z_dict = {}
    for z in zone:
        systemid = z['data-systemid']
        label = z.text
        z_dict[systemid] = label
    return z_dict

def get_table_temp_perma(soup):
    tables = soup.find_all('table')
    z_dict = get_zone_dict(soup)
    js_dict = {}
    for table in tables:
        df = pd.read_html(str(table))
        header = table.previous_sibling.text
        assert len(df) == 1, 'Corrupted table structure. More than 1 found.'
        df = df[0]
        df['Location'] = None # Zone is already used by the site. For no reason.
        _ , body = [t for t in table]
        for i,row in enumerate(body):
            assert df.iloc[i,0] == row.find('a')['data-tradeid'], 'DataFrame and HTML table are not aligned'
            df.iloc[i,-1] = ';'.join([z_dict[id_.split('-')[-1]] for id_ in row['class']])
        js_dict[header] = json.loads(df.to_json(orient='records'))
    return js_dict

def get_soup(link):
    return bs4.BeautifulSoup(rq.get(link).content,'lxml')

def get_table_forward(soup):
    tables = soup.find_all('table')
    js_dict = {}
    for table in tables:
        header = table.parent.parent.previous_sibling.text # go up 2 level
        df = pd.read_html(str(table))
        assert len(df) == 1, 'Corrupted table structure. More than 1 found.'
        df = df[0]
        js_dict[header] = json.loads(df.to_json(orient='records'))
    return js_dict
  
def get_table_last_trades(soup):
    tables = soup.find_all('table')
    js_dict = {}
    for table in tables:
        header = table.parent.previous_sibling.text # go up 1 level
        df = pd.read_html(str(table))
        assert len(df) == 1, 'Corrupted table structure. More than 1 found.'
        df = df[0]
        js_dict[header] = json.loads(df.to_json(orient='records'))
    return js_dict

def write_to_json(path, js):
    with open(path, 'w') as f:
        f.write(json.dumps(js,indent=2,sort_keys=True))
    return None

temp_water = r'https://www.keywater.com.au/temporary-water-market/'
perma_water = r'https://www.keywater.com.au/permanent-water-market/'
forward_water = r'https://www.keywater.com.au/water-market-opportunities/'
last_trades = r'https://www.keywater.com.au/last-trades/'
    
if __name__ == '__main__':
    OUTPUT_PATH = Path.cwd() / 'output' / 'keywater'
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    
    temp = get_table_temp_perma(get_soup(temp_water))
    write_to_json(OUTPUT_PATH / 'temp_water.json', temp)
    print('Finished writing temp_water.json')
    
    temp = get_table_temp_perma(get_soup(perma_water))
    write_to_json(OUTPUT_PATH / 'perma_water.json', temp)
    print('Finished writing perma_water.json')

    temp = get_table_forward(get_soup(forward_water))
    write_to_json(OUTPUT_PATH / 'forward_water.json', temp)
    print('Finished writing forward_water.json')

    temp = get_table_last_trades(get_soup(last_trades))
    write_to_json(OUTPUT_PATH / 'last_trades.json', temp)
    print('Finished writing last_trades.json')