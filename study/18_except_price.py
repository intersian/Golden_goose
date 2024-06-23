import pybithumb
import time

while True:
    price = pybithumb.get_current_price("BTC")
    # if price is not None:
    #     print(price/10)
    try:
        print(price/10)
    except:
        print("에러 발생", price)
    time.sleep(0.2)