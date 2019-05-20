import requests
from pyquery import PyQuery as pq
import json
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

# url1 = "https://query1.finance.yahoo.com/v7/finance/download/BABA?period1=1266854400&period2=1550851200&interval=1d&events=history&crumb=Id1CX7v87Kp"
url1 = "https://finance.yahoo.com/quote/BABA/history?period1=1266854400&period2=1550851200&interval=1d&filter=history&frequency=1d&guccounter=1"

html = urlopen(url1).read()
soup = BeautifulSoup(html,"html.parser")
titles = soup.select("body  script") # CSS 选择器
i = 1
for title in titles:
    if i == 3:
        print(title.get_text())# 标签体、标签属性
        str=title.get_text()
        break
    if i == 2:
        i = 3
    if i == 1:
        i = 2
for aa,x in enumerate([1,2,3,4,5]):
    print(aa,x)



# htmlText = requests.get(url1).text
#
# # print(htmlText)
# p = pq(htmlText)
# # p('HistoricalPriceStore').html()  # 返回<title>hello</title>
# datastr1 = p('script').text().find('HistoricalPriceStore')
# print(datastr1)
# json1 = json.dumps(datastr1)
# print(json1)  # 返回hello
