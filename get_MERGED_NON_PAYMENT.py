import numpy as np
import pandas as pd
import time
from collections import Counter
from crawl_utils.bot_utils import *

NON_PAYMENT = pd.read_csv('NON_PAYMENT.csv')
SUB_NON = pd.read_csv('SUB_NON_PAYMENT.csv')
HAND = pd.read_csv('HAND_NON_PAYMENT.csv')
merged = [NON_PAYMENT, SUB_NON, HAND]
concat_from_list(merged).to_csv('MERGED_NON_PAYMENT.csv', index=False)