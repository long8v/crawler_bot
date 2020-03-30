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

NON_PAYMENT = pd.read_csv('file/{}.csv'.format(file_name))
regular = set(['비급여', 
               '>', '»', '다음', '오른',
               '약제비', '제증명수수료', '치료재료대', '행위료', '기타', '치료재료', '약제', '행위', '제증명'])

digit = re.compile('([0-9])')
DIGIT = select_sub_page_by_re(NON_PAYMENT, digit)
NEXT = select_sub_page_by_query_list(NON_PAYMENT, regular)

NON_PAYMENT = pd.concat([NEXT, DIGIT], axis=0)
NON_PAYMENT = NON_PAYMENT.drop_duplicates(subset='url')
visited = set(NON_PAYMENT.url)
change_column = pickle_open('file/change_column')

df_list = []
NON_PAYMENT_list = []
digit = re.compile('([0-9])')

for _ in tqdm(range(2, 21)):
    NON_PAYMENT = get_html_table(get_sub_pages(NON_PAYMENT, visited))
    visited.update(set(NON_PAYMENT.url))
    DIGIT = select_sub_page_by_re(NON_PAYMENT, digit)
    NEXT = select_sub_page_by_query_list(NON_PAYMENT, regular)
    NON_PAYMENT = pd.concat([NEXT, DIGIT], axis=0)
    # NON_PAYMENT.to_csv('file/MERGED_HAND_depth_{}.csv'.format(_), index=False)
    print(NON_PAYMENT.shape)
    NON_PAYMENT_list.append(NON_PAYMENT)
non_payment_df = concat_from_list(NON_PAYMENT_list)
non_payment_df.to_csv('file/{}_depth_20.csv'.format(file_name), index=False)
