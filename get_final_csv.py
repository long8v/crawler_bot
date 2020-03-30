import numpy as np
import pandas as pd
import time
from collections import Counter
from crawl_utils.bot_utils import *
from crawl_utils.html_request import *
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.column_regularization import *
from crawl_utils.create_table import *

NON_PAYMENT = pd.read_csv('file/HAND_2_depth_20.csv')
regular = set(['비급여', 
               '>', '»', '다음', '오른',
               '약제비', '제증명수수료', '치료재료대', '행위료', '기타', '치료재료', '약제', '행위', '제증명'])

digit = re.compile('([0-9])')
DIGIT = select_sub_page_by_re(NON_PAYMENT, digit)
NEXT = select_sub_page_by_query_list(NON_PAYMENT, regular)

print('non payment {} {}'.format(NEXT, DIGIT))
NON_PAYMENT = pd.concat([NEXT, DIGIT], axis=0)
df = url_df_to_non_payment_df(NON_PAYMENT)

df.to_csv('file/before_HAND_final_{}_오후.csv'.format(get_today_date()), index=False)
CODE = pd.read_csv('file/HSPT_CODE.csv')
CODE.columns = ['병원코드', '병원명']
CODE = CODE.applymap(str)
df = df.dropna(how='all', subset=['최고비용', '최저비용', '비용'])
df = CODE.merge(df, on='병원명')
df = df.drop_duplicates()
df.to_csv('file/final_HAND2_{}_오후.csv'.format(get_today_date()), index=False)
