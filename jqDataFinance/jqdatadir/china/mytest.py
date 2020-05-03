import requests
from pyquery import PyQuery as pq
import json
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.display.max_rows = 31

def testOne():
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


def testTwo():
    url1 = "https://finance.yahoo.com/quote/BABA/history?period1=1266854400&period2=1550851200&interval=1d&filter=history&frequency=1d&guccounter=1"
    htmlText = requests.get(url1).text

    # print(htmlText)
    p = pq(htmlText)
    # p('HistoricalPriceStore').html()  # 返回<title>hello</title>
    datastr1 = p('script').text().find('HistoricalPriceStore')
    print(datastr1)
    json1 = json.dumps(datastr1)
    print(json1)  # 返回hello

def testThree():
    # s = pd.Series([1,3,5,np.nan,6,8])
    # print(s)
    dates = pd.date_range("20190501",periods=6,freq="m")
    # print(dates)
    df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list("ABCD"))
    # print(df)
    # print(list(range(4)))
    # print(np.array([3]*4))
    # print(pd.Categorical(["test","train","test","train"]))
    # df2 = pd.DataFrame({"A":1.,
    #                     "B":pd.Timestamp("20130102"),
    #                     "C":pd.Series(2,index=list(range(4)),dtype='float32'),
    #                     "D":np.array([3]*4,dtype='int32'),
    #                     "E":pd.Categorical(["test","train","test","train"]),
    #                     "F":'foo'})
    # print(df2)
    # print(df.tail())
    # print(df.index)
    # print(df.columns)
    # print(df.values)
    # print(df.describe())
    # print(df.T)
    # print(df['A'])
    # print(df[0:3])
    # print(df.loc[dates[0]])
    # print(df.loc[:,['A','B']])
    s1 = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range('20130102', periods=6))
    print(s1)
    df['F'] = s1
    df.at[dates[0],'A'] = 0
    df.iat[0,1] = 0
    df.loc[:,'D'] = np.array([5]*len(df))
    print(df)
    df2 = df.copy()
    df2[df2>0] = -df2
    print(df2)

def test_four():
    my_orders_list = ('豆一',"")
    key = '豆一'
    print(key in my_orders_list)
    for name in my_orders_list:
        print(name)
    pass

test_four()
