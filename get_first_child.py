import numpy as np
import pandas as pd
from collections import Counter
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.html_request import *
from crawl_utils.create_table import *
from crawl_utils.html_parser import *
from crawl_utils.pickle_io import *
from crawl_utils.column_regularization import *

HSPT_URL = pd.read_csv('MERGED_HSPT_URL.csv')
main_sub_url = get_sub_pages(HSPT_URL, visited=set())
HSPT_CHILDREN_URL = get_html_table(main_sub_url)
HSPT_CHILDREN_URL.to_csv('HSPT_CHILDREN_URL_depth_1.csv', index=False)
print('"HSPT_CHILDREN_URL_depth_1.csv" is saved')

