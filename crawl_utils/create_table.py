import pandas as pd
from collections import Counter
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.html_request import *
from crawl_utils.create_table import *
from crawl_utils.html_parser import *

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



def create_hspt_url_table():
    '''
    input : None
    output : None
    
    given csv with column of hspt names, search name in naver 
    and get offical page for the name
    and save it as a csv file
    '''
    hspt_table = pd.read_csv('HSPT_CODE.csv')
    hspt_url = get_main_page_dict(hspt_table['hspt_name'])
    hspt_valid_url = get_valid_html(hspt_url)
    hspt_sorted_url = {}
    for key, value in hspt_valid_url.items():
        hspt_sorted_url[key] = sorted(hspt_valid_url[key], \
                    key=lambda e: [e[1], -len(e[2])], reverse=True)
    hspt_final_url = {}
    for key, value in hspt_sorted_url.items():
        if hspt_valid_url[key]:
            hspt_final_url[key] = redirect(list(hspt_sorted_url[key])[0][0])
        else:
            try: 
                hspt_final_url[key] = hspt_url[key][0][0]
            except:
                print('{} is omitted'.format(key))
    HSPT_URL = pd.DataFrame()
    HSPT_URL["hspt_name"] = hspt_final_url.keys()
    HSPT_URL["url"] = hspt_final_url.values()
    HSPT_URL.to_csv('HSPT_URL.csv', index=False)
    print('"HSPT_URL.csv" is saved')


def create_hspt_first_child():
    '''
    input : None
    output : None

    given HSPT_URL csv, get all html from main page
    '''
    HSPT_URL = pd.read_csv('HSPT_URL.csv')
    main_sub_url = get_sub_pages(HSPT_URL, visited=set())
    HSPT_CHILDREN_URL = get_html_table(main_sub_url)
    HSPT_CHILDREN_URL.to_csv('HSPT_CHILDREN_URL_depth_1.csv', index=False)
    print('"HSPT_CHILDREN_URL_depth_1.csv" is saved')


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

