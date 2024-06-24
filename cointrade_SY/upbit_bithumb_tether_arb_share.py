import asyncio
import telegram
import pybithumb
import time
import myapi2
import pyupbit
import traceback #에러메시지 관리용

# Bithumb API 정보
BITHUMB_API_KEY = myapi2.bithumb_api_key()
BITHUMB_SECRET_KEY = myapi2.bithumb_secret_key()
BITHUMB_API_URL = 'https://api.bithumb.com'

# UPBIT API 정보
UPBIT_API_KEY = myapi2.upbit_api_key()
UPBIT_SECRET_KEY = myapi2.upbit_secret_key()

upbit = pyupbit.Upbit(UPBIT_API_KEY, UPBIT_SECRET_KEY)
bithumb = pybithumb.Bithumb(BITHUMB_API_KEY, BITHUMB_SECRET_KEY)

def upbit_tick_round(price):
    if price >= 2000000:
        tick_size = round(price / 1000) * 1000
    elif price >= 1000000:
        tick_size = round(price / 500) * 500
    elif price >= 500000:
        tick_size = round(price / 100) * 100
    elif price >= 100000:
        tick_size = round(price / 50) * 50
    elif price >= 10000:
        tick_size = round(price / 10) * 10
    elif price >= 1000:
        tick_size = round(price / 5) * 5
    elif price >= 100:
        tick_size = round(price / 0.1) * 0.1
    elif price >= 10:
        tick_size = round(price / 0.01) * 0.01
    elif price >= 1:
        tick_size = round(price / 0.001) * 0.001
    else:
        tick_size = round(price / 0.0001) * 0.0001

    return tick_size

# 텔레그램 메세지
async def send_message(text):
    # token = "Token 번호 입력-텔레그램 봇 설정 후 token 번호" # telegram 셋팅. 인터넷 참조
    bot = telegram.Bot(token)
    # chat_id = "chat_id번호" #  텔레그램 자동봇에서 내 계정으로의 chat_id 임. 인터넷 참조
    async with bot:
        await bot.send_message(chat_id=chat_id, text=text)

# 매수 1호가, 2호가 등.. - 코인 매도시 필요 - 업비트
def upbit_orderbook_calculation_bid(orderbook):
    # 매수1호가 등 가격 계산 - 타겟 매도가격 포함
    best_sell_price = float(orderbook['orderbook_units'][0]['bid_price'])
    bid_quantity = orderbook['orderbook_units'][0]['bid_size']
    bid_value = best_sell_price * bid_quantity

    return [best_sell_price, bid_value]

def upbit_orderbook_calculation_ask(orderbook):
    # 매수1호가 등 가격 계산 - 타겟 매도가격 포함
    best_buy_price = float(orderbook['orderbook_units'][0]['ask_price'])
    ask_quantity = orderbook['orderbook_units'][0]['ask_size']
    ask_value = best_buy_price * ask_quantity

    return [best_buy_price, ask_value]

# 매수 1호가, 2호가 등.. - 코인 매도시 필요 - 빗썸
def bithumb_orderbook_calculation_bid(orderbook):
    # 매수1호가 등 가격 계산 - 타겟 매도가격 포함
    best_sell_price = float(orderbook['bids'][0]['price'])
    bid_quantity = orderbook['bids'][0]['quantity']
    bid_value = best_sell_price * bid_quantity

    return [best_sell_price, bid_value]

# 매도 1호가, 2호가 등... - 코인 매수시 필요
def bithumb_orderbook_calculation_ask(orderbook):
    # 매수1호가 등 가격 계산 - 타겟 매도가격 포함
    best_buy_price = float(orderbook['asks'][0]['price'])
    ask_quantity = orderbook['asks'][0]['quantity']
    ask_value = best_buy_price * ask_quantity

    return [best_buy_price, ask_value]

# BITHUMB 매수
def bithumb_buy_market_order(coin, order_quantity):
    # 시장가 매수 주문
    result = bithumb.buy_market_order(coin, order_quantity)
    return result

# BITHUMB 매도
def bithumb_sell_market_order(coin, order_quantity):
    # 시장가 매도 주문
    result = bithumb.sell_market_order(coin, order_quantity)
    return result

