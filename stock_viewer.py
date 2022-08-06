#from __future__ import division
import pandas as pd
from pandas import Series,DataFrame
'''
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
import pandas_datareader.data as web

from datetime import datetime
'''

tickers = pd.read_csv('ticker_list.csv',header=None)
tickers.columns = ['Ticker']


