import pybithumb

btc = pybithumb.get_ohlc("BTC")
print(btc)

btc = pybithumb.get_ohlcv("BTC")
print(btc)

close = btc['close']
print(close)