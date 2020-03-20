import numpy as np
import pandas as pd
from collections import Counter
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.html_request import *
from crawl_utils.create_table import *
from crawl_utils.html_parser import *
from crawl_utils.column_regularization import *

NON_PAYMENT = pd.read_csv('MERGED_depth_2.csv')
visited = set(NON_PAYMENT.url)
change_column = pickle_open('change_column')

df_list = []
NON_PAYMENT_list = [NON_PAYMENT]
for _ in range(1, 100):
    print('doing depth {} ...'.format(_))
    NON_PAYMENT = get_html_table(get_sub_pages(NON_PAYMENT, visited))
    visited.update(set(NON_PAYMENT.url))
    NON_PAYMENT = select_sub_page_by_query_list(NON_PAYMENT, ['>', '다음', '오른'])
    print(NON_PAYMENT.shape)
    NON_PAYMENT_list.append(NON_PAYMENT)
non_payment_df = concat_from_list(NON_PAYMENT_list)
non_payment_df.to_csv('MERGED_depth_100.csv', index=False)
