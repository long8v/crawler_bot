import numpy as np
import pandas as pd
from collections import Counter
from crawl_utils.url_extractor import *
from crawl_utils.table_parser import *
from crawl_utils.html_request import *
from crawl_utils.create_table import *
from crawl_utils.bot_utils import *
from crawl_utils.column_regularization import *

hspt_code = pd.read_csv('file/HSPT_CODE.csv')
hspt_url = pd.read_csv('file/MERGED_HSPT_URL.csv')
hspt_child = pd.read_csv('file/HSPT_CHILDREN_URL_depth_1.csv')
auto_non = pd.read_csv('file/NON_PAYMENT.csv')
sub_non = pd.read_csv('file/SUB_NON_PAYMENT.csv')
hand_non = pd.read_csv('file/HAND_NON_PAYMENT.csv')
non = pd.read_csv('file/MERGED_NON_PAYMENT.csv')
nonpay = pd.read_csv('file/final_{}.csv'.format(datetime.today().strftime('%y%m%d')))

print('''{} 개의 병원명이 주어졌고
{} 개의 병원 페이지를 가져왔다
그 중 {} 개의 병원이 서브페이지를 가져올 수 있었다
{} 개의 비급여 페이지가 있었고(메인 페이지에서 {}개, depth 2에서 {}개, 수작업기입 {}개)
{} 개가 테이블 파싱에 성공했다'''.format(len(set(hspt_code.hspt_name)),\
len(set(hspt_url.hspt_name)),\
len(set(hspt_child.hspt_name)),\
len(set(non.hspt_name)),\
len(set(auto_non.hspt_name)),\
len(set(sub_non.hspt_name)),\
len(set(hand_non.hspt_name)), \
len(set(nonpay.병원명))))