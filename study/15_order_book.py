import datetime
import pybithumb

orderbook = pybithumb.get_orderbook("BTC")
print(orderbook)

for k in orderbook:
    print(k)

print(orderbook['payment_currency'])
print(orderbook['order_currency'])
ms = int(orderbook['timestamp'])

dt = datetime.datetime.fromtimestamp(ms/1000)
print(dt)

bids = orderbook['bids']
asks = orderbook['asks']
print(bids)
print(asks)

for bid in bids:
    price = bid['price']
    quant = bid['quantity']
    print("매수호가: ", price, "매수잔량: ", quant)