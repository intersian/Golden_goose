import pybithumb
import pyupbit
import pandas as pd
import csv


f = open('coin_finder_data.csv', 'w', newline='')
data = ['Ticker','Volatility_avg']
writer = csv.writer(f)
writer.writerow(data)
f.close()

tickers = pybithumb.get_tickers()
for ticker in tickers:
    bit_ticker = ticker
    try:
        df_bit = pybithumb.get_ohlcv(bit_ticker, interval="minute1")
        df_bit = df_bit.iloc[61:]
        df_bit.rename(columns = {'open' : 'bit_open', 'high' : 'bit_high', 'low' : 'bit_low','close' : 'bit_close', 'volume' : 'bit_volume'}, inplace = True)

        # 업빗 분봉 데이터 수신, 1440행(60*24)
        up_ticker = "KRW-" + bit_ticker
        df_up = pyupbit.get_ohlcv(up_ticker, interval='minute1', count=1440)
        df_up.rename(columns = {'open' : 'up_open', 'high' : 'up_high', 'low' : 'up_low','close' : 'up_close', 'volume' : 'up_volume'}, inplace = True)

        # 시간열 기준으로 두 dataframe 합치기
        merge = pd.merge(df_bit, df_up, left_index=True, right_index=True, how='left')
        merge = merge[['bit_open', 'up_open']]
        merge['diff'] = merge['up_open'] - merge['bit_open']
        merge['volatility(%)'] = 100 * merge['diff'] / merge['bit_open']
        merge['volatility(%)'] = round(merge['volatility(%)'], 3)
        avg = merge['volatility(%)'].mean()
        print(ticker, round(avg, 3))

        f = open('coin_finder_data.csv', 'a', newline='', encoding='UTF-8')
        writer = csv.writer(f)
        writer.writerow([ticker, round(avg, 3)])
        f.close()

    except:
        print(ticker, '업비트 비상장')
        f = open('coin_finder_data.csv', 'a', newline='', encoding='UTF-8')
        writer = csv.writer(f)
        writer.writerow([ticker, '업비트 비상장'])
        f.close()