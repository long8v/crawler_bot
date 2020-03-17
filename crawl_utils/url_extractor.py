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


def setOption(driver, option_value):
    '''
    input : driver(selenium.webdriver), option_value(str)
    output : text of option(str), url(str)

    using selenium, click option and get link of the result
    '''
    option = driver.find_element_by_xpath("//option[@value='" + str(option_value) + "']")
    option.click()
    try:
        option_text = option.text
    except:
        option_text = ''
    return (option_text, driver.current_url)

def onclick_regular(url):
    return url.split("href=")[1].replace("'","").replace(";", "")


def sub_pages(url, visited=set([]), start_root=True, see_option=False):
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
                        sub_pages.append((_.text, \
                            urljoin(url, onclick_regular(_["onclick"]))))
                    except:
                        pass
            if see_option:
                for options in parsed.select('select'):
                    driver = webdriver.Chrome()
                    driver.get(url)
                    for _ in options.select('option'):    
                        sub_pages.append(setOption(driver, _['value']))

            for _ in parsed.select('a'):
                if _.has_attr("href") and "#" not in _["href"] \
                and not is_portal(_["href"]) and 'javascript' not in _["href"].lower():
                    if _["href"].startswith('http'):
                        link = _["href"]    
                    else: 
                        link = urljoin(url, _["href"])
                    if not _.text.strip():
                        text = '_'.join([img["alt"] for img in _.find_all('img') 
                        if img.has_attr('alt') ])
                    else:
                        text = _.text
                    if link not in visited and text and link :
                        if start_root:
                            if html_re(url) in link:
                                sub_pages.append((text, link))
                                visited.update([link])
                        else:
                            sub_pages.append((text, link))
                            visited.update([link])

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

