import pybithumb
import pyupbit
import time
from datetime import datetime
import csv
import telegram
import asyncio


bit_ticker = 'BCH'      # 거래 코인 빗썸 티커
up_ticker = 'KRW-BCH'   # 거래 코인 업빗 티커
price_diff = 650    # 매매 가격차(수수료 0.09% 이상)
min_amount = 0.02   # 해당 코인 최소 거래 수량(5000원 이상)
round_num = 2   # 최소 매매수량 소수점 자릿수


async def telegram_send(text):  # 텔레그램 메시지 전송 함수
    chat_id = 6067152407
    token = "7449204335:AAGhIXcV8x1I8TRrB-yKG-UoXZ7YxPJyN9s"
    bot = telegram.Bot(token = token)
    await bot.send_message(chat_id,text)


with open("keys.txt") as f:     # txt파일 내 업비트, 빗썸 보안키
    lines = f.readlines()
    bit_key = lines[0].strip()
    bit_secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(bit_key, bit_secret)

    up_key = lines[2].strip()
    up_secret = lines[3].strip()
    upbit = pyupbit.Upbit(up_key, up_secret)

def get_bithumb_orderbook(bit_ticker, round_num):    # 빗썸 매수매도 1호가 및 잔량 호출 함수
    bit_orderbook = pybithumb.get_orderbook(bit_ticker)   # 빗썸 오더북
    bit_bids = bit_orderbook['bids']                  # 빗썸 매수대기
    bit_bids_1st = bit_bids[0]                        # 빗썸 매수 1호가, 잔량
    bit_asks = bit_orderbook['asks']                  # 빗썸 매도대기
    bit_asks_1st = bit_asks[0]                        # 빗썸 매도 1호가, 잔량

    bithumb_1st_bids_price = bit_bids_1st['price']         # 빗썸 1호가 매수 가격
    bithumb_1st_bids_quantity = round(bit_bids_1st['quantity'], round_num)        # 빗썸 1호가 매수 잔량
    bithumb_1st_asks_price = bit_asks_1st['price']         # 빗썸 1호가 매도 가격
    bithumb_1st_asks_quantity = round(bit_asks_1st['quantity'], round_num)        # 빗썸 1호가 매도 잔량

    return bithumb_1st_bids_price, bithumb_1st_bids_quantity, bithumb_1st_asks_price, bithumb_1st_asks_quantity

def get_upbit_orderbook(up_ticker, round_num):    # 업빗 매수매도 1호가 및 잔량 호출 함수
    up_orderbook = pyupbit.get_orderbook(up_ticker)    # 업빗 오더북
    up_1st = up_orderbook['orderbook_units'][0]         # 업빗 매수매도대기 1호가, 잔량
    upbit_1st_bids_price = up_1st['bid_price']             # 업빗 1호가 매수 가격
    upbit_1st_bids_size = round(up_1st['bid_size'], round_num)                    # 업빗 1호가 매수 잔량
    upbit_1st_asks_price = up_1st['ask_price']             # 업빗 1호가 매도 가격
    upbit_1st_asks_size = round(up_1st['ask_size'], round_num)                    # 업빗 1호가 매도 잔량

    return upbit_1st_bids_price, upbit_1st_bids_size, upbit_1st_asks_price, upbit_1st_asks_size

def get_balances(bit_ticker, up_ticker, round_num):
    bithumb_balance = bithumb.get_balance(bit_ticker)
    bithumb_balance_coin = round(bithumb_balance[0], round_num)                  # 빗썸 테더 잔고
    bithumb_balance_krw = int(bithumb_balance[2])                   # 빗썸 원화 잔고
    upbit_balance_coin = round(upbit.get_balance(up_ticker), round_num)         # 업빗 테더 잔고
    upbit_balance_krw = int(upbit.get_balance('KRW'))               # 업빗 원화 잔고
    return bithumb_balance_coin, bithumb_balance_krw, upbit_balance_coin, upbit_balance_krw

