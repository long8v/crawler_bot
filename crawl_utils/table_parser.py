
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

def get_table_column(table):
    if len(table.find_all('tr')) > 1:
        first_row = [tr.find_all('th') for tr in table.find_all('tr')][0]
        second_row = [tr.find_all('th') for tr in table.find_all('tr')][1]
        col = [_.text for _ in first_row if _.has_attr('rowspan')] + [_.text for _ in second_row] 
    else:
        col = [_.text for _ in table.find_all('th')]
    return col

def table_parsing(url):
    '''
    input : url(str)
    output : list of table(DataFrame)

    get list of table given url
    '''
    table_df_list = []
    soup = parsing(url)
    if soup:
        tables = soup.find_all('table')
        if tables:
            for table in tables:
                table_df = pd.DataFrame()
                table_head = table.find('thead')
                table_body = table.find('tbody')
                if table_head:
                    columns_head = get_table_column(table_head)
                if table_body:
                    columns_body = get_table_column(table_body)
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
    for _ in df["full"][:]:
        table = table_parsing(get_html_text(_))
        if table:
            table_list += [table]
    return table_list


