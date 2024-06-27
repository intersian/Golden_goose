import pybithumb
import pyupbit


with open("keys.txt") as f:
    lines = f.readlines()
    bit_key = lines[0].strip()
    bit_secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(bit_key, bit_secret)

    up_key = lines[2].strip()
    up_secret = lines[3].strip()
    upbit = pyupbit.Upbit(up_key, up_secret)


up_orderbook = pyupbit.get_orderbook('KRW-USDT')    # 업빗 오더북
up_1st = up_orderbook['orderbook_units'][0]         # 업빗 매수매도대기 1호가, 잔량
upbit_1st_asks_size = up_1st['ask_size']                    # 업빗 1호가 매도 잔량

bit_orderbook = pybithumb.get_orderbook('USDT')  # 빗썸 오더북
bit_bids = bit_orderbook['bids']                  # 빗썸 매수대기
bit_bids_1st = bit_bids[0]                        # 빗썸 매수 1호가, 잔량
bithumb_1st_bids_quantity = bit_bids_1st['quantity']        # 빗썸 1호가 매수 잔량

up_balance_coin = upbit.get_balance('KRW-USDT')  # 업빗 잔고 조회

amount = min(upbit_1st_asks_size * 0.7, bithumb_1st_bids_quantity * 0.7)
print(amount)