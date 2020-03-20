import numpy as np
import pandas as pd
import time
from collections import Counter
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.html_request import *
from crawl_utils.create_table import *
from crawl_utils.html_parser import *
from crawl_utils.column_regularization import *

NON_PAYMENT = pd.read_csv('NON_PAYMENT.csv')
SUB_NON = pd.read_csv('SUB_NON_PAYMENT.csv')
HAND = pd.read_csv('HAND_NON_PAYMENT.csv')
merged = [NON_PAYMENT, SUB_NON, HAND]
concat_from_list(merged).to_csv('MERGED_NON_PAYMENT.csv', index=False)