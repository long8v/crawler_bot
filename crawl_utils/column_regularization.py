import numpy as np
import pandas as pd
import time
from collections import Counter
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.html_request import *
from crawl_utils.create_table import *
from crawl_utils.html_parser import *
from crawl_utils.pickle_io import *


def get_table_list(df):
    table_list = {}
    no_table = set([])
    error = set([])
    for idx, row in df.iterrows():
        try:
            table = table_parsing(row.url)
            if table:
                table_list["{}/{}".format(row.hspt_name, row.text)] = table
            else:
                no_table.update([row.hspt_name])
        except Exception as e:
            error.update((row.url, e))
    return table_list, no_table, error


def rename_column(table, change_column):
    table.columns = list(map(query_re, table.columns))
    change_dict = \
    dict(filter(lambda f: f[0] in list(filter(lambda e: e in change_column, table.columns)), 
                change_column.items()))
    table = table.rename(columns = change_dict)
    return table

def filter_column(table, change_column):
    return table[set(filter(lambda e: e in change_column, table.columns))]

def change_duplicate_column(cols):
    new_col = []
    i = 0
    dups = list(filter(lambda e: e[1]>1, Counter(cols).items()))
    dups = [_[0] for _ in dups]
    for _ in cols:
        if _ in dups:
            if not i:
                new_col += [_]
                i += 1
            else:
                new_col += ['중복컬럼_{}'.format(i)]
                i += 1
        else:
            new_col += [_]
    return new_col

def get_filtered_dataframe(list_of_df):
    change_column = pickle_open('change_column')
    null_hspt_list = set([])
    filtered_df_list = []
    for hspt, tables in list_of_df.items():
        for table in tables:
            filtered_df = filter_column(rename_column(table, change_column), change_column)
            filtered_df.columns = change_duplicate_column(filtered_df.columns)
            filtered_df = filtered_df.apply(lambda e: [str(_).strip() for _ in e])
            if not filtered_df.empty:
                filtered_df['병원명'] = hspt.split('/')[0]
                filtered_df_list += [filtered_df]
            else:
                null_hspt_list.update([hspt.split('/')[0]])
    return filtered_df_list, null_hspt_list



def get_final_table(filtered_df_list): 
    final_table = reduce(lambda a, b: pd.concat([a,b], ignore_index=True), filtered_df_list)
    sort_column = ['병원명', '명칭', '분류', '소분류', '중분류', '중복컬럼_1', '비용', '최저비용', '최고비용', 
                   '코드', '구분', '특이사항', '약제비포함여부',  '치료재료대포함여부']
    return final_table[sort_column]


'''   
print((len(set(HSPT_URL.hspt_name)), 
        len(set(HSPT_CHILDREN_URL.hspt_name)),
        len(set(NON_PAYMENT.hspt_name)),
        len(set(_.split('/')[0] for _ in table_list.keys())),
        len(set(final_table.병원명)),
        len(set(yes_cost.병원명))))

time_str = time.strftime('%y%m%d', time.localtime(time.time()))
yes_cost.to_csv('yes_cost_{}.csv'.format(time_str), index=None)
'''