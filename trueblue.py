# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 09:41:48 2020

@author: huyng
"""

import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs
from pathlib import Path

URL_PERNAMENT = r'https://truebluewaterexchange.com/permanent-water/'
URL_TEMPORARY = r'https://truebluewaterexchange.com/temporary-water/'

OUTPUT_PATH = Path.cwd() / 'output' / 'trueblue'
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    # Get Pernament
    soup = bs(rq.get(URL_PERNAMENT).text, 'lxml')
    soup = soup.find('div', attrs={'class':'rtd'})
    soup = soup.find_all('div',recursive=False)
    df = []
    cur_category = ''
    for s in soup:
        category = s.find_all('h2')
        content = s.find_all('p')
        if category:
            cur_category = category[0].text
        if content and len(content) == 4:
            row = [c.text for c in content]
            row.append(cur_category)
            df.append(row)
    df = pd.DataFrame(df)
    df.columns = df.iloc[0,:]
    df = df.iloc[1:,:]
    df.columns = [*df.columns[:-1], 'Buyers/Sellers?']
    df.to_csv(OUTPUT_PATH / 'pernament.csv')
    
    # Get Temporary
    soup = bs(rq.get(URL_TEMPORARY).text, 'lxml')
    soup = soup.find('div', attrs={'class':'rtd'})
    soup = soup.find_all('div',recursive=False)
    df = []
    cur_category = ''
    saved_column = []
    for s in soup:
        category = s.find_all('h2')
        content = s.find_all('p')
        column = s.find_all('h4')
        if category:
            cur_category = category[0].text
        elif content and len(content) == 4:
            row = [c.text for c in content]
            row.append(cur_category)
            df.append(row)
        elif column and len(column) == 4:
            saved_column = [c.text for c in column]

    df = pd.DataFrame(df)
    df.columns = saved_column + ['Buyers/Sellers?']
    df.to_csv(OUTPUT_PATH / 'temporary.csv')
    
    
    
    
            