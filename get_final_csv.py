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

NON_PAYMENT = pd.read_csv('file/merged_depth_100.csv')
df = url_df_to_non_payment_df(NON_PAYMENT)
df.to_csv('file/before_final_{}.csv'.format(get_today_date()), index=False)
CODE = pd.read_csv('file/HSPT_CODE.csv')
CODE.columns = ['병원코드', '병원명']
CODE = CODE.applymap(str)
df = df.dropna(how='all', subset=['최고비용', '최저비용', '비용'])
df = CODE.merge(df, on='병원명')
df = df.drop_duplicates()
df.to_csv('file/final_{}.csv'.format(get_today_date()), index=False)
