import pybithumb
import time

tickers = pybithumb.get_tickers()
print(tickers)
print(len(tickers))

price = pybithumb.get_current_price("BTC")
print(price)

# while True:
#     price = pybithumb.get_current_price("BTC")
#     print(price)
#     time.sleep(1)

# for ticker in tickers:
#     price = pybithumb.get_current_price(ticker)
#     print(ticker, price)
#     time.sleep(0.1)

detail = pybithumb.get_market_detail("BTC")
print(detail)