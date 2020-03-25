import pandas as pd
from crawl_utils.bot_utils import *
from crawl_utils.html_request import *
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.column_regularization import *
from crawl_utils.create_table import *

display_start()
NON_PAYMENT = pd.read_csv('file/MERGED_NON_PAYMENT.csv')
change_column = pickle_open('file/change_column')

df_list = [NON_PAYMENT]
for _ in range(2, 3):
    print('doing depth {} ...'.format(_))
    NON_PAYMENT = get_html_table(get_sub_pages(NON_PAYMENT, get_option=True))
    df_list.append(NON_PAYMENT)

concat_from_list(df_list).to_csv('MERGED_depth_2.csv', index=False)
