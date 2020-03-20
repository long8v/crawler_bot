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


NON_PAYMENT = pd.read_csv('merged_depth_100.csv')
df = url_df_to_non_payment_df(NON_PAYMENT)
df = df.dropna(how='all', subset=['최고비용', '최저비용', '비용'])
df.to_csv('final_{}.csv'.format(datetime.today().strftime('%y%m%d')), index=False)