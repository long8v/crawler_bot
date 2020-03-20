import pandas as pd
from collections import Counter
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.html_request import *
from crawl_utils.create_table import *
from crawl_utils.html_parser import *
from crawl_utils.main_site_extractor import *

HSPT_CHILDREN_URL = pd.read_csv('HSPT_CHILDREN_URL_depth_1.csv')

visited = set(HSPT_CHILDREN_URL.url)
NON_PAYMENT = select_sub_page_by_query(HSPT_CHILDREN_URL, '비급여')
find_NON_PAYMENT = set(HSPT_CHILDREN_URL.hspt_name).difference(set(NON_PAYMENT.hspt_name))
print('we will find {} hospitals..'.format(len(find_NON_PAYMENT)))

non_pay_sub = []
cannot_find = []
query = '비급여'

for hspt in find_NON_PAYMENT:
    sub_hspt = select_sub_page_by_hspt_name(HSPT_CHILDREN_URL, hspt)
    reduced = drop_duplicate_by_column(sub_hspt, 'url')
    print(hspt)
    visited = set(reduced)
    if sub_hspt is not None and not sub_hspt.empty:
        sub_hspt_n = create_hspt_children_query(reduced, 
        visited, until_depth=2, query=query)
        if sub_hspt_n is not None and not sub_hspt_n.empty:
            print('find {} from {} !!'.format(query, hspt))
            non_pay_sub += [sub_hspt_n]
        else:
            cannot_find += [hspt]
print('found non-payment from {} hosptials!'.format(len(non_pay_sub)))

SUB_NON = concat_from_list(non_pay_sub)
SUB_NON.to_csv('SUB_NON_PAYMENT.csv', index=False)