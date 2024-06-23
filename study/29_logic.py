with open("../bithumb.txt") as f:
lines = f.readlines()
key = lines[0].strip()
secret = lines[1].strip()
# bithumb = pybithumb.Bithumb(key, secret)

import pybithumb
import time
import datetime

# con_key = "09899240e4999f7972860affceb43e23"
# sec_key = "7cac9287114a6b643572b3dc9750391b"
#
# bithumb = pybithumb.Bithumb(con_key, sec_key)
def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw/float(sell_price)
    bithumb.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)

def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv("BTC")
    close = df['close']
    ma5 = close.rolling(window=5).mean()
    return ma5[-2]

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma5 = get_yesterday_ma5("BTC")
target_price = get_target_price("BTC")

while True:
    try:
        now = datetime.datetime.now()
        # if now == mid:
        if mid < now < mid + datetime.timedelta(seconds=10):
            # print("정각입니다")
            target_price = get_target_price("BTC")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            ma5 = get_yesterday_ma5("BTC")
            sell_crypto_currency("BTC")

        # print(now, "vs", mid)
        current_price = pybithumb.get_current_price("BTC")
        # print(current_price)
        if (current_price > target_price) and (current_price > ma5):
            # krw = bithumb.get_balance("BTC")[2]
            # orderbook = pybithumb.get_orderbook("BTC")
            # sell_price = orderbook['asks'][0]['price']
            # unit = krw/float(sell_price)
            # bithumb.buy_market_order("BTC", unit)
            buy_crypto_currency("BTC")
    except:
        print("에러 발생")

    time.sleep(1)



# while True:
#     price = pybithumb.get_current_price("BTC")
#     print(price)
#     time.sleep(0.2)

# df = pybithumb.get_ohlcv("BTC")
# # print(df.tail())
# yesterday = df.iloc[-2]
#
# today_open = yesterday['close']
# yesterday_high = yesterday['high']
# yesterday_low = yesterday['low']
# target = today_open + (yesterday_high - yesterday_low) * 0.5
# print(target)

