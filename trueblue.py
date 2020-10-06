# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 09:41:48 2020

@author: huyng
"""

import pandas as pd
import requests as rq
from collections import defaultdict
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
    raw_data = defaultdict(list)
    cur_header = ''
    for s in soup:
        header = s.find_all('h2')
        content = s.find_all('p')
        if header:
            cur_header = header[0].text
        if content and len(content) == 4:
            raw_data[cur_header].append([c.text for c in content])