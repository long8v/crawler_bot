import pandas as pd
from crawl_utils.bot_utils import *
from crawl_utils.html_request import *
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.column_regularization import *


def get_html_table(main_sub_pages, depth=1):
    '''
    input : list having tuples (text, lisf of urls)
    output : DataFrame
    
    get html table having text from url, url, depth, url name(hspt)
    '''
    HSPT_CHILDREN_URL_list = []
    for hspt, contents in main_sub_pages:
        HSPT_CHILDREN_URL = pd.DataFrame({'hspt_name':[], 'url':[],'depth':[],'text':[]})
        zipped = list(zip(*contents))
        if len(zipped):
            HSPT_CHILDREN_URL["text"] = ['{}/{}'.format(hspt, _) for _ in zipped[0]]
            HSPT_CHILDREN_URL["url"] = list(zipped[1])
            HSPT_CHILDREN_URL["depth"] = [depth for _ in range(len(contents))]
            HSPT_CHILDREN_URL["hspt_name"] = [hspt for _ in range(len(contents))]
            HSPT_CHILDREN_URL["date"] = [datetime.today().strftime('%y%m%d') 
            for _ in range(len(contents))]
            HSPT_CHILDREN_URL_list.append(HSPT_CHILDREN_URL)
    return concat_from_list(HSPT_CHILDREN_URL_list)


def create_hspt_children_url(df, visited, depth = 1):
    '''
    input : df(DataFrame), visited(set), depth(int)
    output : DataFrame

    given DataFrame with url, get first children url table 
    visited url will not be visited again
    '''
    if df is not None and not df.empty:
        main_sub_url = get_sub_pages(df, visited)
        HSPT_CHILDREN_URL = get_html_table(main_sub_url, depth)
        return HSPT_CHILDREN_URL


def create_hspt_children_url_until(df, visited, until_depth = 2):
    '''
    input : df(DataFrame), visited(set), until_depth(int)
    output : DataFrame

    given DataFrame with url, get childeren of children until until_depth
    '''
    children_list = [df]
    current_depth = max(df.depth)
    for depth in range(current_depth + 1, until_depth + 1):
        print('doing depth {}...'.format(depth))
        df = create_hspt_children_url(df, visited, depth)
        if df.empty:
            break
        visited.update(set(df.url))
        children_list += [df]
    return concat_from_list(children_list)

def create_hspt_children_query(df, visited, query, until_depth = 2):
    '''
    input : df(DataFrame), visited(set), until_depth(int)
    output : DataFrame

    given DataFrame with url, get childeren of children until until_depth
    '''
    children_list = [df]
    current_depth = max(df.depth)
    for depth in range(current_depth + 1, until_depth + 1):
        print('doing depth {}...'.format(depth))
        df = create_hspt_children_url(df, visited, depth)
        if df is not None:
            df_query = select_sub_page_by_query(df, query)
            if df_query is None or not df_query.empty:
                return df_query
            if df.empty:
                break

