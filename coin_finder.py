import pybithumb
import numpy as np


def get_hpr(ticker):
    try:
        df = pybithumb.get_ohlcv(ticker)
        df = df.loc['2024']

        df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
        df['range'] = (df['high'] - df['low']) * 0.5
        df['target'] = df['open'] + df['range'].shift(1)
        df['bull'] = df['open'] > df['ma5']


        fee = 0.0009
        df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)
        df['hpr'] = df['ror'].cumprod()
        df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

        return df['hpr'].iloc[-2]

    except:
        return 1


tickers = pybithumb.get_tickers()

hprs = []
for ticker in tickers:
    hpr = get_hpr(ticker)
    hprs.append((ticker, hpr))

sorted_hprs = sorted(hprs, key=lambda x:x[1], reverse=True)
print(sorted_hprs[:5])