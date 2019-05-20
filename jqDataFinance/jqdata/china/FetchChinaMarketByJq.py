# encoding:utf-8
import datetime

from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip
from jqdata.china.common.jqDataLogin import login
from jqdata.china.common.handJqDataToFile import *
# from scrapy.spider import BaseSpider


login()

# datenow = datetime.datetime.now().strftime('%Y-%m-%d');
# 获取贵州茅台按天为周期以"2018-12-05"为基础往前10个交易日的数据
def getDataByCode(stockCode, stockName,monthNumBar = 800,numBar=100000):
    stockCodeMarket = stockCode;
    if stockCode.endswith("6", 0, 1):
        stockCodeMarket += '.XSHG'  # 深圳证券交易所     .XSHE
    else:
        stockCodeMarket += '.XSHE'  #
    ### 获取单只股票在某一日期的市值数据
    df = get_fundamentals(query(
        valuation
    ).filter(
        valuation.code == stockCodeMarket
    ))
    # 获取贵州茅台("600519.XSHG")的所属行业数据
    # d_industry = get_industry(stockCodeMarket,datenow)
    if df['market_cap'][0]<120:
        # 取出总市值
        print(stockCodeMarket,stockName, " 总市值 ", df['market_cap'][0])
        return
    # print(i, str(list).replace(".0", ""), list2 ,d_industry.get(stockCodeMarket).get("zjw"))
    getDataByCodeToFile(stockCodeMarket,stockName,path="D:\\\\ideaWorkspace\\python\\jqJson\\")

# workbook = xlrd.open_workbook("C:\\\\Users\\Administrator\\Desktop\\20190507stock_base_info.xlsx")
workbook = xlrd.open_workbook("C:\\\\Users\\Administrator\\Desktop\\20190507stock_base_info.xlsx")
sheet_names = workbook.sheet_by_index(0)
for i in range(1, 52):
    list = sheet_names.cell_value(i, 1);
    list2 = sheet_names.cell_value(i, 0);
    newStockCode = str(list).replace(".0", "")
    getDataByCode(newStockCode, list2)

