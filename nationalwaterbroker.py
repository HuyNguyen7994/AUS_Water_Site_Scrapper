# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 06:57:56 2020

@author: huyng
"""

import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs
from pathlib import Path

LOCATION = ['vic','sa','nsw']
URL_PERNAMENT = (f'http://nationalwaterbrokers.com.au/buysell-perm/{location}-perm/' for location in LOCATION)
URL_TEMPORARY = (f'http://nationalwaterbrokers.com.au/buysell-temp/{location}-temp/' for location in LOCATION)
URL_ENTITLEMENT = r'http://nationalwaterbrokers.com.au/entitlement-lease/'
URL_FORWARD = r'http://nationalwaterbrokers.com.au/forward-water/'
URL_CARRYOVER = r'http://nationalwaterbrokers.com.au/carry-over/'

OUTPUT_PATH = Path.cwd() / 'output' / 'nationalwaterbroker'
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    # Get Pernament 
    for url,loc in zip(URL_PERNAMENT,LOCATION):
        tables = pd.read_html(url)
        tables[0].to_csv(OUTPUT_PATH / f'pernament_forsales_{loc}.csv')
        tables[1].to_csv(OUTPUT_PATH / f'pernament_tobuy_{loc}.csv')
    
    # Get Temporary 
    for url,loc in zip(URL_TEMPORARY,LOCATION):
        tables = pd.read_html(url)
        zones = [soup.text for soup in bs(rq.get(url).text, 'lxml').find_all('h3')]
        temp = tables.pop()
        temp.to_csv(OUTPUT_PATH / f'temporary_tobuy_{loc}.csv')
        for table,zone in zip(tables,zones):
            table.to_csv(OUTPUT_PATH / f'temporary_forsales_{loc}_{zone}.csv')
        
    # Get Entitlement
    headers = ['available','wanted','sold']
    tables = pd.read_html(URL_ENTITLEMENT)
    for table,header in zip(tables,headers):
        table.to_csv(OUTPUT_PATH / f'entitlement_{header}.csv')
        
    # Get Forward
    headers = ['selling','buying']
    tables = pd.read_html(URL_FORWARD)
    for table,header in zip(tables,headers):
        table.to_csv(OUTPUT_PATH / f'forward_{header}.csv')
        
    # Get CarryOver
    headers = ['available','wanted']
    tables = pd.read_html(URL_CARRYOVER)
    for table,header in zip(tables,headers):
        table.to_csv(OUTPUT_PATH / f'carryover_{header}.csv')
        
        