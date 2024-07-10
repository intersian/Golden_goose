import pyupbit
import pybithumb

bit_tickers = pybithumb.get_tickers()
for ticker in bit_tickers:
    print(ticker)


up_tickers = pyupbit.get_tickers()
for ticker in up_tickers:
    print(ticker)