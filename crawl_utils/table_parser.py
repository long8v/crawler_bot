
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


def strip_all(text):
    '''
    input : text(str)
    output : text(str)

    strip all blank in the text
    '''
    return text.strip().replace(" ", "").replace("\n", "").replace("\t", "").replace('\r',"")

def get_table_column(table):
    '''
    input : table(dom obejct)
    output : column(list)
    
    given table dom, get column list 
    if having double column, ignore first
    '''
    columns = []
    columns_final = []
    trs = table.find_all('tr')
    if len(table.find_all('tr')) > 1:
        for tr in trs:
            columns.append(tr.find_all(['th', 'td']))
        first_row = []
        for c in columns[0]:
            if c.has_attr('rowspan'):
                first_row += [c.text]
            elif c.has_attr('colspan'):
                first_row += [None for _ in range(int(c["colspan"]))]
            else:
                first_row += [None]

        second_row = [strip_all(c.text) for c in columns[1]]
        final_row = []
        for f in first_row:
            if f:
                final_row += [f]
            else:
                try:
                    final_row += [second_row.pop()]
                except:
                    final_row = []
                    break
    else:
        final_row = [strip_all(th.text) for th in table.find_all(['th'])]
    return final_row


def table_parsing(url):
    '''
    input : url(str)
    output : list of table(DataFrame)

    get list of table given url
    '''
    table_df_list = []
    columns = []
    element = []
    soup = parsing(url)
    if soup:
        tables = soup.find_all('table')
        if tables:
            for table in tables:
                table_df = pd.DataFrame()
                table_head = table.find('thead')
                table_body = table.find('tbody')
                if table_body:
                    columns_body = get_table_column(table_body)
                    rows = table_body.find_all('tr')
                    for row in rows:
                        element = row.find_all(['td', 'th'])
                        element = [e.text.replace('\r', '').strip() \
                            for e in element]
                else:
                    continue
                if table_head:
                    columns_head = get_table_column(table_head)
                    if len(element) == len(columns_head):
                        columns = columns_head
                elif len(element) == len(columns_body):
                    columns = columns_body
                if not columns:
                    print('cannot parse column name {}'.format(url))
                    columns = [str(_) for _ in range(len(element))]
                    columns = list(map(strip_all, columns))
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


