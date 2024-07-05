import pybithumb
import pyupbit
import time
from datetime import datetime
import csv

bit_ticker = 'DOGE'
up_ticker = 'KRW-DOGE'
price_diff = 0.5
min_amount = 40


with open("keys.txt") as f:
    lines = f.readlines()
    bit_key = lines[0].strip()
    bit_secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(bit_key, bit_secret)

    up_key = lines[2].strip()
    up_secret = lines[3].strip()
    upbit = pyupbit.Upbit(up_key, up_secret)

def get_bithumb_orderbook(bit_ticker):    # 빗썸 매수매도 1호가 및 잔량 호출 함수
    bit_orderbook = pybithumb.get_orderbook(bit_ticker)   # 빗썸 오더북
    bit_bids = bit_orderbook['bids']                  # 빗썸 매수대기
    bit_bids_1st = bit_bids[0]                        # 빗썸 매수 1호가, 잔량
    bit_asks = bit_orderbook['asks']                  # 빗썸 매도대기
    bit_asks_1st = bit_asks[0]                        # 빗썸 매도 1호가, 잔량

    bithumb_1st_bids_price = bit_bids_1st['price']         # 빗썸 1호가 매수 가격
    bithumb_1st_bids_quantity = int(bit_bids_1st['quantity'])        # 빗썸 1호가 매수 잔량
    bithumb_1st_asks_price = bit_asks_1st['price']         # 빗썸 1호가 매도 가격
    bithumb_1st_asks_quantity = int(bit_asks_1st['quantity'])        # 빗썸 1호가 매도 잔량

    return bithumb_1st_bids_price, bithumb_1st_bids_quantity, bithumb_1st_asks_price, bithumb_1st_asks_quantity

def get_upbit_orderbook(up_ticker):    # 업빗 매수매도 1호가 및 잔량 호출 함수
    up_orderbook = pyupbit.get_orderbook(up_ticker)    # 업빗 오더북
    up_1st = up_orderbook['orderbook_units'][0]         # 업빗 매수매도대기 1호가, 잔량
    upbit_1st_bids_price = up_1st['bid_price']             # 업빗 1호가 매수 가격
    upbit_1st_bids_size = int(up_1st['bid_size'])                    # 업빗 1호가 매수 잔량
    upbit_1st_asks_price = up_1st['ask_price']             # 업빗 1호가 매도 가격
    upbit_1st_asks_size = int(up_1st['ask_size'])                    # 업빗 1호가 매도 잔량

    return upbit_1st_bids_price, upbit_1st_bids_size, upbit_1st_asks_price, upbit_1st_asks_size

def get_balances(bit_ticker, up_ticker):
    bithumb_balance = bithumb.get_balance(bit_ticker)
    bithumb_balance_coin = int(bithumb_balance[0])                  # 빗썸 테더 잔고
    bithumb_balance_krw = int(bithumb_balance[2])                   # 빗썸 원화 잔고
    upbit_balance_coin = int(upbit.get_balance(up_ticker))         # 업빗 테더 잔고
    upbit_balance_krw = int(upbit.get_balance('KRW'))               # 업빗 원화 잔고
    return bithumb_balance_coin, bithumb_balance_krw, upbit_balance_coin, upbit_balance_krw

