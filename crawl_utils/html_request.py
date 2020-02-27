from bs4 import BeautifulSoup
import requests
import time
import os
import pandas as pd
from urllib.parse import urljoin
from functools import reduce
from collections import defaultdict
from difflib import SequenceMatcher

def download(url="https://www.google.com/search",params={},retries=3):
    """
    input : url(str), parameter(dict)
    output : resp(object)
    
    using requests, get object resp given url
    for robustness, if error is server error(500s), retry at most 3 times
    otherwise, print error name, error reason, and header
    """
    resp = None
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
    header = {"user-agent":user_agent}
    try:
        resp = requests.get(url,params=params,headers=header)
        resp.raise_for_status() #error/event 발생하면 except로 가게해라 
        resp.encoding = None
    except requests.exceptions.HTTPError as e:
        url = url.replace("http://", "https://")
        if e.response.status_code//100==5 and retries>0:
            print(retries)
            resp = download(url,params,retries-1)
        else: 
            print(e.response.status_code)
            print(e.response.reason)
            print(e.response.headers)
            print(url)
    except:
        print('{} : Error'.format(url))
        if retries > 0:
            print(retries)
            resp = download(url,params,retries-1)
        if retries == 0:
            print('failed to download {}'.format(url))
            resp = ''
            return resp
    return resp

def get_html_text(url):
    '''
    input : url(str)
    output : html(str)
    
    download url and get html text
    '''
    url = download(url)
    return url.text

def parsing(url):
    '''
    input : url(str)
    output : dom(object)
    
    get dom given url
    '''
    dom_text = get_html_text(url)
    dom = BeautifulSoup(dom_text, 'lxml')
    return dom

def html_parsing(df, query):
    '''
    input : dataframe, query(str)
    output : dataframe
    
    find rows having query from given data frame 
    '''
    df_query = df[df["text"].apply(lambda e: query in e)]
    print('{} have {} page'.format(df_query.shape[0], query))
    return df_query