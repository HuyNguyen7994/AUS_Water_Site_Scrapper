# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 22:05:56 2020

@author: huyng
"""

import pandas as pd
from pathlib import Path

URL_LISTING = r'https://docs.google.com/spreadsheets/d/e/2PACX-1vQNlBtj4a2VfqtPhYe5Vu4BtMgU3GQQMDX-9adW8PZsXoifiuZUN77mCzSZud4sUAacHAHwt2K93CTD/pubhtml'
URL_TRADE = r'https://docs.google.com/spreadsheets/d/e/2PACX-1vThODrBOr0sCNiRV2M9YnPA3TgTxbli2hNYQrlZVe_qFKFLyzp7A-PwQj4OqTTvf9rwnks5tglkVQxk/pubhtml'

OUTPUT_PATH = Path.cwd() / 'output' / 'h2ox'
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    # Get listing
    listing_tables = pd.read_html(URL_LISTING)
    print('Parsed listings table from source')
    
    # Clean listing
    for table, name in zip(listing_tables,
                           ('leases', 'forwards', 'entitlement')):
        table = table.iloc[:,1:] # drop redundant index column
        table.columns = table.iloc[0,:]
        table = table.iloc[1:,:]
        table = table.dropna(how='all')
        table.to_csv(OUTPUT_PATH / f'{name}.csv')
        print(f'Exported {name} table to csv file')
        
    # Get trade
    trade = pd.read_html(URL_TRADE)
    trade = trade[0]
    print('Parsed trade table from source')
    
    # Clean trade
    trade = trade.iloc[:,1:]
    trade.columns = trade.iloc[0,:]
    trade = trade.iloc[1:,:]
    trade = trade.dropna(how='all')
    trade.to_csv(OUTPUT_PATH / 'trade.csv')
    print('Exported trade table to csv file')
        
        
    
    
    

    

