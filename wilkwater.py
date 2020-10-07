# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 20:38:44 2020

@author: huyng
"""

import requests as rq
import pandas as pd
import bs4
import json
from pathlib import Path



def get_soup(link):
    return bs4.BeautifulSoup(rq.get(link).content,'lxml')

def write_to_json(path, js):
    with open(path, 'w') as f:
        f.write(json.dumps(js,indent=2,sort_keys=True))
    return None

def go_back(soup):
    soup = soup.previous_sibling
    if type(soup) is not bs4.element.Tag:
        return go_back(soup)
    elif not soup.text:
        return go_back(soup)
    else:
        return soup

def get_table(soup):
    tables = soup.find_all('table', attrs={'class':'table table-striped',
                                           'data-apply-readmore-class':'table__readmore-wrapper--active'})
    js = {}
    for table in tables:
        if not table.parent.attrs: # edge case where parent div doesn't have attrs (Suplementary in Temporary Page)
            header = go_back(table.parent).text.strip().replace(u'\xa0', u' - ')
        elif table.parent['id'] == 'radePasteHelper': # hidden element
            continue
        else:
            header = go_back(table).text.strip().replace(u'\xa0', u' - ')
        df = pd.read_html(str(table))
        df = df[0]
        js[header] = json.loads(df.to_json(orient='records'))
    return js

perma_water = r'http://www.wilkswater.com.au/permanent-water'
temp_water = r'http://www.wilkswater.com.au/temporary-water'
forward_water = r'http://www.wilkswater.com.au/Water-Trading/forward-water'
carryover_water = r'http://www.wilkswater.com.au/Water-Trading/carryover-capacity'
leasing_water = r'http://www.wilkswater.com.au/Water-Trading/water-leasing'
df_delivery = r'http://www.wilkswater.com.au/Water-Trading/deferred-delivery'

if __name__ == '__main__':
    OUTPUT_PATH = Path.cwd() / 'output' / 'wilkwater'
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    temp = get_table(get_soup(perma_water))
    write_to_json(OUTPUT_PATH / 'perma_water.json', temp)
    print('Finished writing perma_water.json')

    temp = get_table(get_soup(temp_water))
    write_to_json(OUTPUT_PATH / 'temp_water.json', temp)
    print('Finished writing temp_water.json')

    temp = get_table(get_soup(forward_water))
    write_to_json(OUTPUT_PATH / 'forward_water.json', temp)
    print('Finished writing forward_water.json')

    temp = get_table(get_soup(carryover_water))
    write_to_json(OUTPUT_PATH / 'carryover.json', temp)
    print('Finished writing carryover.json')

    temp = get_table(get_soup(leasing_water))
    write_to_json(OUTPUT_PATH / 'leasing.json', temp)
    print('Finished writing leasing.json')
    
    temp = get_table(get_soup(df_delivery))
    write_to_json(OUTPUT_PATH / 'df_delivery.json', temp)
    print('Finished writing df_delivery.json')

