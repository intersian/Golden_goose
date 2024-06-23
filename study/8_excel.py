import pandas as pd
df = pd.read_excel("C:\\ohlc.xlsx")
print(df)

df.to_excel("C:\\ohlc_2.xlsx")

df = df.set_index('date')
print(df)