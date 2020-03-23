import pandas as pd
from crawl_utils.bot_utils import *
from crawl_utils.html_request import *
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.column_regularization import *
from crawl_utils.create_table import *

hspt_table = pd.read_csv('file/HSPT_CODE.csv')
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
HSPT_URL.to_csv('file/HSPT_URL.csv', index=False)
print('"HSPT_URL.csv" is saved')

