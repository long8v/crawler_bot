from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from pyvirtualdisplay import Display

def download(url,params={},retries=0):
    '''
    input : url(str), parameter(dict)
    output : resp(object)
    
    using requests, get object resp given url
    for robustness, if error is server error(500s), retry at most 3 times
    otherwise, print error name, error reason, and header
    '''
    resp = None
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    header = {"user-agent":user_agent}
    try:
        resp = requests.get(url,params=params,headers=header)
        resp.raise_for_status() #error/event 발생하면 except로 가게해라 
        resp.encoding = None
    except requests.exceptions.HTTPError as e:
        url = url.replace("http://", "https://")
        if e.response.status_code//100==5 and retries>0:
            print(retries)
            resp = download(url, params, retries-1)
        else: 
            pass
            # print('failed to download {}'.format(url))
    except:
        if retries > 0:
            resp = download(url,params,retries-1)
        if retries == 0:
            pass
            # print('failed to download {}'.format(url))
    return resp


def parsing(url):
    '''
    input : url(str)
    output : dom(object)
    
    get dom given url
    '''
    html = download(url)
    if html:
        dom = BeautifulSoup(html.text, 'lxml')
        return dom
        
def display_start():
    display = Display(visible=0, size=(800,800))
    display.start()

def get_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def parsing_dynamic(url):
    dom = BeautifulSoup(get_driver(url).page_source, 'lxml')
    return dom