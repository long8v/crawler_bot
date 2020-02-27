from bs4 import BeautifulSoup
import requests
import time
import os
import pandas as pd
from urllib.parse import urljoin
from functools import reduce
from collections import defaultdict
from difflib import SequenceMatcher
from datetime import datetime
from crawl_utils.html_request import * 

def query_re(query):
    '''
    input : query(str)
    input : query(str)

    delete things inside () including parenthsis
    '''
    par_open = query.find('(')
    par_close = query.find(')')
    return query.replace(query[par_open:par_close + 1], "")



def get_main_page(query):
    '''
    input : query(str)
    output : list of tuples(text, href)
    
    search from naver given query
    '''
    url = download("https://search.naver.com/search.naver?", params = {'query':query_re(query)})
    dom = BeautifulSoup(url.text,"lxml")
    hspt_top = lambda dom : list(zip([_["href"] for _ in dom.select('.nsite.section._nsiteTop dl dt a')],
                                [_.text for _ in dom.select('.nsite.section._nsiteTop dl dt b.hl')]))
    hspt_title_link = [(_["href"], _.text) for _ in dom.select('.title_link') if not is_portal(_["href"])]
    hspt_title_link += hspt_top(dom)
    return hspt_title_link




def get_main_page_dict(query_list):
    '''
    input : list of query(str)
    output : {query : list of url given url}(dict)
    
    get dictionary having main page list given query 
    '''
    return {query:get_main_page(query) for query in query_list}




def html_re(url): 
    '''
    input : full url(str)
    output : main url(str)
    
    regularization for finding main page
    '''
    main = "/".join(url.split('/')[:3])
    return main




def is_portal(url):
    '''
    input : url(str)
    output : boolean
    
    see whether url is not offical one but other portal site such as facebook
    '''
    portals = ['facebook', 'naver', 'saramin', 'jobplanet', 'instagram', 
               'coupang', '11st', 'incruit','blog', 'jobkorea', 'tistory', 'hidoc',
               'health.chosun', 'kakao', 'recruit', 'youtube', 'localmap', 'mediup',
               'hira', 'gailbo', 'modoodoc', 'kookje', 'news', 'foursquare',  
               'catch', 'e-gen', 'press', 'koreaknee', 'namu.wiki', 'gangseo.soul',
               'mgoon', 'fosquare', 'career', '/healthstory/', 'amc', 'youtu.be'
               ]
    return any(p in url for p in portals)


def similar(a, b):
    '''
    input : a(str), b(str)
    output : the number of string in common(int)
    
    betweetn two string, get the number of string in common
    '''
    return len(set(a).intersection(set(b)))




def get_valid_html(HSPT_URL):
    '''
    input :  {text : [(html, text of html), ... ]} (dict)
    output : {text, set of urls} (dict)
    
    get valid urls by using rule module 'similar' and 'is_portal' 
    and make them into dictionary
    '''
    HSPT_URL_VALID = {}
    for hspt, url_list in HSPT_URL.items():
        HSPT_URL_VALID.update({hspt:set((html_re(link), similar(name, hspt)) 
                                        for link, name in url_list 
                                        if similar(name, hspt) > 2
                                        and not is_portal(link))})
    return HSPT_URL_VALID



def sub_pages(url, visited=set([])):
    '''
    input : url(str)
    output : list of tuples(text, href)
    
    get sub pages given url
    '''
    sub_pages = []
    java_pages = []
    if url.startswith("http"):
        for _ in parsing(url).select('a'):
            if _.has_attr("href") and _.text.strip() \
            and "#" not in _["href"] and not is_portal(_["href"]): #and "javascript" not in _["href"]:
                if 'javascript' in _['href'].lower():
                    java_pages.append((url, _["href"]))
                if _["href"].startswith('http'):
                    link = _["href"]
                else: 
                    link = urljoin(url, _["href"])
                if link not in visited:
                    if link.startswith(html_re(url)):
                        sub_pages.append((_.text, link))
                        visited.update([link])
    if java_pages:
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



def concat_from_list(df_list):
    '''
    input : list having dataframes
    output : concatened dataframe
    
    concatenate dataframes from list 
    '''
    if len(df_list) > 1:
        return reduce(lambda a, b: pd.concat([a,b], axis=0), df_list)
    if df_list:
        return df_list[0]

"""
def drop_duplicate_by_column(df, column):
    '''
    input : dataframe, column(str or list of str)
    output : dataFrame 
    
    drop rows having overlapped item in selected column 
    '''
    df_reduced = df.drop_duplicates(column)
    print('deleted duplicated rows by {} : {} ->  {}'.format(column, df.shape[0], df_reduced.shape[0]))
    return df_reduced
"""

def get_html_table(main_sub_pages, depth=1):
    '''
    input : list having tuples (text, lisf of urls)
    output : DataFrame
    
    get html table having text from url, url, depth, url name
    '''
    HSPT_CHILDREN_URL_list = []
    for hspt, contents in main_sub_pages:
        HSPT_CHILDREN_URL = pd.DataFrame({'hspt_name':[], 'url':[],'depth':[],'text':[]})
        zipped = list(zip(*contents))
        if len(zipped):
            HSPT_CHILDREN_URL["text"] = list(zipped[0])
            HSPT_CHILDREN_URL["url"] = list(zipped[1])
            HSPT_CHILDREN_URL["depth"] = [depth for _ in range(len(contents))]
            HSPT_CHILDREN_URL["hspt_name"] = [hspt for _ in range(len(contents))]
            HSPT_CHILDREN_URL["date"] = [datetime.today().strftime('%y%m%d') for _ in range(len(contents))]
            HSPT_CHILDREN_URL_list.append(HSPT_CHILDREN_URL)
    return concat_from_list(HSPT_CHILDREN_URL_list)

