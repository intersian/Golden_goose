import pybithumb

con_key = "09899240e4999f7972860affceb43e23"
sec_key = "7cac9287114a6b643572b3dc9750391b"

bithumb = pybithumb.Bithumb(con_key, sec_key)

# order = bithumb.buy_limit_order("BTC", 96040000, 0.001)
# print(order)


balance = bithumb.get_balance("BTC")
print(balance)
krw = bithumb.get_balance("BTC")[2]
orderbook = pybithumb.get_orderbook("BTC")

asks = orderbook['asks']
sell_price = asks[0]['price']
unit = krw/sell_price
print(unit)

# order = bithumb.sell_limit_order("BTC", 100000000, 1)
# print(order)

# time.sleep(10)
# cancel = bithumb.cancel_order(order)
# print(cancel)
