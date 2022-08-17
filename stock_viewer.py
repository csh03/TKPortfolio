#from __future__ import division
import pandas as pd
from pandas import Series,DataFrame
import random
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import Adjustment
from datetime import datetime,timedelta
import yfinance as yf
import yahoo_fin.stock_info as si

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest,StockBarsRequest

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

def get_cash_flow(ticker):
    return si.get_cash_flow(ticker)

def get_balance_sheet(ticker):
    return si.get_balance_sheet(ticker)

def get_income_statement(ticker):
    return si.get_income_statement(ticker)

def gen_random_8():
    return todays_8

def get_stock_info(ticker):
    ticker = yf.Ticker(ticker)
    return ticker.info

def get_prev_close(ticker):
    end = datetime.now() - timedelta(days=1)
    start = datetime.now() - timedelta(days=4)
    request_params = StockBarsRequest(
                    symbol_or_symbols=ticker,
                    timeframe=TimeFrame.Day,
                    start=start.strftime("%Y-%m-%d"),
                    end = end.strftime("%Y-%m-%d"),
                    adjustment=Adjustment.SPLIT
                    )
    if end.weekday() == 5:
        prev_close = client.get_stock_bars(request_params).df.iloc[-2]['close']
    else:
        prev_close = client.get_stock_bars(request_params).df.iloc[-1]['close']
    return prev_close

def get_pct_change(ticker):
    current = get_current(ticker)
    prev_close = get_prev_close(ticker)
    diff = (current - prev_close)
    pct_change = diff/prev_close*100
    return (round(diff,2),round(pct_change,2))

def get_historical_data(ticker,timeframe):
    now = datetime.now()
    timeframe_dict = {"1d":now,
                      "1w":datetime(now.year,now.month,now.day - 7),
                      "1m":datetime(now.year,now.month - 1,now.day),
                      "1y":datetime(now.year - 1,now.month,now.day),
                      "5y":datetime(now.year - 5,now.month,now.day)
                      }
    start = timeframe_dict[timeframe]

    if timeframe == "1d":
        if start.weekday() == 5:
            start = start - timedelta(days=1)
        elif start.weekday() == 6:
            start = start - timedelta(days=2)
        request_params = StockBarsRequest(
                            symbol_or_symbols=ticker,
                            timeframe=TimeFrame.Hour,
                            start=start.strftime("%Y-%m-%d")
                         )
    else:
        request_params = StockBarsRequest(
                    symbol_or_symbols=ticker,
                    timeframe=TimeFrame.Day,
                    start=start.strftime("%Y-%m-%d"),
                    adjustment=Adjustment.SPLIT
                 )
    bars = client.get_stock_bars(request_params)

    return bars.df

#print(get_stock_info('NVDA'))
