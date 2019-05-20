# encoding:utf-8
from jqdatasdk import *#平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip
import numpy as np
import pandas as pd
import csv
auth('18680538805','zzzz00000000')#依次输入账号、密码，链接到平台数据库

# 市场整体数据获取
#get_all_securities(types='stock',date)
#types，为列表，可以为stock/fund/index/futures/etf/lof/fja(分级A)/fjb,为空时返回所有股票不含基金指数期货；date日期表获取这一日期还在上市的股票默认None表获取所有日期股票
#上海证券交易所     .XSHG     ‘600519.XSHG’     贵州茅台
#深圳证券交易所     .XSHE     ‘000001.XSHE’     平安银行
#中金所     .CCFX     ‘IC9999.CCFX’     中证500主力合约
#大商所     .XDCE     ‘A9999.XDCE’     豆一主力合约
#上期所     .XSGE     ‘AU9999.XSGE’     黄金主力合约
#郑商所     .XZCE     ‘CY8888.XZCE’     棉纱期货指数
#上海国际能源期货交易所     .XINE     ‘SC9999.XINE’     原油主力合约
index = get_all_securities(types='index')
stock = get_all_securities()
df = get_all_securities(['fund'])
get_all_securities(date='2015-10-24')[:5]

#查询当日剩余可调用数据条数
count=get_query_count()
##print(count)

#print(stock)
#print(stock[:2])
len(stock)
type(stock)

#获取贵州茅台按天为周期以"2018-12-05"为基础往前10个交易日的数据
#df = get_bars('600519.XSHG', 1000, unit='1M',fields=['date','open','high','low','close'],include_now=False,end_dt='2018-12-05')
#print(df)

with open('C:\\Program Files\\apache-tomcat-7.0.75\\apache-tomcat-7.0.75\\webapps\\ROOT\\json\\data.json', 'r', encoding='utf-8') as f:
    print(f.read())