def trade(bit_ticker, up_ticker, price_diff, min_amount):
    bithumb_1st_bids_price, bithumb_1st_bids_quantity, bithumb_1st_asks_price, bithumb_1st_asks_quantity = get_bithumb_orderbook(bit_ticker)
    upbit_1st_bids_price, upbit_1st_bids_size, upbit_1st_asks_price, upbit_1st_asks_size = get_upbit_orderbook(up_ticker)
    bithumb_balance_coin, bithumb_balance_krw, upbit_balance_coin, upbit_balance_krw = get_balances(bit_ticker, up_ticker)

    print('****** AUTO PROGRAM START ******')
    print('빗썸 즉시매수 가격, 수량 :', format(bithumb_1st_asks_price, ','), '원,', format(bithumb_1st_asks_quantity, ','), '개')
    print('빗썸 즉시매도 가격, 수량 :', format(bithumb_1st_bids_price, ','), '원,', format(bithumb_1st_bids_quantity, ','), '개')
    print()

    print('업빗 즉시매수 가격, 수량 :', format(upbit_1st_asks_price, ','), '원,', format(upbit_1st_asks_size, ','), '개')
    print('업빗 즉시매도 가격, 수량 :', format(upbit_1st_bids_price, ','), '원,', format(upbit_1st_bids_size, ','), '개')
    print()

    delta_1 = (upbit_1st_bids_price - bithumb_1st_asks_price)
    delta_2 = (bithumb_1st_bids_price - upbit_1st_asks_price)
    print('업빗 즉시매도-빗썸 즉시매수 가격차: ', delta_1, '원')
    print('빗썸 즉시매도-업빗 즉시매수 가격차: ', delta_2, '원')
    print()

    print('빗썸 원화 잔고 :', format(bithumb_balance_krw, ','), '원,', format(bithumb_balance_coin, ','), '개')
    print('업빗 원화 잔고 :', format(upbit_balance_krw, ','), '원,', format(upbit_balance_coin, ','), '개')
    print()

    # 업빗 매도 - 빗썸 매수
    if (upbit_1st_bids_price - bithumb_1st_asks_price) >= price_diff:
        # usdt_amount = bithumb_balance_krw / upbit_1st_asks_price            #빗썸 원화 잔고에 해당하는 테더 수량
        amount = int(min(upbit_1st_bids_size * 0.7, bithumb_1st_asks_quantity * 0.7, upbit_balance_coin))    # 업빗 매도 1호가 잔량*0.7, 빗썸 매수 1호가 잔량 * 0.7, 업빗 코인 잔고 중 최솟값
        if amount >= min_amount:
            print('빗썸 - ', bithumb_1st_asks_price, '원, ', amount, '개 매수')
            print('업빗 - ', upbit_1st_bids_price, '원, ',  amount, '개 매도')
            try:
                bithumb.buy_market_order(bit_ticker, amount)       # 빗썸 시장가 매수
                upbit.sell_market_order(up_ticker, amount)    # 업빗 시장가 매도

                profit = (round(upbit_1st_bids_price * 0.9995 * amount) - round(bithumb_1st_asks_price * 1.0004 * amount))  # 업빗 매도 정산금액(수수료 0.05%) - 빗썸 매수 정산금액(수수료 0.04%)
                print('매매수익: ', profit, '원')    # 매매수익 출력

                now = datetime.now()
                f = open('profit.csv', 'a', newline='', encoding='UTF-8')
                wr = csv.writer(f)
                wr.writerow([now.strftime('%Y-%m-%d %H:%M:%S'), bithumb_1st_asks_price, upbit_1st_bids_price, amount, profit, '업빗매도-빗썸매수'])
                f.close()

                breakpoint
            except Exception as e:
                print('거래 실패: ', e)

    # 빗썸 매도 - 업빗 매수
    if (bithumb_1st_bids_price - upbit_1st_asks_price) >= price_diff:
        # usdt_amount = bithumb_balance_krw / upbit_1st_asks_price            #빗썸 원화 잔고에 해당하는 테더 수량
        amount = int(min(bithumb_1st_bids_quantity * 0.7, upbit_1st_asks_size * 0.7, bithumb_balance_coin))  # 빗썸 매도 1호가 잔량*0.7, 업빗 매수 1호가 잔량*0.7, 빗썸 코인 잔고 중 최솟값
        if amount >= min_amount:
            print('빗썸 - ', bithumb_1st_asks_price, '원, ', amount, '개 매도')
            print('업빗 - ', upbit_1st_bids_price, '원, ',  amount, '개 매수')
            try:
                bithumb.sell_market_order(bit_ticker, amount)      # 빗썸 시장가 매도
                upbit.buy_market_order(up_ticker, amount)     # 업빗 시장가 매수

                profit = (round(bithumb_1st_asks_price * 0.9996) - round(upbit_1st_bids_price * 1.0005)) * amount   # 빗썸 매도 정산금액(수수료 0.04%) - 업빗 매도 정산금액(수수료 0.05%)
                print('매매수익: ', profit, '원')    # 매매수익 출력

                now = datetime.now()
                f = open('profit.csv', 'a', newline='', encoding='UTF-8')
                wr = csv.writer(f)
                wr.writerow(
                    [now.strftime('%Y-%m-%d %H:%M:%S'), upbit_1st_asks_price, bithumb_1st_bids_price, amount, profit,
                     '빗썸매도-업빗매수'])
                f.close()

                breakpoint
            except Exception as e:
                print('거래 실패: ', e)

while True:
    try:
        trade(bit_ticker, up_ticker, price_diff, min_amount)
        time.sleep(1)  # 반복간격
    except Exception as e:
        print('Error: ', e)
        time.sleep(5)