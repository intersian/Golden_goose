import pandas as pd
import requests
url = "https://finance.naver.com/item/sise_day.nhn?code=066570"
df = pd.read_html(requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text)
print(df[0].dropna(axis=0))