import numpy as np
import pandas as pd
import time
from collections import Counter
from crawl_utils.bot_utils import *

NON_PAYMENT = pd.read_csv('file/NON_PAYMENT.csv')
SUB_NON = pd.read_csv('file/SUB_NON_PAYMENT.csv')
HAND = pd.read_csv('file/HAND_NON_PAYMENT.csv')
merged = [NON_PAYMENT, SUB_NON, HAND]
concat_from_list(merged).to_csv('file/MERGED_NON_PAYMENT.csv', index=False)
print('saved')