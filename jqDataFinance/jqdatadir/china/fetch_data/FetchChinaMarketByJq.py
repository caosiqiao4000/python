# encoding:utf-8
import datetime

import xlrd
from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip
from jqdatadir.china.common.jqDataLogin import login
from jqdatadir.china.common.handJqDataToFile import *
import logging as log

login()

no_check_value = ("399001.XSHE", "399006.XSHE", "800000.XHKG", '000016.XSHE', "000001.XSHG", "000905.XSHG", "000300.XSHG")


## 取得指定的股票的相应的聚宽价格年月日数据
def getDataByCode(stockCode, stockName, monthNumBar=800, numBar=100000):
    stockCodeMarket = stockCode;
    if len(stockCode) < 8:
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
    # print(stockCodeMarket,stockName)
    try:
        if stockCodeMarket not in no_check_value and df['market_cap'][0] < 50:
            # 取出总市值
            print(stockCodeMarket, stockName, " 总市值不到50亿 ", df['market_cap'][0])
            return
        # print(i, str(list).replace(".0", ""), list2 ,d_industry.get(stockCodeMarket).get("zjw"))
        getDataByCodeToFile(stockCodeMarket, stockName, path="D:\\\\ideaWorkspace\\python\\jqJson\\")
    except Exception as e:
        print("open exception: %s: %s\n" % (e, e))
        pass


def fetch_index_mult():
    '''
        https://www.joinquant.com/help/api/help?name=index#%E5%8E%86%E5%8F%B2%E8%A1%8C%E6%83%85%E6%95%B0%E6%8D%AE
     取得相应的指数
    '399980.XSHE': '中证超级大盘指数', 20190719 有个数据错误
    :return:
    '''


def start_fetch():
    # workbook = xlrd.open_workbook("..\\..\\..\\file\\20190522stock_base_info.xlsx")
    workbook = xlrd.open_workbook("..\\..\\..\\file\\stock_base_info20200503.xlsx")
    sheet_names = workbook.sheet_by_index(0)
    for i in range(1, 105):
        list = sheet_names.cell_value(i, 1);
        list2 = sheet_names.cell_value(i, 0);
        newStockCode = str(list).replace(".0", "")
        # print(newStockCode,list2)
        getDataByCode(newStockCode, list2)
    getDataByCode("000016.XSHE", "上证50")
    getDataByCode("510050.XSHE", "上证50ETF")
    getDataByCode("399001.XSHE", "深证指数")
    getDataByCode("399006.XSHE", "创业指数")
    getDataByCode("000001.XSHG", "上证指数")
    getDataByCode("000300.XSHG", "沪深300")
    getDataByCode("000905.XSHG", "中证500")

    getDataByCode("002032", "苏泊尔")
    getDataByCode("000333", "美的集团")
    getDataByCode("002304", "洋河股份")
    getDataByCode("603899", "晨光文具")
    getDataByCode("600276", "恒瑞医药")
    getDataByCode("300357", "我武生物")
    getDataByCode("601888", "中国国旅")
    getDataByCode("600036", "招商银行")
    getDataByCode("002714", "牧原股份")

    getDataByCode("000651", "格力电器")
    getDataByCode("300750", "宁德时代")
    getDataByCode("300676", "华大基因")
    getDataByCode("601988", "中国银行")

    


# print(get_all_securities(types=['index'], date=None))


# if __name__ == '__main__':
start_fetch()

# 输入
# print(normalize_code(['399001', '399006', '000001SZ', '000001.sz', '000001.XSHE']))
