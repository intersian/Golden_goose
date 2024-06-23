import pybithumb
import numpy as np


def get_hpr(ticker):
    try:
        df = pybithumb.get_ohlcv("BTC")
        df = df.loc['2024']

        df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
        df['range'] = (df['high'] - df['low']) * k
        df['target'] = df['open'] + df['range'].shift(1)
        df['bull'] = df['open'] > df['ma5']


        fee = 0.0009
        df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)
        df['hpr'] = df['ror'].cumprod()
        df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

        return df['hpr'][-2]

    except:
        return 1