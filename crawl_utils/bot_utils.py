import numpy as np
import pandas as pd
import time
import datetime
import pickle
from collections import Counter
from functools import reduce
from PIL import Image
from io import BytesIO

def select_sub_page_by_hspt_name(df, query, query_in = False):
    '''
    input : df(DataFrame), query(str)
    output : DataFrame

    given query, get DataFrame whose hspt_name has query 
    '''
    if query_in:
        return df[df['hspt_name'].apply(lambda e: query in e)]
    return df[df['hspt_name'].apply(lambda e: query == e)]

def select_sub_page_by_query(df, query):
    '''
    input : df(DataFrame), query(str)
    output : DataFrame

    given query, get DataFrame whose text has query 
    '''
    return df[df['text'].apply(lambda e: query in e)]


def select_sub_page_by_query_list(df, query_list):
    '''
    input : df(DataFrame), query(str)
    output : DataFrame

    given query, get DataFrame whose text has query 
    '''
    return df[df['text'].apply(lambda e: any(q in e for q in query_list))]

def select_sub_page_by_re(df, reg_exp):
    '''
    input : df(DataFrame), reg_exp(re.Pattern)
    output : DataFrame

    given query, get DataFrame which is searched by regular expression
    '''
    return df[df['text'].apply(lambda e: bool(reg_exp.search(e)))]   

def select_sub_page_by_hspt_list(df, query_list):
    '''
    input : df(DataFrame), query(str)
    output : DataFrame

    given query, get DataFrame whose text has query 
    '''
    return df[df['hspt_name'].apply(lambda e: any(q in e for q in query_list))]


def pickle_open(file_name):
    '''
    input : file_name without .p(str)
    output : object

    get pickle file
    '''
    with open('{}.p'.format(file_name), 'rb') as f:
        return pickle.load(f)
        
def pickle_save(file_name, obj_name):
    '''
    input : file_name(str), otj_name(object)
    output : None datetime import *

    save object as pickle file
    '''
    with open('{}.p'.format(file_name), 'wb') as f:
        pickle.dump(obj_name, f)


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

def get_yes_cost(df):
    '''
    input : df(DataFrame)
    output : df(DataFrame)

    get DataFrame whose rows have cost at least from 최고비용, 최저비용, 비용
    '''
    return df.dropna(how='all', subset=['최고비용', '최저비용', '비용'])

def get_yes_name(df):
    '''
    input : df(DataFrame)
    output : df(DataFrame)

    get DataFrame whose rows have cost at least from 최고비용, 최저비용, 비용
    '''
    return df.dropna(how='all', subset=['명칭', '분류', '소분류', '중분류', '중복컬럼_1', '구분', '특이사항'])

def html_parsing(df, query):
    '''
    input : DataFrame, query(str)
    output : DataFrame

    find rows having query from given data frame 
    '''
    df_query = df[df["text"].apply(lambda e: query in e)]
    print('{} have {} page'.format(df_query.shape[0], query))
    return df_query


def drop_duplicate_by_column(df, column):
    '''
    input : dataframe, column(str or list of str)
    output : dataFrame 
    
    drop rows having overlapped item in selected column 
    '''
    df_reduced = df.drop_duplicates(column)
    return df_reduced

def get_now():
    '''
    input : None
    output : str
    '''
    return time.strftime("%m%d_%H%M_%S", time.gmtime())

def get_today_date():
    '''
    input : None
    output : date(str)

    get today date
    '''
    return datetime.datetime.today().strftime('%y%m%d')

def re_url(url):
    '''
    input : url(str)
    output : url(str)
    
    get main part of url 
    '''
    return url.replace("http://", "").replace("https://", "").replace("www.","").split(".co")[0].split(".kr")[0]
    
def save_image(driver, png_name):
    '''
    input : driver(driver), png_name(str)
    output : None


    '''
    png = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png)) 
    im.save('{}.png'.format(png_name)) 
