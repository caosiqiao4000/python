# encoding:utf-8
import datetime

import xlrd
from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip
from jqdata.china.common.jqDataLogin import login
from jqdata.china.common.handJqDataToFile import *
import logging as log

login()

no_check_value = ("399001.XSHE", "399006.XSHE", "800000.XHKG",'000016.XSHE')


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
        if stockCodeMarket not in no_check_value and df['market_cap'][0] < 120:
            # 取出总市值
            print(stockCodeMarket, stockName, " 总市值不到120亿 ", df['market_cap'][0])
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
    000819.XSHG	有色金属
    000300.XSHG	沪深300
    :return:
    '''
    stock_index_tuple = ("000001.XSHG", '000819.XSHG', '000300.XSHG')
    stock_index_tuple_name = ("上证指数", '有色金属', '沪深300')
    for index, code in enumerate(stock_index_tuple):
        getIndexDataByCodeToFile(code, stock_index_tuple_name[index], path="D:\\\\ideaWorkspace\\python\\jqJson\\")
    pass


def start_fetch():
    # workbook = xlrd.open_workbook("C:\\\\Users\\Administrator\\Desktop\\20190507stock_base_info.xlsx")
    workbook = xlrd.open_workbook("..\\..\\..\\file\\20190522stock_base_info.xlsx")
    sheet_names = workbook.sheet_by_index(0)
    # for i in range(1, 35):
    # for i in range(1, 35):
    #     list = sheet_names.cell_value(i, 1);
    #     list2 = sheet_names.cell_value(i, 0);
    #     newStockCode = str(list).replace(".0", "")
    #     getDataByCode(newStockCode, list2)
    # getDataByCode("002415.XSHE", "海康威视")
    getDataByCode("000016.XSHE", "上证50")
    # getDataByCode("399001.XSHE", "深证指数")
    # getDataByCode("399006.XSHE", "创业指数")
    # fetch_index_mult()


# print(get_all_securities(types=['index'], date=None))


# if __name__ == '__main__':
start_fetch()

# 输入
# print(normalize_code(['399001', '399006', '000001SZ', '000001.sz', '000001.XSHE']))
