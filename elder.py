# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:33:17 2020

@author: huyng
"""

import requests as rq
import pandas as pd
import bs4
import json
from pathlib import Path
from collections import defaultdict

bs = bs4.BeautifulSoup
URL = r'https://eldersrural.com.au/water-trading/'

def go_back(soup):
    soup = soup.previous_sibling
    if type(soup) is not bs4.element.Tag:
        return go_back(soup)
    else:
        return soup
        
if __name__ == '__main__':
    json_output = defaultdict(list)
    OUTPUT_PATH = Path.cwd() / 'output' / 'elder'
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    soup = bs(rq.get(URL).content,'lxml')
    soup = soup.find('main',attrs={'id':'main'})
    groups = soup.find_all('section',attrs={'class':'section accordions'})
    for group in groups:
        header_top = go_back(group).text.strip()
        tables = group.find_all(attrs={'class':'panel panel-default'})
        for table in tables:
            header = table.find(attrs={'class':'panel-heading'}).text.strip()
            table_result = pd.read_html(str(table))
            table_result = [json.loads(df.to_json(orient='records')) for df in table_result]
            json_output[header_top].append({header:table_result})
    with open(OUTPUT_PATH / 'elder.json', 'w') as f:
        f.write(json.dumps(json_output,indent=2,sort_keys=True))
        print('Finished writing elder.json')
    
        
            
            