# UPBIT 지정가 매수
def upbit_buy_limit_order(upbit_coin, order_quantity, bid_price): # bid_price: 업비트 슬리피지를 고려한 매도 호가, 여기서의 bid_price는 나의 bidding 가격
    result = upbit.buy_limit_order(upbit_coin, bid_price, order_quantity)
    return result

# UPBIT 지정가 매도
def upbit_sell_limit_order(upbit_coin, order_quantity, ask_price): # ask_price: 업비트 슬리피지를 고려한 매수 호가, 여기서의 ask_price는 나의 ask 가격
    result = upbit.sell_limit_order(upbit_coin, ask_price, order_quantity)
    return result

# UPBIT 지정가 매수 - 잔량없을때까지 - Target price는 슬리피지 고려한 매수가격
# 오더북은 매수가 잘 안됐을때 다시 로드
def upbit_buy_limit_all(upbit_coin, order_quantity, target_price, time_sleep):
    initial_order = upbit_buy_limit_order(upbit_coin, order_quantity, target_price)
    initial_order_uuid = initial_order['uuid']

    reorder_count = 0
    upbit_size = 0

    while True:
        time.sleep(0.7)
        # 주문 취소하기 -- 정보 받고 그사이에 체결되는 것을 방지
        upbit.cancel_order(initial_order_uuid)
        order_status = upbit.get_order(initial_order_uuid)

        if order_status['state'] == 'done': #주문 완료된 경우
            upbit_transaction = order_status['trades']
            for contract in upbit_transaction:
                upbit_size += float(contract['funds'])  # 재주문없이 한번에 거래가된 경우 - 0에서 바로 더해짐, 재주문이 있는 경우, loop 내에서 합쳐졌을 것
            break
        else: #주문 완료되지 않은 경우
            remaining_quantity = order_status['remaining_volume']

            #취소 후 체결내역 확인하여, 거래 사이즈 더하기
            upbit_transaction = order_status['trades']
            for contract in upbit_transaction:
                upbit_size += float(contract['funds'])  # 재주문없이 한번에 거래가된 경우

            time.sleep(time_sleep)

            upbit_orderbook = pyupbit.get_orderbook(f"KRW-{coin}")
            best_buy_price = float(upbit_orderbook['orderbook_units'][0]['ask_price'])

            # 매수에서 slippage고려하므로, 1 + slippage를 곱해줌
            target_price_new = best_buy_price

            new_order = upbit_buy_limit_order(upbit_coin, remaining_quantity, target_price_new)
            initial_order_uuid = new_order['uuid']

            reorder_count+=1

    return upbit_size, reorder_count

# UPBIT 지정가 매도 - 잔량없을때까지 - Target price는 슬리피지 고려한 매도가격
# 오더북은 매도가 잘 안됐을때 다시 로드
def upbit_sell_limit_all(upbit_coin, order_quantity, target_price, time_sleep):

    initial_order = upbit_sell_limit_order(upbit_coin, order_quantity, target_price)
    initial_order_uuid = initial_order['uuid']

    reorder_count = 0
    upbit_size = 0

    while True:
        time.sleep(0.7)
        # 주문 취소하기 -- 정보 받고 그사이에 체결되는 것을 방지
        upbit.cancel_order(initial_order_uuid)
        order_status = upbit.get_order(initial_order_uuid)

        if order_status['state'] == 'done': #주문 완료된 경우
            upbit_transaction = order_status['trades']
            for contract in upbit_transaction:
                upbit_size += float(contract['funds'])  # 재주문없이 한번에 거래가된 경우 - 0에서 바로 더해짐, 재주문이 있는 경우, loop 내에서 합쳐졌을 것
            break
        else: #주문 완료되지 않은 경우
            remaining_quantity = order_status['remaining_volume']

            # 취소 후 체결내역 확인하여, 거래 사이즈 더하기
            upbit_transaction = order_status['trades']
            for contract in upbit_transaction:
                upbit_size += float(contract['funds'])  # 재주문없이 한번에 거래가된 경우

            time.sleep(time_sleep)

            upbit_orderbook = pyupbit.get_orderbook(f"KRW-{coin}")
            best_sell_price = float(upbit_orderbook['orderbook_units'][0]['bid_price'])

            # 매도에서 slippage고려하므로, 1 - slippage를 곱해줌
            target_price_new = best_sell_price

            new_order = upbit_sell_limit_order(upbit_coin, remaining_quantity, target_price_new)
            initial_order_uuid = new_order['uuid']

            reorder_count += 1

    return upbit_size, reorder_count

