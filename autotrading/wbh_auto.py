import pyupbit
import pybithumb
import time
from datetime import datetime
import requests
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

with open("wbh_keys.txt", encoding='utf-8') as f:
    lines = f.readlines()
    bit_key = lines[0].strip()
    bit_secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(bit_key, bit_secret)

    up_key = lines[2].strip()
    up_secret = lines[3].strip()
    upbit = pyupbit.Upbit(up_key, up_secret)

    upbit_wallet_address = lines[4].strip()
    
    bank_name = lines[5].strip()                # 예: 신한은행
    bank_account = lines[6].strip()             # 예: 계좌번호
    holder_name = lines[7].strip()              # 예: 예금주명

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

##########################################################################################################
###### 업비트 access token 생성
def generate_upbit_token(access_key, secret_key):
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4())
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    return authorize_token

###### 빗썸에서 업비트로 USDT 전송
def transfer_bithumb_to_upbit(amount, address):
    currency = "USDT"
    destination = address  # 업비트의 USDT 지갑 주소
    response = bithumb.bithumb_private_api('/trade/btc_withdrawal', {
        'currency': currency,
        'units': amount,
        'address': destination,
    })
    return response

###### 업비트에서 빗썸으로 원화 전송
def transfer_upbit_to_bithumb(amount):
    upbit_access_token = generate_upbit_token(up_key, up_secret)

    url = "https://api.upbit.com/v1/withdraws/krw"
    headers = {
        "Authorization": upbit_access_token,
        "Content-Type": "application/json"
    }
    data = {
        "amount": amount,
        "bank": bank_name,
        "account": bank_account,
        "holder_name": holder_name
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
##########################################################################################################

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

    #################################################################################################
    ##### 업빗 즉시매도 가격 - 빗썸 즉시매수 가격 ≥ 2원 ===> 빗썸에서 매수, 업빗에서 매도 ################
    #################################################################################################
    if (upbit_1st_bids_price - bithumb_1st_asks_price) >= 2:
        #빗썸, 업빗 원화 잔고에 해당하는 테더 수량
        bithumb_amount = (bithumb_balance_krw / bithumb_1st_asks_price) * 0.7
        upbit_amount = upbit_balance_coin * 0.7
        amount = min(bithumb_amount, upbit_amount, upbit_1st_bids_size * 0.7, bithumb_1st_asks_quantity * 0.7)

        if amount > 0:
            flag = "Y"
            print('빗썸 - ', bithumb_1st_asks_price, '원, ', amount, '개 매수')
            print('업빗 - ', upbit_1st_bids_price, '원, ',  amount, '개 매도')
            try:
                #빗썸 시장가 즉시매수, 업빗 시장가 즉시매도
                bithumb.buy_market_order('USDT', amount)
                upbit.sell_market_order('KRW-USDT', amount)
            except Exception as e:
                print('거래 실패: ', e)

            bithumb_to_upbit_transfer_response = transfer_bithumb_to_upbit(amount, upbit_wallet_address)
            print(bithumb_to_upbit_transfer_response)

            upbit_to_bithumb_transfer_response = transfer_upbit_to_bithumb(upbit_balance_krw)
            print(upbit_to_bithumb_transfer_response)

    ################################################################################################################################
    ##### 빗썸 즉시매수 가격 - 업빗 즉시매도 가격 ≥ 2원 ===> 빗썸에서 매도, 업빗에서 매수(이런 경우는 희박하기 때문에 전송) ################
    ################################################################################################################################

    return flag

while True:
    try:
        now = datetime.now()
        flag = "N"

        if trade(flag) == "Y":
            print("문자열 변환 : ", now.strftime('%Y-%m-%d %H:%M:%S'))
            exit()

        time.sleep(0.15)  # 0.15초마다 반복
        
    except Exception as e:
        print('Error: ', e)
        time.sleep(5)
