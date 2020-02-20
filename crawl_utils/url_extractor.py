from bs4 import BeautifulSoup
import requests
import time
import os
import pandas as pd
from urllib.parse import urljoin
from functools import reduce
from collections import defaultdict
from difflib import SequenceMatcher
from crawl_utils.html_request import * 

def get_main_page(query):
    '''
    input : query(str)
    output : list of tuples(text, href)
    
    search from naver given query
    '''
    url = download("https://search.naver.com/search.naver?", params = {'query':query})
    dom = BeautifulSoup(url.text,"lxml")
    hspt_top = lambda dom : list(zip([_["href"] for _ in dom.select('.nsite.section._nsiteTop dl dt a')],
                                [_.text for _ in dom.select('.nsite.section._nsiteTop dl dt b.hl')]))
    hspt_title_link = [(_["href"], _.text)                        for _ in dom.select('.title_link') if not is_portal(_["href"])]
    hspt_title_link += hspt_top(dom)
    return hspt_title_link




def get_main_page_dict(query_list):
    '''
    input : list of query(str)
    output : {query : lis of url given url}(dict)
    
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
    portals = ['facebook', 'naver', 'saramin', 'jobplanet', 'facebook', 
               'coupang', '11st', 'incruit','blog', 'jobkorea', 'tistory', 'hidoc']
    return any(p in url for p in portals)




def similar(a, b):
    '''
    input : a(str), b(str)
    output : the number of string in common(int)
    
    betweetn two string, get the number of string in common
    '''
    return SequenceMatcher(None, a, b).get_matching_blocks()[0]




def get_valid_html(HSPT_URL):
    '''
    input :  list of tuples (text, href)
    output : {text, set of urls} (dict)
    
    get valid urls by using rule module 'similar' and 'is_portal' 
    and make them into dictionary
    '''
    HSPT_URL_VALID = {}
    for hspt, url_list in HSPT_URL.items():
        HSPT_URL_VALID.update({hspt:set(html_re(link) for link, name in url_list 
                                        if similar(name, hspt).size > 2
                                        and not is_portal(link))})
    return HSPT_URL_VALID



def sub_pages(url):
    '''
    input : url(str)
    output : list of tuples(text, href)
    
    get sub pages given url
    '''
    return [(_.text.strip(), _["href"])
            for _ in parsing(url).select('a') 
            if _.has_attr("href") 
            and _.text.strip()
            and "#" not in _["href"]
            and "javascript" not in _["href"]]




def get_sub_pages(main_pages):
    '''
    input : {hspt, list of url}(dict)
    output : list of tuples (text, lisf of urls)
    
    get sub pages given dictionary
    '''
    main_sub_pages = []
    for hspt, url in main_pages.items():
        for u in url:
            main_sub_pages.append((hspt, sub_pages(u)))
    return main_sub_pages



def root_path_join(row, main_pages):
    '''
    input : row from HSPT_CHILDREN_URL(Series)
    output : path(str)
    
    made in order to do 'apply' in axis 1
    if html is made of relative url, make it absolute by joining with root url   
    '''
    url = row["url"]
    hspt = row["hspt"]
    if not url.startswith("http"):
        return urljoin(main_pages[hspt][0][0], url)
    return url



def get_html_table(main_sub_pages, main_pages):
    '''
    input : list having tuples (text, lisf of urls)
    output :list of DataFrame
    
    get html table having text of url, url, depth, url name(hspt)
    we will list these dataframes into list
    '''
    HSPT_CHILDREN_URL_list = []
    for hspt, contents in main_sub_pages:
        HSPT_CHILDREN_URL = pd.DataFrame({'hspt':[], 'url':[],'depth':[],'text':[]})
        zipped = list(zip(*contents))
        if len(zipped):
            HSPT_CHILDREN_URL["text"] = list(zipped[0])
            HSPT_CHILDREN_URL["url"] = list(zipped[1])
            HSPT_CHILDREN_URL["depth"] = [1 for _ in range(len(contents))]
            HSPT_CHILDREN_URL["hspt"] = [hspt for _ in range(len(contents))]
            HSPT_CHILDREN_URL["full_url"] = HSPT_CHILDREN_URL.apply(lambda row: \
                root_path_join(row, main_pages), axis=1)
            HSPT_CHILDREN_URL_list.append(HSPT_CHILDREN_URL)
    return HSPT_CHILDREN_URL_list


def concat_from_list(df_list):
    '''
    input : list having dataframes
    output : concatened dataframe
    
    concatenate dataframes from list 
    '''
    return reduce(lambda a, b: pd.concat([a,b], axis=0), df_list)



def drop_duplicate_by_column(df, column):
    '''
    input : dataframe, column(str or list of str)
    output : dataFrame 
    
    drop rows having overlapped item in selected column 
    '''
    df_reduced = df.drop_duplicates(column)
    print('{} ->  {}'.format(df.shape[0], df_reduced.shape[0]))
    return df_reduced