###########################
## 거래 실행관련 수익계산 ##
###########################
def profit_calculation(coin):
    upbit_coin = "KRW-" + coin

    # 업비트 - 코인의 best sell 조건
    upbit_orderbook = pyupbit.get_orderbook(upbit_coin)
    upbit_best_sell_price, upbit_total_bid_value = upbit_orderbook_calculation_bid(upbit_orderbook)

    # 빗썸 - 테더의 best buy 조건
    bithumb_orderbook = pybithumb.get_orderbook(coin, limit=5)
    bithumb_best_buy_price, bithumb_total_ask_value = bithumb_orderbook_calculation_ask(bithumb_orderbook)

    # 업비트 - 코인의 best buy 조건
    upbit_orderbook = pyupbit.get_orderbook(upbit_coin)
    upbit_best_buy_price, upbit_total_ask_value = upbit_orderbook_calculation_ask(upbit_orderbook)

    # 빗썸 - 테더의 best sell 조건
    bithumb_orderbook = pybithumb.get_orderbook(coin, limit=5)
    bithumb_best_sell_price, bithumb_total_bid_value = bithumb_orderbook_calculation_bid(bithumb_orderbook)

    # 공통 수수료 계산
    fee_upbit = 0.05 / 100
    fee_bithumb = 0.04 / 100
    fee_total = fee_upbit + fee_bithumb


    profit_upbit = (upbit_best_sell_price - bithumb_best_buy_price) / upbit_best_sell_price
    net_profit_upbit = profit_upbit - fee_total

    profit_bithumb = (bithumb_best_sell_price - upbit_best_buy_price) / bithumb_best_sell_price
    net_profit_bithumb = profit_bithumb - fee_total


    return profit_upbit, net_profit_upbit, profit_bithumb, net_profit_bithumb, upbit_total_bid_value, upbit_total_ask_value, bithumb_total_bid_value, bithumb_total_ask_value,upbit_best_buy_price, upbit_best_sell_price, bithumb_best_buy_price, bithumb_best_sell_price



