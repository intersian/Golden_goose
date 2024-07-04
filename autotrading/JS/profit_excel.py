import pandas as pd
from datetime import datetime


df = pd.read_excel('profit.xlsx')
print(df)
# df.loc[0, 'a'] = 'f'
# print(df)
# df.to_excel('profit.xlsx')

# now = datetime.now()
# print("현재 : ", now)
# print("문자열 변환 : ", now.strftime('%Y-%m-%d %H:%M:%S'))