import pyupbit
import pybithumb
import time

with open("wbh_keys.txt") as f:
    lines = f.readlines()
    bit_key = lines[0].strip()
    bit_secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(bit_key, bit_secret)

    up_key = lines[2].strip()
    up_secret = lines[3].strip()
    upbit = pyupbit.Upbit(up_key, up_secret)

bit_orderbook = pybithumb.get_orderbook('USDT')             #빗썸 오더북
bit_bids = bit_orderbook['bids']                            #빗썸 매수대기
bit_bids_1st = bit_bids[0]                                  #빗썸 매수 1호가, 잔량
bit_asks = bit_orderbook['asks']                            #빗썸 매도대기
bit_asks_1st = bit_asks[0]                                  #빗썸 매도 1호가, 잔량
bithumb_1st_bids_price = int(bit_bids_1st['price'])         #빗썸 1호가 매도 가격
bithumb_1st_bids_quantity = bit_bids_1st['quantity']        #빗썸 1호가 매도 잔량
bithumb_1st_asks_price = int(bit_asks_1st['price'])         #빗썸 1호가 매수 가격
bithumb_1st_asks_quantity = bit_asks_1st['quantity']        #빗썸 1호가 매수 잔량

print('빗썸 즉시매도 가격:', bithumb_1st_bids_price)
print('빗썸 즉시매도 잔량:', bithumb_1st_bids_quantity)
print('빗썸 즉시매수 가격:', bithumb_1st_asks_price)
print('빗썸 즉시매수 잔량:', bithumb_1st_asks_quantity)
print()

up_orderbook = pyupbit.get_orderbook('KRW-USDT')            #업빗 오더북
up_1st = up_orderbook['orderbook_units'][0]                 #업빗 매수매도대기 1호가, 잔량
upbit_1st_bids_price = int(up_1st['bid_price'])             #업빗 1호가 매도 가격
upbit_1st_asks_size = up_1st['bid_size']                    #업빗 1호가 매도 잔량
upbit_1st_asks_price = int(up_1st['ask_price'])             #업빗 1호가 매수 가격
upbit_1st_asks_size = up_1st['ask_size']                    #업빗 1호가 매수 잔량

print('업빗 즉시매도 가격:', upbit_1st_bids_price)
print('업빗 즉시매도 잔량:', upbit_1st_asks_size)
print('업빗 즉시매수 가격:', upbit_1st_asks_price)
print('업빗 즉시매수 잔량:', upbit_1st_asks_size)
print()


#################################################################################################
###### 업비트의 매수대기 1호가 - 빗썸의 매도대기 1호가 ≥ 2원 이면 업비트에서 매도, 빗썸에서 매수 ######
#################################################################################################

if (upbit_1st_asks_price - bithumb_1st_bids_price) >= 2:
    ##1. 업비트 매도, 빗썸 매수 로직 작성.
    ##2. 텔레그램으로 알림.
    print("업비트가 더 비쌈.")


################################################################################################################################
###### 빗썸의 매수대기 1호가 - 업비트의 매도대기 1호가 ≥ 2원 이면 업비트에서 매수, 빗썸에서 매도(이런 경우는 희박하기 때문에 전송) ######
################################################################################################################################

if (bithumb_1st_asks_price - upbit_1st_bids_price) >= 2:
    ##업비트 매수, 빗썸 매도 전송 로직 작성.
    print("빗썸이 더 비쌈.")


bit_balance = bithumb.get_balance('USDT')                   #빗썸 잔고 조회
up_balance_coin = upbit.get_balance('KRW-USDT')             #업빗 잔고 조회
up_balance_krw = upbit.get_balance('KRW')
print('빗썸 테더 잔고:', bit_balance[0])
print('빗썸 원화 잔고:', bit_balance[2])
print('업빗 테더 잔고:', up_balance_coin)
print('업빗 원화 잔고:', up_balance_krw)
print()


'''
def repeat_task():
    while True:
        # 여기에 실행할 코드를 추가하세요
        print("0.1초마다 동작 실행")
        
        # 0.1초 대기
        time.sleep(0.1)

# 함수 호출
repeat_task()
'''








# Coins = pyupbit.get_tickers(fiat="KRW")

'''
# 업비트 현재가 매수매도 
for coin in Coins:
    print(coin, pyupbit.get_current_price(coin))
    time.sleep(0.1)

    if coin == "KRW-BTC" or coin == "KRW-TRX":
        upbit.buy_market_order("KRW-XRP", 10000)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BUY DONE : ", coin)


btc_balance = upbit.get_balance("KRW-BTC")

print(upbit.sell_market_order("KRW-BTC", btc_balance))
'''


'''
# 지정가 매수매도
btc_now_price = pyupbit.get_current_price("KRW-BTC")
btc_now_price = btc_now_price * 0.998

won = 10000

print(upbit.buy_limit_order("KRW-BTC", pyupbit.get_tick_size(btc_now_price), (won / btc_now_price) ))
'''


'''
# 내 코인 잔고와 수익률 계산
my_balances = upbit.get_balances()

for coin_balance in my_balances:
    ticker = coin_balance['currency']
    if ticker == "KRW" or ticker == "XRP":
        continue

    # print(coin_balance)
    # print(ticker, coin_balance['balance'], coin_balance['avg_buy_price'])

    nowPrice = pyupbit.get_current_price("KRW-" + ticker)
    avg_price = float(coin_balance['avg_buy_price'])

    print("nowPrice :: ", nowPrice)

    revenu_rate = (nowPrice - avg_price) / avg_price * 100.0
    print("revenu_rate :: ", revenu_rate)

    if revenu_rate >= 1.5:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!in")
        print(upbit.sell_limit_order("KRW-" + ticker, pyupbit.get_tick_size(nowPrice * 1.001), coin_balance['balance']))


# print(my_balances)
# [{'currency': 'BTC', 'balance': '0.00183575', 'locked': '0', 'avg_buy_price': '97033396.27944982', 'avg_buy_price_modified': False, 'unit_currency': 'KRW'},
#  {'currency': 'KRW', 'balance': '0.5230437', 'locked': '0', 'avg_buy_price': '0', 'avg_buy_price_modified': True, 'unit_currency': 'KRW'},
#  {'currency': 'XRP', 'balance': '0.00000062', 'locked': '0', 'avg_buy_price': '905.99999974', 'avg_buy_price_modified': False, 'unit_currency': 'KRW'},
#  {'currency': 'SC', 'balance': '570.16536776', 'locked': '0', 'avg_buy_price': '16.65', 'avg_buy_price_modified': False, 'unit_currency': 'KRW'},
#  {'currency': 'SHIB', 'balance': '505986.84210526', 'locked': '0', 'avg_buy_price': '0.057', 'avg_buy_price_modified': False, 'unit_currency': 'KRW'}]
'''


'''
# 차트 데이터 보기
tickers = pyupbit.get_tickers("KRW")

for ticker in tickers:
    if ticker == "KRW-BTC":
        df = pyupbit.get_ohlcv(ticker, interval="day")
        # print(df['open'].iloc[-2])
        # print(df['open'].iloc[-1])
        print(df)
        break
'''



