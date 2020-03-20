import numpy as np
import pandas as pd
import time
from collections import Counter
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.html_request import *
from crawl_utils.create_table import *
from crawl_utils.html_parser import *
from crawl_utils.pickle_io import *
from crawl_utils.column_regularization import *

NON_PAYMENT = pd.read_csv('NON_PAYMENT_depth3.csv')
change_column = pickle_open('change_column')

df = url_df_to_non_payment_df(NON_PAYMENT, change_column)
df.to_csv('merged.csv')