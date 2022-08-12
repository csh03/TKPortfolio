#from __future__ import division
import pandas as pd
from pandas import Series,DataFrame
import random
import alpaca_trade_api as tradeapi
from alpaca.data.timeframe import TimeFrame
from datetime import datetime,timedelta

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest,StockBarsRequest

'''
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
'''

stocks = pd.read_csv('stock_list.csv')
mega_stocks = stocks[stocks['Market Cap'] > 2e11]

ALPACA_API_KEY = "PKSNUPWHX9Q1PB1DDX6C"
ALPACA_SECRET_KEY = "M6xWH9bDmHfQZdgvTQYYCY32fcoOA7G5Cv63yF8j"

client = StockHistoricalDataClient(ALPACA_API_KEY,ALPACA_SECRET_KEY)

#seeding random on different days
tmp = datetime.today().strftime("%Y:%m:%d")
random.seed(tmp)

todays_8 = random.sample(mega_stocks['Symbol'].squeeze().tolist(),8)

def get_current(ticker):
    request_params = StockLatestQuoteRequest(symbol_or_symbols=ticker)
    latest_bar = client.get_stock_latest_bar(request_params)
    return round(latest_bar[ticker].close,2)

def gen_random_8():
    return todays_8

def get_pct_change(ticker):
    end = datetime.now() - timedelta(days=1)
    start = datetime.now() - timedelta(days=4)
    current = get_current(ticker)

    request_params = StockBarsRequest(
                    symbol_or_symbols=ticker,
                    timeframe=TimeFrame.Day,
                    start=start.strftime("%Y-%m-%d"),
                    end = end.strftime("%Y-%m-%d")
                 )
    prev_close = client.get_stock_bars(request_params).df.iloc[-1]['close']
    diff = (current - prev_close)
    pct_change = diff/prev_close*100
    return (round(diff,2),round(pct_change,2))

def get_historical_data(ticker,timeframe):
    now = datetime.now()
    if(timeframe == "1d"):
        start = now
    elif(timeframe == "1w"):
        start = datetime(now.year,now.month,now.day - 7)
    elif(timeframe == "1m"):
        start = datetime(now.year,now.month - 1,now.day)
    elif(timeframe == "1y"):
        start = datetime(now.year - 1,now.month,now.day)
    elif(timeframe == "5y"):
        start = datetime(now.year - 5,now.month,now.day)

    request_params = StockBarsRequest(
                        symbol_or_symbols=ticker,
                        timeframe=TimeFrame.Day,
                        start=start.strftime("%Y-%m-%d")
                     )
    bars = client.get_stock_bars(request_params)

    return bars.df
