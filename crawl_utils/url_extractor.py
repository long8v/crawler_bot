from bs4 import BeautifulSoup
import requests
import time
import os
import pandas as pd
from urllib.parse import urljoin
from functools import reduce
from collections import defaultdict
from datetime import datetime
from crawl_utils.html_request import * 
from crawl_utils.main_site_extractor import *
from selenium import webdriver


def sub_pages(url, visited=set([]), show_javascript=False):
    '''
    input : url(str)
    output : list of tuples(text, href)
    
    get sub pages given url
    '''
    sub_pages = []
    java_pages = []
    if url.startswith("http"):
        parsed = parsing(url)
        if parsed:
            for _ in parsed.select('div'):
                if _.has_attr('onclick'):
                    try:
                        sub_pages.append((_.text, urljoin(url, _["onclick"].split("href=")[1].replace("'","").replace(";", ""))))
                    except:
                        pass
            for _ in parsed.select('a'):
                if _.has_attr("href") and "#" not in _["href"] and not is_portal(_["href"]):
                    if 'javascript' in _['href'].lower():
                        java_pages.append((url, _["href"]))
                    if _["href"] not in visited:
                        if _["href"].startswith('http'):
                            link = _["href"]    
                        else: 
                            link = urljoin(url, _["href"])
                        if not _.text.strip():
                            text = '_'.join([img["alt"] for img in _.find_all('img') 
                            if img.has_attr('alt') ])
                        else:
                            text = _.text
                        if text and link:
                            sub_pages.append((text, link))
                            visited.update([link])
    if java_pages and show_javascript:
        print(url, len(java_pages))
    return sub_pages, visited 




def get_sub_pages(main_pages, visited=set([])):
    '''
    input : {hspt: url}(DataFrane)
    output : list of tuples (text, lisf of urls)
    
    get sub pages given dictionary
    '''
    main_sub_pages = []
    for idx, page in main_pages.iterrows():
        hspt = page["hspt_name"]
        try:
            url = page["root_url"]
        except:
            url = page["url"]
        sub, visited = sub_pages(url, visited)
        main_sub_pages.append((hspt, sub))
    return main_sub_pages


def drop_duplicate_by_column(df, column):
    '''
    input : dataframe, column(str or list of str)
    output : dataFrame 
    
    drop rows having overlapped item in selected column 
    '''
    df_reduced = df.drop_duplicates(column)
    # print('deleted duplicated rows by {} : {} ->  {}'.format(column, df.shape[0], df_reduced.shape[0]))
    return df_reduced

