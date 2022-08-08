#from __future__ import division
import pandas as pd
from pandas import Series,DataFrame
import random
import yfinance as yf
from yahoo_fin import stock_info

from datetime import datetime,timedelta

'''
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')


from datetime import datetime
'''

stocks = pd.read_csv('stock_list.csv')
mega_stocks = stocks[stocks['Market Cap'] > 2e11]

#seeding random on different days
tmp = datetime.today().strftime("%Y:%m:%d")
random.seed(tmp)

todays_8 = random.sample(mega_stocks['Symbol'].squeeze().tolist(),8)

def gen_random_8():
    return todays_8

def get_pct_change(ticker):
    data = yf.Ticker('TSLA').info
    diff = (data['regularMarketPrice'] - data['regularMarketPreviousClose'])
    pct_change = diff/data['regularMarketPreviousClose']*100
    return (round(diff,2),round(pct_change,2))
