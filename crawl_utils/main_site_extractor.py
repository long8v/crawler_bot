from bs4 import BeautifulSoup
import requests
import time
import re
import pandas as pd
from urllib.parse import urljoin
from functools import reduce
from datetime import datetime
from crawl_utils.html_request import * 
from selenium import webdriver


def redirect(url):
    '''
    input : url(str)
    ouput : url(str)

    get real main page using Selenium
    '''
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        return driver.current_url
    except:
        driver.get_screenshot_as_file('{}.png'.format(url))
        pass


def query_re(query):
    '''
    input : query(str)
    input : query(str)

    delete things inside () including parenthsis
    '''
    query = str(query)
    par_open = query.find('(')
    par_close = query.find(')')
    query = query.replace(query[par_open:par_close + 1], "")
    jaedan = re.compile('[가-힣]+재단').search(query)
    if jaedan:
        query = query.replace(jaedan.group(), "")
    query = query.replace("의료법인", "").replace(" ", "")
    return query



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
    main = "/".join(url.split('/')[:4])
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
               'mgoon', 'fosquare', 'career', '/healthstory/', 'amc', 'youtu.be',
               'goodhosrank', 'easysearch', 'boas', 'kiu.ac.kr/~subhome/',
               'goodoc', 'daejeon.go.kr', 'gimhae.go.kr', 'jeonju.go.kr' 
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
        HSPT_URL_VALID.update({hspt:set((html_re(link), similar(name, hspt), name) 
                                        for link, name in url_list 
                                        if similar(name, hspt) > 2
                                        and not is_portal(link))})
    return HSPT_URL_VALID