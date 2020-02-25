import pandas as pd
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.html_request import *

def create_hspt_url_table():
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

def create_hspt_children_url(df, depth = 1):
    main_sub_url = get_sub_pages(df)
    HSPT_CHILDREN_URL = get_html_table(main_sub_url, depth)
    return HSPT_CHILDREN_URL

def create_hspt_children_url_until(df, until_depth = 2):
    children_list = []
    current_depth = max(df.depth)
    for depth in range(current_depth, until_depth + 1):
        print(depth)
        df = create_hspt_children_url(df, depth)
        children_list += [df]
    return concat_from_list(children_list)
