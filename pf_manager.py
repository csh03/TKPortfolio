import numpy as np
import pandas as pd
from pandas import Series,DataFrame

class Portfolio:
    def __init__(filename):
        if filename == None:
            self.capital = 0
            self.stockDict = {}

class stockPurchase:
    def __init__(ticker, orderSize, initialPrice):
        self.ticker = ticker
        self.orderSize = orderSize
        self.initialPrice = initialPrice

def create_new():
    return Portfolio(None)

'''
def load_existing(filename):
    new_df = pd.read_csv(filename)
    return new_df.values.tolist()
'''

        
            
