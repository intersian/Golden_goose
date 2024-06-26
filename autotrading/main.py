import pybithumb
import pyupbit
import time


with open("keys.txt") as f:
    lines = f.readlines()
    bit_key = lines[0].strip()
    bit_secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(bit_key, bit_secret)

    up_key = lines[2].strip()
    up_secret = lines[3].strip()
    upbit = pyupbit.Upbit(up_key, up_secret)

# 거래할 수량 설정 (예: 1 USDT)
trade_amount = 4

bit_orderbook = pybithumb.get_orderbook('USDT')   # 빗썸 오더북
bit_bids = bit_orderbook['bids']                  # 빗썸 매수대기
bit_bids_1st = bit_bids[0]                        # 빗썸 매수 1호가, 잔량
bit_asks = bit_orderbook['asks']                  # 빗썸 매도대기
bit_asks_1st = bit_asks[0]                        # 빗썸 매도 1호가, 잔량

print('빗썸 즉시매도 가격:', bit_bids_1st['price'])
print('빗썸 즉시매도 잔량:', bit_bids_1st['quantity'])
print('빗썸 즉시매수 가격:', bit_asks_1st['price'])
print('빗썸 즉시매도 잔량:', bit_asks_1st['quantity'])

up_orderbook = pyupbit.get_orderbook('KRW-USDT')    # 업빗 오더북
up_1st = up_orderbook['orderbook_units'][0]         # 업빗 매수매도대기 1호가, 잔량

print('업빗 즉시매도 가격:', up_1st['bid_price'])
print('업빗 즉시매도 잔량:', up_1st['bid_size'])
print('업빗 즉시매수 가격:', up_1st['ask_price'])
print('업빗 즉시매도 잔량:', up_1st['ask_size'])


bit_balance = bithumb.get_balance('USDT')   # 빗썸 잔고 조회
up_balance_coin = upbit.get_balance('KRW-USDT')      # 업빗 잔고 조회
up_balance_krw = upbit.get_balance('KRW')
print('빗썸 테더 잔고:', bit_balance[0])
print('빗썸 원화 잔고:', bit_balance[2])
print('업빗 테더 잔고:', up_balance_coin)
print('업빗 원화 잔고:', up_balance_krw)