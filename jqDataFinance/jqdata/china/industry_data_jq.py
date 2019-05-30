# encoding:utf-8
import datetime

from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip
from jqDataFinance.jqdata.china.common.jqDataLogin import login
from jqDataFinance.jqdata.china.common.handJqDataToFile import *
# from scrapy.spider import BaseSpider
# from jqdata import macro
import pandas as pd
import numpy as np

# 宏观数据     https://www.joinquant.com/help/api/help?name=macroData#%E6%95%B0%E6%8D%AE%E8%B0%83%E7%94%A8%E6%96%B9%E6%B3%95
# macro.run_query(query_object)
login()


# 查询分地区农林牧渔业总产值表(季度累计) 的前10条数据
# q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER
#           ).limit(10)
# df = macro.run_query(q)
# print(df)

# 查询2014年的分地区农林牧渔业总产值表(年度)
# q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR
#         ).filter(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.stat_year=='2014')
# df = macro.run_query(q)
# print(df)

def query_stock_main_pe():
    # 证券市场基本情况 MAC_STK_MARKET  货币供应量(月度)  MAC_MONEY_SUPPLY_MONTH
    dates = pd.date_range("1991", periods=30, freq="y")
    # print(dates)
    for date_one in dates.values:
        date_two = str(date_one)[:4]
        # print(date_two)
        q = query(macro.MAC_STK_MARKET
                  ).filter(macro.MAC_STK_MARKET.stat_year == date_two)
        df = macro.run_query(q)
        # print(df.index,df.columns)
        # xshe_avg_pe	深圳平均市盈率
        print(df.loc[:,['stat_year','xshg_avg_pe','xshe_avg_pe']])

#  宏观经济景气预警指数 MAC_BOOM_WARNING_IDX     MAC_MONEY_SUPPLY_MONTH
def query_money_total_month():
    dates = pd.date_range("1991", periods=350, freq="m")#350
    # print(dates)
    list1 = []
    # list2 = []
    for date_one in dates.values:
        date_two = str(date_one)[:7]
        # print(date_two)
        q = query(macro.MAC_MONEY_SUPPLY_MONTH
                  ).filter(macro.MAC_MONEY_SUPPLY_MONTH.stat_month == date_two)
        df = macro.run_query(q)
        list1.append(df.loc[:, ['stat_month', 'm2_yoy', 'm1_yoy', 'm0_yoy']].values)
        # print(df.loc[:,['stat_month','m2_yoy','m1_yoy','m0_yoy']].values)
        # ============================================================================
        # q2 = query(macro.MAC_BOOM_WARNING_IDX
        #           ).filter(macro.MAC_BOOM_WARNING_IDX.stat_month == date_two)
        # df2 = macro.run_query(q2)
        # # print(df2)
        # list2.append(df2.loc[:,['stat_month', 'm2_sgn', 'cpi_sgn', 'loan_sgn','warning_idx']].values)
    print(list1)


query_money_total_month()
# query_stock_main_pe()