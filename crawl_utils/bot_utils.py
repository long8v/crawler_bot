import numpy as np
import pandas as pd
import time
import pickle
from collections import Counter
from functools import reduce

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


def select_sub_page_by_hspt_list(df, query_list):
    '''
    input : df(DataFrame), query(str)
    output : DataFrame

    given query, get DataFrame whose text has query 
    '''
    return df[df['hspt_name'].apply(lambda e: any(q in e for q in query_list))]


def pickle_open(file_name):
    with open('{}.p'.format(file_name), 'rb') as f:
        return pickle.load(f)
        
def pickle_save(file_name, obj_name):
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