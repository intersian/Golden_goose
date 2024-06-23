import pybithumb
import time

con_key = "09899240e4999f7972860affceb43e23"
sec_key = "7cac9287114a6b643572b3dc9750391b"

bithumb = pybithumb.Bithumb(con_key, sec_key)

balance = bithumb.get_balance("BTC")
print(balance)
print(format(balance[0], 'f'))

for ticker in pybithumb.get_tickers():
    balance = bithumb.get_balance(ticker)
    print(ticker, ":", balance)
    time.sleep(0.1)