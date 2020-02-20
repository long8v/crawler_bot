
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
from crawl_utils.url_extractor import *

def table_parsing(html):
    '''
    input : url(str)
    output : list of table(DataFrame)

    get list of table given url
    '''
    table_df_list = []
    soup = parsing(html)
    tables = soup.find_all('table')
    print('table found in {}'.format(html) 
          if tables else "no table in {}".format(html))
    if tables:
        for table in tables:
            table_df = pd.DataFrame()
            table_head = table.find('thead')
            table_body = table.find('tbody')
            if table_head:
                columns_head = table_head.find_all('th')
                columns_head = [c.text for c in columns_head]
            if table_body:
                columns_body = table_body.find_all('th')
                if not columns_body:
                    columns_body = table_body.find_all('td')
                columns_body = [c.text for c in columns_body]
            if table_body:
                rows = table_body.find_all('tr')
                for row in rows:
                    element = row.find_all('td')
                    element = [e.text.replace('\r', '').strip() for e in element]
                    if len(element) == len(columns_body):
                        columns = columns_body
                    else:
                        try:
                            if len(element) == len(columns_head):
                                columns = columns_head
                            else:
                                columns = [_ for _ in range(len(element))]
                        except:
                            columns = [_ for _ in range(len(element))]
                    if columns and element:
                        cols_dict = {c: e for c, e
                                     in zip(columns, element)}
                        table_df = table_df.append(cols_dict, ignore_index=True)
                table_df_list.append(table_df)
                
    table_df_list = [table for table in table_df_list if any(table)]
    return table_df_list


def get_table_list(df):
    '''
    input : dataframe having full_url
    output : list of tables(dataframe)
    
    using table parser, get list of tables given dataframe with full_url 
    '''
    table_list = []
    for _ in df["full_url"][:]:
        table = table_parsing(_)
        if table:
            table_list += [table]
    return table_list


