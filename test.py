from alpaca_trade_api.rest import REST


api = REST("3Hus1kCjzawtebPulmdnXPJhma9KjjZX1q0flajT")
import datetime

def process_quote(quote):
    # process quote
    print(quote)

quote_iter = api.get_quotes_iter("AAPL", datetime.now(), datetime.now(), limit=10)
for quote in quote_iter:
    process_quote(quote)
