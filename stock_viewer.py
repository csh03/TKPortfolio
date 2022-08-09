#from __future__ import division
import pandas as pd
from pandas import Series,DataFrame
import random
from polygon import RESTClient
from yahoo_fin import stock_info
import pandas_datareader.data as web
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

api_key = "W4wUBkKhnuicYooQTJE4cWIkXhNqfqch"

client = RESTClient(api_key)

#seeding random on different days
tmp = datetime.today().strftime("%Y:%m:%d")
random.seed(tmp)

todays_8 = random.sample(mega_stocks['Symbol'].squeeze().tolist(),8)

def get_current_price(ticker):
    return str(round(stock_info.get_live_price(ticker),2))

def gen_random_8():
    return todays_8

endtime = datetime.now()
start = datetime(endtime.year,endtime.month,endtime.day - 3)

def get_pct_change(ticker):
    current = stock_info.get_live_price(ticker)
    prev_close = web.DataReader(ticker,'yahoo',start,endtime).iloc[-2]['Adj Close']
    diff = (current - prev_close)
    pct_change = diff/prev_close*100
    return (round(diff,2),round(pct_change,2))

print(get_pct_change('NVDA'))