def trade(bit_ticker, up_ticker, price_diff, min_amount, round_num):
    bithumb_1st_bids_price, bithumb_1st_bids_quantity, bithumb_1st_asks_price, bithumb_1st_asks_quantity = get_bithumb_orderbook(bit_ticker, round_num)
    upbit_1st_bids_price, upbit_1st_bids_size, upbit_1st_asks_price, upbit_1st_asks_size = get_upbit_orderbook(up_ticker, round_num)
    bithumb_balance_coin, bithumb_balance_krw, upbit_balance_coin, upbit_balance_krw = get_balances(bit_ticker, up_ticker, round_num)

    print('****** AUTO PROGRAM START ******')
    print('빗썸 즉시매수 가격, 수량 :', format(bithumb_1st_asks_price, ','), '원,', format(bithumb_1st_asks_quantity, ','), '개')
    print('빗썸 즉시매도 가격, 수량 :', format(bithumb_1st_bids_price, ','), '원,', format(bithumb_1st_bids_quantity, ','), '개')
    print()

    print('업빗 즉시매수 가격, 수량 :', format(upbit_1st_asks_price, ','), '원,', format(upbit_1st_asks_size, ','), '개')
    print('업빗 즉시매도 가격, 수량 :', format(upbit_1st_bids_price, ','), '원,', format(upbit_1st_bids_size, ','), '개')
    print()

    delta_1 = (upbit_1st_bids_price - bithumb_1st_asks_price)
    delta_2 = (bithumb_1st_bids_price - upbit_1st_asks_price)
    print('업빗 즉시매도-빗썸 즉시매수 가격차: ', round(delta_1, round_num), '원')
    print('빗썸 즉시매도-업빗 즉시매수 가격차: ', round(delta_2, round_num), '원')
    print()

    print('빗썸 원화 잔고 :', format(bithumb_balance_krw, ','), '원,', format(bithumb_balance_coin, ','), '개')
    print('업빗 원화 잔고 :', format(upbit_balance_krw, ','), '원,', format(upbit_balance_coin, ','), '개')
    print()

    # 업빗 매도 - 빗썸 매수
    if (upbit_1st_bids_price - bithumb_1st_asks_price) >= price_diff:
        # usdt_amount = bithumb_balance_krw / upbit_1st_asks_price            #빗썸 원화 잔고에 해당하는 테더 수량
        amount = round(min(upbit_1st_bids_size * 0.7, bithumb_1st_asks_quantity * 0.7, upbit_balance_coin), round_num)    # 업빗 매도 1호가 잔량*0.7, 빗썸 매수 1호가 잔량 * 0.7, 업빗 코인 잔고 중 최솟값
        if amount >= min_amount:
            print('빗썸 - ', bithumb_1st_asks_price, '원, ', amount, '개 매수')
            print('업빗 - ', upbit_1st_bids_price, '원, ',  amount, '개 매도')
            try:
                bithumb.buy_market_order(bit_ticker, amount)       # 빗썸 시장가 매수
                upbit.sell_market_order(up_ticker, amount)    # 업빗 시장가 매도

                # 수익 계산
                profit = (round(upbit_1st_bids_price * 0.9995 * amount) - round(bithumb_1st_asks_price * 1.0004 * amount))  # 업빗 매도 정산금액(수수료 0.05%) - 빗썸 매수 정산금액(수수료 0.04%)
                print('매매수익: ', profit, '원')    # 매매수익 출력

                # 매매기록 csv data 추가
                now = datetime.now()
                f = open('profit.csv', 'a', newline='', encoding='UTF-8')
                wr = csv.writer(f)
                wr.writerow([now.strftime('%Y-%m-%d %H:%M:%S'), bit_ticker, bithumb_1st_asks_price, upbit_1st_bids_price, amount, profit, '업빗매도-빗썸매수'])
                f.close()

                # telegram 전송
                upbit_balance_krw = str(upbit_balance_krw)
                bithumb_balance_krw = str(bithumb_balance_krw)
                upbit_balance_coin = str(upbit_balance_coin)
                bithumb_balance_coin = str(bithumb_balance_coin)
                upbit_1st_bids_price = str(upbit_1st_bids_price)
                bithumb_1st_asks_price = str(bithumb_1st_asks_price)
                amount = str(amount)
                profit = str(profit)
                text_ticker = "매매코인: " + bit_ticker + "\n"
                text_up_bal = "업비트 잔고: " + upbit_balance_krw + "원, " + upbit_balance_coin + "개" + "\n"
                text_bit_bal = "빗썸 잔고: " + bithumb_balance_krw + "원, " + bithumb_balance_coin + "개" + "\n"
                text_up_sell = "업비트 매도가: " + upbit_1st_bids_price + "\n"
                text_bit_buy = "빗썸 매수가: " + bithumb_1st_asks_price + "\n"
                text_amount = "매매수량: " + amount + "\n"
                text_profit = "매매수익: " + profit + "원"

                text = text_ticker + text_up_bal + text_bit_bal + text_up_sell + text_bit_buy + text_amount + text_profit
                asyncio.run(telegram_send(text))

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
                    [now.strftime('%Y-%m-%d %H:%M:%S'), bit_ticker, upbit_1st_asks_price, bithumb_1st_bids_price, amount, profit,
                     '빗썸매도-업빗매수'])
                f.close()

                # telegram 전송
                upbit_balance_krw = str(upbit_balance_krw)
                bithumb_balance_krw = str(bithumb_balance_krw)
                upbit_balance_coin = str(upbit_balance_coin)
                bithumb_balance_coin = str(bithumb_balance_coin)
                bithumb_1st_bids_price = str(bithumb_1st_bids_price)
                upbit_1st_asks_price = str(upbit_1st_asks_price)
                amount = str(amount)
                profit = str(profit)
                text_ticker = "매매코인: " + bit_ticker + "\n"
                text_up_bal = "업비트 잔고: " + upbit_balance_krw + "원, " + upbit_balance_coin + "개" + "\n"
                text_bit_bal = "빗썸 잔고: " + bithumb_balance_krw + "원, " + bithumb_balance_coin + "개" + "\n"
                text_bit_sell = "빗썸 매도가: " + bithumb_1st_bids_price + "원" + "\n"
                text_up_buy = "업비트 매수가: " + upbit_1st_asks_price + "원" + "\n"
                text_amount = "매매수량: " + amount + "개" + "\n"
                text_profit = "매매수익: " + profit + "원"

                text = text_ticker + text_up_bal + text_bit_bal + text_bit_sell + text_up_buy + text_amount + text_profit
                asyncio.run(telegram_send(text))

                breakpoint
            except Exception as e:
                print('거래 실패: ', e)


asyncio.run(telegram_send("재정거래 시작"))
while True:
    try:
        trade(bit_ticker, up_ticker, price_diff, min_amount, round_num)
        time.sleep(1)  # 반복간격
    except Exception as e:
        print('Error: ', e)
        time.sleep(5)