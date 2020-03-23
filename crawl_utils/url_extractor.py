from bs4 import BeautifulSoup
import requests
import time
import os
import pandas as pd
from urllib.parse import urljoin
from functools import reduce
from collections import defaultdict
from datetime import datetime
from selenium import webdriver
from crawl_utils.html_request import * 
from crawl_utils.main_site_extractor import *


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

def sub(parsed, url, visited=set([]), start_root=True, get_option=False):
    '''
    input : parsed(dom)
    output : sub_pages(list), visited(set)

    get sub pages and visited set given dom 
    '''
    sub_pages = []
    for _ in parsed.select('div'):
        if _.has_attr('onclick'):
            try:
                sub_pages.append((_.text, \
                    urljoin(url, onclick_regular(_["onclick"]))))
            except:
                pass
    if get_option:
        for options in parsed.select('select'):
            driver = webdriver.Chrome()
            driver.get(url)
            for _ in options.select('option'):    
                sub_pages.append(setOption(driver, _['value']))

    for _ in parsed.find_all(['a', 'area', 'table']):
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
            if 'javascript' in _["href"].lower():
                druver = get_driver(url)
                script = _["href"].split('::')[1]
                driver.execute_script(script)
                sub_pages.append((script, driver.current_url))
    return sub_pages, visited


def sub_pages(url, visited=set([]), start_root=True, get_option=False):
    '''
    input : url(str)
    output : sub_pages(list), visited(set)
    
    get sub pages given url
    '''
    sub_pages = []
    java_pages = []
    if str(url).startswith("http"):
        parsed = parsing(url)
        if parsed:
            sub_pages, visited = sub(parsed, url, start_root=start_root, get_option=get_option)
            if not sub_pages:
                parsed = parsing_dynamic(url)
                sub_pages, visited = sub(parsed, url)
    return sub_pages, visited 



def get_sub_pages(main_pages, visited=set([]), start_root=True, get_option=False):
    '''
    input : {hspt: url}(DataFrane)
    output : list of tuples (text, lisf of urls)
    
    get sub pages given dictionary
    '''
    main_sub_pages = []
    for idx, page in main_pages.iterrows():
        try:
            hspt = page["hspt_name"]
        except:
            hspt = page["병원명"]
        try:
            url = page["root_url"]
        except:
            url = page["url"]
        sub, visited = sub_pages(url, visited, start_root=start_root, get_option=get_option)
        main_sub_pages.append((hspt, sub))
    return main_sub_pages

