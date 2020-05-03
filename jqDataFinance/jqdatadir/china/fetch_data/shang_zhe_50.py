# encoding:utf-8
import datetime

from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip
from jqDataFinance.jqdata.china.common.jqDataLogin import login
# from scrapy.spider import BaseSpider


login()

def find_all_index():
    #获取所有标的信息 types: list: 用来过滤securities的类型, list元素可选: 'stock', 'fund', 'index', 'futures', 'etf', 'lof', 'fja', 'fjb'。types为空时返回所有股票, 不包括基金,指数和期货
    # df =  get_all_securities(['etf'])
    df =  get_all_securities(['index'])
    ##          000016.XSHG              上证50    SZ50 2004-01-02 2200-01-01  index
    # print(df)
    ##获取单个标的信息
    # df =  get_security_info('000016.XSHG')
    ##get_index_stocks - 获取指数成份股
    # df = get_index_stocks('000016.XSHG')
    # print(df)
    for name in df.values:
        if str(name).__contains__("上证50"):
            print(name)

#['上证50' 'SZ50' Timestamp('2018-01-15 00:00:00') Timestamp('2200-01-01 00:00:00') 'etf']
def query_index_info():
    # 查询("10001313.XSHG ")最新的期权基本资料数据。 10001313.XSHG
    q = query(opt.OPT_CONTRACT_INFO).filter(opt.OPT_CONTRACT_INFO.code == 'SZ50')
    # q = query(opt.OPT_CONTRACT_INFO).filter(opt.OPT_CONTRACT_INFO.code == '000016.XSHG')
    df = opt.run_query(q)
    print(df.head(5))

find_all_index()
# query_index_info()