import numpy as np
import pandas as pd
from collections import Counter
from crawl_utils.bot_utils import *
from crawl_utils.html_request import *
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.column_regularization import *
from crawl_utils.create_table import *

HAND_HSPT_URL = pd.read_csv('file/HAND_HSPT_URL.csv')
HAND_HSPT_URL['url'] = HAND_HSPT_URL.apply(lambda e: e['original_link'] 
                                                   if e['hand_link'] is np.nan 
                                                   else e['hand_link'], axis=1)
                                                   
HAND_HSPT_URL[['hspt_name', 'url']].to_csv('file/MERGED_HSPT_URL.csv', index=False)