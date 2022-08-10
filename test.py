import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta

# API Info for fetching data, portfolio, etc. from Alpaca
BASE_URL = "https://paper-api.alpaca.markets"
ALPACA_API_KEY = "PKSNUPWHX9Q1PB1DDX6C"
ALPACA_SECRET_KEY = "M6xWH9bDmHfQZdgvTQYYCY32fcoOA7G5Cv63yF8j"

endtime = datetime.now() - timedelta(days=1)
start = datetime(endtime.year,endtime.month,endtime.day-7)

# Instantiate REST API Connection
api = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, 
                    base_url=BASE_URL, api_version='v2')

test = api.get_bars("NVDA", TimeFrame.Day, start.strftime("%Y-%m-%d"),
                    endtime.strftime("%Y-%m-%d")).df
print(test)
