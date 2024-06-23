import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/item/main.nhn?code=005930"
html = requests.get(url).text

soup = BeautifulSoup(html, "html5lib")
tags = soup.select("#tab_con1 > div:nth-child(6) > table > tbody > tr.strong > td > em")
tag = tags[0]
print(tag.text)