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

def get_bithumb_orderbook():
    bithumb_orderbook = pybithumb.get_orderbook('USDT')             # 빗썸 오더북
    bithumb_bids = bithumb_orderbook['bids']                        # 빗썸 매수대기
    bithumb_bids_1st = bithumb_bids[0]                              # 빗썸 매수 1호가, 잔량
    bithumb_asks = bithumb_orderbook['asks']                        # 빗썸 매도대기
    bithumb_asks_1st = bithumb_asks[0]                              # 빗썸 매도 1호가, 잔량

    bithumb_1st_bids_price = int(bithumb_bids_1st['price'])         # 빗썸 1호가 매수 가격
    bithumb_1st_bids_quantity = int(bithumb_bids_1st['quantity'])   # 빗썸 1호가 매수 잔량
    bithumb_1st_asks_price = int(bithumb_asks_1st['price'])         # 빗썸 1호가 매도 가격
    bithumb_1st_asks_quantity = int(bithumb_asks_1st['quantity'])   # 빗썸 1호가 매도 잔량

    return bithumb_1st_bids_price, bithumb_1st_bids_quantity, bithumb_1st_asks_price, bithumb_1st_asks_quantity

def get_upbit_orderbook():
    upbit_orderbook = pyupbit.get_orderbook('KRW-USDT')            # 업빗 오더북
    upbit_1st = upbit_orderbook['orderbook_units'][0]              # 업빗 매수매도대기 1호가, 잔량
    upbit_1st_bids_price = int(upbit_1st['bid_price'])             # 업빗 1호가 매수 가격
    upbit_1st_bids_size = int(upbit_1st['bid_size'])               # 업빗 1호가 매수 잔량
    upbit_1st_asks_price = int(upbit_1st['ask_price'])             # 업빗 1호가 매도 가격
    upbit_1st_asks_size = int(upbit_1st['ask_size'])               # 업빗 1호가 매도 잔량

    return upbit_1st_bids_price, upbit_1st_bids_size, upbit_1st_asks_price, upbit_1st_asks_size

def get_balances():
    bithumb_balance = bithumb.get_balance('USDT')
    bithumb_balance_coin = int(bithumb_balance[0])                  # 빗썸 테더 잔고
    bithumb_balance_krw = int(bithumb_balance[2])                   # 빗썸 원화 잔고
    upbit_balance_coin = int(upbit.get_balance('KRW-USDT'))         # 업빗 테더 잔고
    upbit_balance_krw = int(upbit.get_balance('KRW'))               # 업빗 원화 잔고
    return bithumb_balance_coin, bithumb_balance_krw, upbit_balance_coin, upbit_balance_krw

def trade(flag):
    bithumb_1st_bids_price, bithumb_1st_bids_quantity, bithumb_1st_asks_price, bithumb_1st_asks_quantity = get_bithumb_orderbook()
    upbit_1st_bids_price, upbit_1st_bids_size, upbit_1st_asks_price, upbit_1st_asks_size = get_upbit_orderbook()
    bithumb_balance_coin, bithumb_balance_krw, upbit_balance_coin, upbit_balance_krw = get_balances()

    print('****** AUTO PROGRAM START ******')
    print('빗썸 즉시매수 가격, 수량 :', format(bithumb_1st_asks_price, ','), '원,', format(bithumb_1st_asks_quantity, ','), '개')
    print('빗썸 즉시매도 가격, 수량 :', format(bithumb_1st_bids_price, ','), '원,', format(bithumb_1st_bids_quantity, ','), '개')
    print()

    print('업빗 즉시매수 가격, 수량 :', format(upbit_1st_asks_price, ','), '원,', format(upbit_1st_asks_size, ','), '개')
    print('업빗 즉시매도 가격, 수량 :', format(upbit_1st_bids_price, ','), '원,', format(upbit_1st_bids_size, ','), '개')
    print()

    print('빗썸 원화 잔고 :', format(bithumb_balance_krw, ','), '원,', format(bithumb_balance_coin, ','), '개')
    print()
    print('업빗 원화 잔고 :', format(upbit_balance_krw, ','), '원,', format(upbit_balance_coin, ','), '개')
    print()
    
    bithumb_amount = (bithumb_balance_krw / bithumb_1st_asks_price) * 0.7
    upbit_amount = upbit_balance_coin * 0.7                                          #업빗 원화 잔고에 해당하는 테더 수량
    amount = min(bithumb_amount, upbit_amount, upbit_1st_bids_size * 0.7, bithumb_1st_asks_quantity * 0.7)

    #################################################################################################
    ##### 업빗 즉시매도 가격 - 빗썸 즉시매수 가격 ≥ 2원 이면 빗썸에서 매수, 업빗에서 매도 ################
    #################################################################################################
    # 빗썸에서 매수하고 업빗에서 매도하는 로직
    if (upbit_1st_bids_price - bithumb_1st_asks_price) >= 2:
        bithumb_amount = (bithumb_balance_krw / bithumb_1st_asks_price) * 0.7
        upbit_amount = upbit_balance_coin * 0.7                                          #업빗 원화 잔고에 해당하는 테더 수량
        amount = min(bithumb_amount, upbit_amount, upbit_1st_bids_size * 0.7, bithumb_1st_asks_quantity * 0.7)
        if amount > 0:
            flag = "Y"
            print('빗썸 - ', bithumb_1st_asks_price, '원, ', amount, '개 매수')
            print('업빗 - ', upbit_1st_bids_price, '원, ',  amount, '개 매도')
            try:
                bithumb.buy_market_order('USDT', amount)       # 빗썸 시장가 매수
                upbit.sell_market_order('KRW-USDT', amount)    # 업빗 시장가 매도
            except Exception as e:
                print('거래 실패: ', e)

    ################################################################################################################################
    ##### 빗썸 즉시매수 가격 - 업빗 즉시매도 가격 ≥ 2원 이면 빗썸에서 매도, 업빗에서 매수(이런 경우는 희박하기 때문에 전송) ################
    ################################################################################################################################
    # 빗썸에서 매도하고 업비트에서 매수하는 로직
    # if (bithumb_1st_asks_price - upbit_1st_bids_price) >= 2:
    #     upbit_amount = upbit_balance_coin                                          #업빗 원화 잔고에 해당하는 테더 수량
    #     amount = min(upbit_amount, bithumb_1st_asks_quantity * 0.7, upbit_1st_bids_size * 0.7)
    #     if amount > 0:
    #         print('빗썸 - ', bithumb_1st_asks_price, '원, ', amount, '개 매도')
    #         print('업빗 - ', upbit_1st_bids_price, '원, ',  amount, '개 매수')
            # try:
            #     bithumb.sell_market_order('USDT', str(amount))      # 빗썸 시장가 매도
            #     upbit.buy_market_order('KRW-USDT', amount)     # 업빗 시장가 매수
            # except Exception as e:
            #     print('거래 실패: ', e)

    return flag
    
while True:
    try:
        flag = "N"
        trade(flag)
        time.sleep(1)  # 1초마다 반복
        if trade(flag) == "Y":
            exit()
    except Exception as e:
        print('Error: ', e)
        time.sleep(5)
