#from __future__ import division
import pandas as pd
from pandas import Series,DataFrame
import random
from yahoo_fin import stock_info
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime,timedelta

'''
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
'''

stocks = pd.read_csv('stock_list.csv')
mega_stocks = stocks[stocks['Market Cap'] > 2e11]

BASE_URL = "https://paper-api.alpaca.markets"
ALPACA_API_KEY = "PKSNUPWHX9Q1PB1DDX6C"
ALPACA_SECRET_KEY = "M6xWH9bDmHfQZdgvTQYYCY32fcoOA7G5Cv63yF8j"

api = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, 
                    base_url=BASE_URL, api_version='v2')

endtime = datetime.now() - timedelta(days=1)
start = datetime(endtime.year,endtime.month,endtime.day-7)

#seeding random on different days
tmp = datetime.today().strftime("%Y:%m:%d")
random.seed(tmp)

todays_8 = random.sample(mega_stocks['Symbol'].squeeze().tolist(),8)

def get_current_price(ticker):
    return str(round(stock_info.get_live_price(ticker),2))

def gen_random_8():
    return todays_8

endtime = datetime.now() - timedelta(1)
start = datetime(endtime.year,endtime.month,endtime.day - 2)

def get_pct_change(ticker):
    current = stock_info.get_live_price(ticker)
    prev_close = api.get_bars(ticker, TimeFrame.Day, start.strftime("%Y-%m-%d"),
                    endtime.strftime("%Y-%m-%d")).df.iloc[-1]['close']
    diff = (current - prev_close)
    pct_change = diff/prev_close*100
    return (round(diff,2),round(pct_change,2))

print(get_pct_change('NVDA'))
