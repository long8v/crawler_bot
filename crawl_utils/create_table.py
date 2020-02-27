import pandas as pd
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.html_request import *

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
        hspt_sorted_url[key] = sorted(hspt_valid_url[key], key=lambda e: e[1], reverse=True)
    hspt_final_url = {}
    for key, value in hspt_sorted_url.items():
        if hspt_valid_url[key]:
            hspt_final_url[key] = list(hspt_valid_url[key])[0][0]
        else:
            try: 
                hspt_final_url[key] = hspt_url[key][0][0]
            except:
                print('{} is omitted'.format(key))
    HSPT_URL = pd.DataFrame()
    HSPT_URL["hspt_name"] = hspt_final_url.keys()
    HSPT_URL["root_url"] = hspt_final_url.values()
    HSPT_URL.to_csv('HSPT_URL.csv', index=False)
    print('"HSPT_URL.csv" is saved')

def create_hspt_children_url(df, visited, depth = 1):
    '''
    input : df(DataFrame), visited(set), depth(int)
    output : DataFrame

    given DataFrame with url, get first children url table 
    visited url will not be visited again
    '''
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
        visited.update(set(df.url))
        children_list += [df]
    return concat_from_list(children_list)
