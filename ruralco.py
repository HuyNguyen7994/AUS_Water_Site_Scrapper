# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 14:36:22 2020

@author: huyng
"""

import base64
import json
import re
import requests as rq
from bs4 import BeautifulSoup as bs
from collections import Counter
from pathlib import Path

def decode_jb64(content):
    """Input: bytes representation of json in reponse object
    Decode following instruction in this document https://jb64.org/specification/
    Output: JSON"""
    content = content.split(b'\r\n')
    data = content[-1] # get the last bytes set
    data = data.split(b'.')
    data = data[:-1] # the last bytes are MD5 hex => ignore
    data = [datum.replace(b'_',b'/').replace(b'-',b'+') for datum in data]
    data = [datum.ljust((len(datum)//4+1)*4,b'=') for datum in data]
    data = [base64.b64decode(datum) for datum in data]
    data = [json.loads(datum.decode('ISO-8859-1')) for datum in data]
    return data

def generate_html():
    #inspect https://waterexchange.com.au/prelogin/js/prelogin.js to get id var
    rp = rq.get(r'https://waterexchange.com.au/prelogin/js/prelogin.js')
    text = rp.text
    var_list = ['temp_alloc_list', 'forward_alloc_list', 'perm_entitle_list',
                'perm_ent_lease_list', 'carryover_list']
    html_dict = {}
    for var in var_list:
        pattern = re.compile(f'var {var}=(\[.*?\]);', re.DOTALL)
        match = re.search(pattern,text)
        if match:
            result_list = eval(match.group(1))
            assert type(result_list) is list, f'{var=} returns non-list object upon evaluation'
            html_dict[var[:-5]] = result_list
        else:
            raise ValueError(f'Cannot find {var=} in prelogin site')
    return html_dict

def find_product_id():
    html_dict = generate_html()
    id_dict = {var:[] for var in html_dict} # prepare empty dict
    def is_a_and_has_id(tag):
        return tag.name == 'a' and tag.has_attr('id')
    for var in html_dict:
        html_list = html_dict[var]
        for html in html_list:
            soup = bs(html, 'lxml')
            id_list = [s['id'] for s in soup.find_all(is_a_and_has_id)]
            id_dict[var] += id_list
    id_ = Counter([sblst for lst in id_dict.values() for sblst in lst]).most_common(1)[0]
    assert id_[1] == 1, f"Non-unique {id_[0]=} found."
    return id_dict

def generate_link(skip_all=True,*args):
    id_dict = find_product_id()
    if not args:
        args = id_dict.keys()
    else:
        for market in args:
            assert market in id_dict, f"Invalid command. Accept: {', '.join(id_dict.keys())}"
    
    base_url = r'https://waterexchange.com.au/cgi-bin/zonetrade/TradingPlatform/Iframe?'
    id_all = ['999', '2999', '6999', '7999'] # permanent_market, forward, carryover, permanent_lease 
    
    for market in args:
        if market == 'temp_alloc':
            for id_ in id_dict[market]:
                yield market, id_, base_url + f'getMarketData=1&product={id_}'
        else:
            for id_ in id_dict[market]:
                if id_ in id_all and skip_all:
                    continue
                yield market, id_, base_url + f'getAuctionData=1&product={id_}'
        
if __name__ == '__main__':
    OUTPUT_PATH = Path.cwd() / 'output' / 'ruralco'
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    for market, id_, link in generate_link():
        rp = rq.get(link)
        js = decode_jb64(rp.content)
        SUBOUTPUT = OUTPUT_PATH / market
        SUBOUTPUT.mkdir(parents=True, exist_ok=True)
        with open(SUBOUTPUT / f'{id_}.json', 'w') as f:
            f.write(json.dumps(js,indent=2,sort_keys=True))
            print(f'Finished writing {market}/{id_}.json')