if __name__=="__main__":

    condition_continue = True  # while loop 내 에러발생시 진행여부를 판단하기 위한 초기값 셋팅
    print("업비트-빗썸간 테더 재정거래")
    coin = "USDT"
    upbit_coin = "KRW-USDT"

    # 현재 자산 계산
    upbit_coin_balance = upbit.get_balance(upbit_coin)
    upbit_krw_balance = upbit.get_balance("KRW")
    bithumb_coin_balance = bithumb.get_balance(coin)[0]
    bithumb_krw_balance = bithumb.get_balance(coin)[2]

    # 현재 상황 계산
    profit_upbit, net_profit_upbit, profit_bithumb, net_profit_bithumb, upbit_total_bid_value, upbit_total_ask_value, bithumb_total_bid_value, bithumb_total_ask_value, upbit_best_buy_price, upbit_best_sell_price, bithumb_best_buy_price, bithumb_best_sell_price = profit_calculation(coin)

    # 현재테더, 10당 차이...
    print(f"업비트 매도/매수호가: ")
    print(f"업비트 매도시 이익 / 순이익 (%) : {round(profit_upbit * 100,2)} / {round(net_profit_upbit * 100,2)}")
    print(f"빗썸 매도시 이익 / 순이익 (%) : {round(profit_bithumb * 100, 2)} / {round(net_profit_bithumb* 100,2)}")
    print(f"업비트 / 빗썸 보유 {coin} 개수 : {upbit_coin_balance} / {bithumb_coin_balance}")
    print(f"업비트 / 빗썸 보유 원화(원)) : {format(round(upbit_krw_balance),',')} / {format(round(bithumb_krw_balance),',')}")

    condition_upbit_sell_value = float(input("업비트 매도시 조건(원) : ")) # 업비트 매도시 조건
    condition_bithumb_sell_value = float(input("빗썸 매도시 조건(원) : ")) # 빗썸 매도시 조건
    time_sleep = float(input("재주문 시도시간(s)(ex:1~5) : ")) # 미체결시 재주문 시도시간
    print("\n")
    print(f"현재 총 {coin} 개수: {upbit_coin_balance + bithumb_coin_balance} (참고)")
    coin_transaction_amount = int(input("거래개수(정수단위로) : ")) # 한번 거래시 코인거래 개수
    total_amount = float(input("합산운용 코인개수 : "))
    amount_upbit = float(input("보유 업비트코인개수 : "))
    amount_bithumb = total_amount - amount_upbit

    # 보유 자산이 거래셋팅대비 부족한 경우
    total_krw_amount = total_amount * upbit_best_buy_price
    condition_upbit_krw = total_krw_amount > upbit_krw_balance
    condition_bithumb_krw = total_krw_amount > bithumb_krw_balance
    condition_upbit_coin = amount_upbit > upbit_coin_balance
    condition_bithumb_coin = amount_bithumb > upbit_coin_balance

    if condition_upbit_krw or condition_bithumb_krw or condition_upbit_coin or condition_bithumb_coin:
        balance_text0 = f"재정거래 - {coin} 거래 잔액에러 발생!!\n"

        if condition_upbit_krw:
            balance_text1 = "1. 업비트 원화 부족!!\n"
        else:
            balance_text1 = "1. 업비트 원화 정상\n"

        if condition_bithumb_krw:
            balance_text2 = "2. 빗썸 원화 부족!!\n"
        else:
            balance_text2 = "2. 빗썸 원화 정상\n"

        if condition_upbit_coin:
            balance_text3 = f"3. 업비트 {coin} 부족!!\n"
        else:
            balance_text3 = f"3. 업비트 {coin} 정상\n"

        if condition_bithumb_coin:
            balance_text4 = f"4. 빗썸 {coin} 부족!!"
        else:
            balance_text4 = f"4. 빗썸 {coin} 정상"

        text = balance_text0 + balance_text1 + balance_text2 + balance_text3 + balance_text4
        print(text)
        asyncio.run(send_message(text))

        raise Exception('자산 에러 발생')

    while True:

        # 원화 잔고확인 후 안될 경우 종료 및 메세지 송달 필요

        try:
            condition_continue = True  # 에러 발생시, 진행조건 초기화

            profit_upbit, net_profit_upbit, profit_bithumb, net_profit_bithumb, upbit_total_bid_value, upbit_total_ask_value, bithumb_total_bid_value, bithumb_total_ask_value, upbit_best_buy_price, upbit_best_sell_price, bithumb_best_buy_price, bithumb_best_sell_price = profit_calculation(coin)

            # CASE별 계산
            upbit_sell_case_percent = profit_upbit * 100
            bithumb_sell_case_percent = profit_bithumb * 100

            upbit_sell_case_value = upbit_best_sell_price - bithumb_best_buy_price
            bithumb_sell_case_value = bithumb_best_sell_price - upbit_best_buy_price


            # 기타 정의 - 업비트 거래액, 빗썸 거래액 (1회거래액)
            upbit_amount_won = upbit_best_sell_price * coin_transaction_amount
            bithumb_amount_won = bithumb_best_sell_price * coin_transaction_amount

            # 업비트 매도조건 만족시 & 업비트 보유량이 거래 코인숫자보다 많을 시, 슬리피지 감안했을때, 업비트 매도 및 빗썸 매수 소화 가능할 시 (1회거래액 2배 이상)
            if upbit_sell_case_value > condition_upbit_sell_value and (amount_upbit >= coin_transaction_amount) and (upbit_total_bid_value > upbit_amount_won * 2) and (bithumb_total_ask_value > bithumb_amount_won * 2):

                target_price = upbit_best_sell_price
                upbit_size, reorder_count = upbit_sell_limit_all(upbit_coin, coin_transaction_amount, target_price,time_sleep) # 업비트 매도, 업비트 value랑 재주문 횟수 로드

                # UnderMinTotalAsk 라는 에러 뜸
                # InsufficientFundsAsk 라는 에러 뜸 -- 이는 팔 물량이 부족할때 주문 넣는 경우..
                condition_continue = False

                result_bithumb = bithumb_buy_market_order(coin, coin_transaction_amount)  # 빗썸 매수

                condition_continue = True

                # 체결내역 확인
                # 빗썸
                bithumb_transaction = bithumb.get_order_completed(result_bithumb)['data']['contract']
                bithumb_size = 0
                for contract in bithumb_transaction:
                    bithumb_size += float(contract['total'])  # 거래된 총 size를 계산 (KRW)

                if bithumb_size == 0:
                    time.sleep(1)
                    bithumb_transaction = bithumb.get_order_completed(result_bithumb)['data']['contract']
                    bithumb_size = 0
                    for contract in bithumb_transaction:
                        bithumb_size += float(contract['total'])  # 거래된 총 size를 계산 (KRW)
                if bithumb_size == 0:
                    bithumb_size = 1

                # 빗썸 평균 매수/매도 체결 가격 계산: total KRW 사이즈를 주문한 코인개수로 나눈 값
                bithumb_avg = bithumb_size / coin_transaction_amount
                # 업비트
                upbit_avg = upbit_size / coin_transaction_amount

                # 각 거래소별 코인개수 조정
                amount_upbit -= coin_transaction_amount
                amount_bithumb += coin_transaction_amount

                # 수수료 계산
                bithumb_fee = bithumb_avg * coin_transaction_amount * 0.04 / 100
                upbit_fee = upbit_avg * coin_transaction_amount * 0.05 / 100
                total_fee = bithumb_fee + upbit_fee

                # 이익금 계산
                profit = (upbit_avg - bithumb_avg) * coin_transaction_amount
                net_profit = profit - total_fee

                # 메세지 텔레그램 전송을 위한 process
                text0 = str(coin) + " 업비트 매도 실행 완료\n"
                text1 = "업비트 평균체결가격 : " + str(round(upbit_avg,2)) + "\n"
                text2 = "빗썸 평균체결가격 : " + str(round(bithumb_avg,2)) + "\n"
                text3 = "업비트 매도차액(원) / 목표(원) : " + str(round((upbit_avg - bithumb_avg),1)) + " / " + str(condition_upbit_sell_value) + "\n"
                text4 = "순수익금(원) : " + str(round(net_profit,1)) + "\n"
                text5 = "거래수량  : " + str(coin_transaction_amount) + "\n"
                text6 = "업비트 재주문횟수 : " + str(reorder_count) + "\n"
                text7 = "총수량 / 업비트 / 빗썸 : " + str(total_amount) + " / " + str(amount_upbit) + " / " + str(amount_bithumb) + "\n"
                text8 = "업비트 거래액 / 빗썸 거래액 : " + str(upbit_size) + " / " + str(bithumb_size)

                text = text0 + text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8

                print(text)

                # 업비트 빗썸 거래체결 결과 로드 확인 필요..
                asyncio.run(send_message(text))

                time.sleep(0.5)


            # 빗썸 매도조건 만족시 & 빗썸 보유량이 거래 코인숫자보다 많을 시 --------
            if (bithumb_sell_case_value > condition_bithumb_sell_value) and (amount_bithumb >= coin_transaction_amount) and (upbit_total_ask_value > upbit_amount_won * 2) and (bithumb_total_bid_value > bithumb_amount_won * 2):

                target_price = upbit_best_buy_price # 업비트용 target price 계산 - 함수 활용하여 호가 단위 확보
                upbit_size, reorder_count = upbit_buy_limit_all(upbit_coin, coin_transaction_amount, target_price, time_sleep)  # 업비트 매수

                condition_continue = False

                result_bithumb = bithumb_sell_market_order(coin, coin_transaction_amount)  # 빗썸 매도

                condition_continue = True

                # 체결내역 확인
                # 빗썸
                bithumb_transaction = bithumb.get_order_completed(result_bithumb)['data']['contract']
                bithumb_size = 0
                for contract in bithumb_transaction:
                    bithumb_size += float(contract['total'])  # 거래된 총 size를 계산 (KRW)
                if bithumb_size == 0:
                    time.sleep(1)
                    bithumb_transaction = bithumb.get_order_completed(result_bithumb)['data']['contract']
                    bithumb_size = 0
                    for contract in bithumb_transaction:
                        bithumb_size += float(contract['total'])  # 거래된 총 size를 계산 (KRW)
                if bithumb_size == 0:
                    bithumb_size = 1

                # 빗썸 평균 매수/매도 체결 가격 계산: total KRW 사이즈를 주문한 코인개수로 나눈 값
                bithumb_avg = bithumb_size / coin_transaction_amount
                # 업비트
                upbit_avg = upbit_size / coin_transaction_amount

                # 각 거래소별 코인개수 조정
                amount_upbit += coin_transaction_amount
                amount_bithumb -= coin_transaction_amount

                # 수수료 계산
                bithumb_fee = bithumb_avg * coin_transaction_amount * 0.04 / 100
                upbit_fee = upbit_avg * coin_transaction_amount * 0.05 / 100
                total_fee = bithumb_fee + upbit_fee

                # 이익금 계산
                profit = (bithumb_avg - upbit_avg) * coin_transaction_amount
                net_profit = profit - total_fee

                # 메세지 텔레그램 전송을 위한 process
                text0 = str(coin) + "빗썸 매도 실행 완료\n"
                text1 = "업비트 평균체결가격 : " + str(round(upbit_avg, 2)) + "\n"
                text2 = "빗썸 평균체결가격 : " + str(round(bithumb_avg, 2)) + "\n"
                text4 = "빗썸 매도이익(원) / 목표(원) : " + str(round((bithumb_avg-upbit_avg), 1)) + " / " + str(condition_bithumb_sell_value) + "\n"
                text5 = "순수익금(원) : " + str(round(net_profit, 1)) + "\n"
                text6 = "거래수량  : " + str(coin_transaction_amount) + "\n"
                text7 = "업비트 재주문횟수 : " + str(reorder_count) + "\n"
                text8 = "총수량 / 업비트 / 빗썸 : " + str(total_amount) + " / " + str(amount_upbit) + " / " + str(amount_bithumb) + "\n"
                text9 = "업비트 거래액 / 빗썸 거래액 : " + str(upbit_size) + " / " + str(bithumb_size)

                text = text0 + text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8

                print(text)

                # 업비트 빗썸 거래체결 결과 로드 확인 필요..
                asyncio.run(send_message(text))

                time.sleep(0.5)

            print("업비트 매도 1호가: ", upbit_best_buy_price)
            print("업비트 슬리피지 고려 매도물량(원): ", upbit_total_ask_value)
            print("업비트 매수 1호가: ", upbit_best_sell_price)
            print("업비트 슬리피지 고려 매수물량(원): ", upbit_total_bid_value)

            print("빗썸 매도 1호가: ", bithumb_best_buy_price)
            print("빗썸 슬리피지 고려 매도물량(원): ", bithumb_total_ask_value)
            print("빗썸 매수 1호가: ", bithumb_best_sell_price)
            print("빗썸 슬리피지 고려 매수물량(원): ", bithumb_total_bid_value)

            print("\n")
            print("업비트 매도시 이익(%): ", round(upbit_sell_case_percent,2))
            print("빗썸 매도시 이익(%): ", round(bithumb_sell_case_percent,2))

        except:
            if condition_continue:
                text1 = f"{coin}거래 에러발생 - 거래이상없음 계속\n수량체크 필요"
                err_msg = traceback.format_exc()
                text = text1 + err_msg
                asyncio.run(send_message(text))
                continue
            else:
                text1 = f"{coin}거래 에러발생 종료\n"
                err_msg = traceback.format_exc()
                text = text1 + err_msg
                asyncio.run(send_message(text))
                break
            


