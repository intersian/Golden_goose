import pybithumb

all = pybithumb.get_current_price("ALL")
for k, v in all.items():
    print(k, v)

for ticker, data in all.items() :
    print(ticker, data['closing_price'])