import re
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import Counter
from crawl_utils.bot_utils import *
from crawl_utils.html_request import *
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.column_regularization import *
from crawl_utils.create_table import *

display_start()
NON_PAYMENT = pd.read_csv('file/MERGED_depth_2.csv')
visited = set(NON_PAYMENT.url)
change_column = pickle_open('file/change_column')

df_list = []
NON_PAYMENT_list = [NON_PAYMENT]
digit = re.compile('([0-9])')

for _ in tqdm(range(1, 100)):
    NON_PAYMENT = get_html_table(get_sub_pages(NON_PAYMENT, visited))
    visited.update(set(NON_PAYMENT.url))
    NEXT = select_sub_page_by_query_list(NON_PAYMENT, ['>', '»', '다음', '오른'])
    DIGIT = select_sub_page_by_re(NON_PAYMENT, digit)
    NON_PAYMENT = pd.concat([NEXT, DIGIT], axis=0)
    print(NON_PAYMENT.shape)
    NON_PAYMENT_list.append(NON_PAYMENT)
non_payment_df = concat_from_list(NON_PAYMENT_list)
non_payment_df.to_csv('file/MERGED_depth_100.csv', index=False)
