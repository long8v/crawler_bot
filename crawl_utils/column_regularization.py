import numpy as np
import pandas as pd
import time
from collections import Counter
from pydash import *
from crawl_utils.table_parser import *
from crawl_utils.create_table import *
from crawl_utils.bot_utils import *


def get_table_list(df):
    '''
    input : DataFrame with url
    output : table_list, no_table, error

    given DataFrame with url, get list of tables from url using table parser
    '''
    table_list = {}
    no_table = set([])
    error_list = set([])
    for idx, row in df.iterrows():
        try:
            table = table_parsing(row.url)
            if table:
                table_list["{}/{}".format(row.hspt_name, row.text)] = table
            else:
                no_table.update([row.hspt_name])
        except Exception as e:
            print(e)
            error_list.update((row.url, e))
    return table_list, no_table, error_list


def rename_column(table, change_column):
    '''
    input : table(DataFrame)
    output : change_column(dict)

    get dictionary 'change_column' which is used for regularize column name 
    '''
    table.columns = list(map(query_re, table.columns))
    change_dict = \
    dict(filter(lambda f: f[0] in list(filter(lambda e: e in change_column, table.columns)), 
                change_column.items()))
    table = table.rename(columns = change_dict)
    return table

def filter_column(table, change_column):
    '''
    input : table(DataFrame)
    output : change_column(dict)
    
    index columns which are in change_column
    '''
    return table[set(filter(lambda e: e in change_column, table.columns))]

def change_duplicate_column(cols):
    '''
    input : cols(list)
    output : new_col(list)
    
    when there are multiple same columns,
    change ones into 중복컬럼_1, 중복컬럼_2, and so on
    '''
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

def make_change_column(table_list):
    '''
    input : table_list(list of DataFrames)
    output : change_column(dict)

    get change_column dictionary given table_list
    '''
    column = ['분류', '구분', '명칭', '코드', '비용', '특이사항', '최저비용', '약제비포함여부', '치료재료대포함여부', '최고비용',
            '중분류', '소분류']
    change_column = {c:c for c in column}

    column = {'최대':'최고비용','최저': '최저비용', '최고':'최고비용', '최소':'최저비용', 
            '비고':'특이사항',  '기타':'특이사항', '단위' : '특이사항',
            '단가': '비용', '금액':'비용', '가격':'비용', '(원)':'비용',
            '수가명칭':'명칭', '내용':'명칭', '비급여명':'명칭', '처방명':'명칭', 
            '항목':'명칭', '품목':'명칭', '수가명':'명칭', '명':'명칭', '품명':'명칭', '기본항목':'명칭',
            '수가':'비용', '일반수가':'비용',
            '약제':'약제비포함여부', '약재':'약제비포함여부', 
            '치료재료':'치료재료대포함여부', '치료대':'치료재료대포함여부', }
            
    change_column.update(column)

    counter = Counter([c for table in table_list.values() for t in table for c in t.columns]).most_common()
    for c, v in counter:
        c = str(c)
        for col in column:
            if len(c) == 1 or len(col) == 1:
                continue
            if c in col:
                if c =="":
                    continue
                change_column[c] = column[col]
            if col in c:
                change_column[c] = column[col]

    change_column = dict(filter(lambda e: len(e[0]) < 10 and len(e[0]) > 1, change_column.items()))

    change_column['소분류-상세명'] = '소분류'
    change_column['수가코드'] = '특이사항'
    change_column['최저부가비율'] = '특이사항'
    change_column['최고가비율'] = '특이사항'
    change_column['단위'] = '특이사항'
    change_column['비급여가(원)'] = '비용'


    name = ['제증명 내역', '기본항목', '분류/명칭', '수가명','수가명칭', '상세 분류', '세부항목', '수가명칭(한글)', '병원사용명칭',
    '제증명료 구분','상급병실료 구분','식대료 구분','이송료 구분', 
    '주사료 구분','처치수술료 구분', '처치수술료 구분', '약제료 구분', '비급여 항목']   

    for n in name:
        change_column[n] = '명칭'
   
    return change_column
    

def get_filtered_dataframe(list_of_df, change_column):
    '''
    input : list_of_df(list of DataFrames)
    output : change_column(dict)
    
    
    '''
    null_hspt_list = set([])
    filtered_df_list = []
    for hspt, tables in list_of_df.items():
        change_column = make_change_column(tables)
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
    '''
    input : filtered_df_list(list of DataFrames)
    output : final_table(stacked DataFrame)

    given list of DataFrame, stack it and sort it given sort_column
    '''
    final_table = reduce(lambda a, b: pd.concat([a,b], ignore_index=True), filtered_df_list)
    sort_column = ['병원명', '명칭', '분류', '소분류', '중분류', '중복컬럼_1', '비용', '최저비용', '최고비용', 
                   '코드', '구분', '특이사항', '약제비포함여부',  '치료재료대포함여부']
    return final_table[sort_column]


def url_df_to_non_payment_df(df):
    '''
    input : DataFrame(with url)
    output : DataFrame(stacked regularized table)

    given DataFrame with url, get regularized table
    '''
    TABLE_LIST, _, _ = get_table_list(df)
    change_column = make_change_column(TABLE_LIST)
    FILTERED_TABLE_LIST, _ = get_filtered_dataframe(TABLE_LIST, change_column)
    FINAL_TABLE = get_final_table(FILTERED_TABLE_LIST)
    return FINAL_TABLE

