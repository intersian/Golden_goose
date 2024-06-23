import pybithumb


# btc = pybithumb.get_ohlcv("BTC")
# close = btc['close']
#
# # window = close.rolling(5)
# # ma5 = window.mean()
#
# ma5 = close.rolling(5).mean()
# print(ma5)

def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv("BTC")
    close = df['close']
    ma5 = close.rolling(window=5).mean()
    # print(close)
    # print(ma5)
    return ma5[-2]
