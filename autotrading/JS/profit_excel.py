import pandas as pd
import csv
from datetime import datetime


# now = datetime.now()
# df = pd.DataFrame([], columns = ['시간'])
# df['매수가'] = []
# df['매도가'] = []
# df['수량'] = []
# df['손익'] = []
# df['비고'] = []
# df.to_csv("profit.csv", index = False)

f = open('profit.csv', encoding='UTF-8')

rdr = csv.reader(f)

for line in rdr:
    print(line)
f.close()


# f = open('profit.csv','a', newline='', encoding='UTF-8')
# wr = csv.writer(f)
# wr.writerow([now.strftime('%Y-%m-%d %H:%M:%S'), 1400, 1410, 700, 500, '업빗매도-빗썸매수'])
# f.close()

# print("문자열 변환 : ", now.strftime('%Y-%m-%d %H:%M:%S'))