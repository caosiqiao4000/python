# encoding:utf-8

#%%

import pandas as pd
from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip
from jqdatadir.china.common.jqDataLogin import login
from jqdatadir.china.common.handJqDataToFile import *
import logging as log

login()

def get_stock_name(stock_code):
    stocks_df = get_all_securities()
    stock_name = [stocks_df.loc[c, 'display_name'] for c in stock_code]
    return stock_name

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)

print("2e10",2e1)
print("1e10",1e10)

"""
股票上市信息
https://www.joinquant.com/help/api/help?name=Stock#%E8%82%A1%E7%A5%A8%E4%B8%8A%E5%B8%82%E4%BF%A1%E6%81%AF
"""
init_filter_query = query(
                            valuation.pe_ratio, indicator.code, indicator.inc_return, indicator.roa,
                        ).filter(
                            valuation.inc_revenue_year_on_year > 25,
                        ).order_by(
                            indicator.inc_return.desc()
                        ).limit(
                            100
                        )


df = get_fundamentals(init_filter_query, statDate='2020q1')
stocks = df['code']

multi_stock_data_query = query(
                                valuation.pe_ratio, indicator.code, indicator.inc_return, indicator.total_liability,indicator.total_sheet_owner_equities
                            ).filter(
                                indicator.code.in_(stocks)
                            )

roe_dict = {}
roa_dict = {}
year_list = ['2015', '2016', '2017', '2018', '2019']
for year in year_list:
    df = get_fundamentals(multi_stock_data_query, statDate=year)
    df = df.set_index('code')
    roe_dict[year] = df['roe']
    roa_dict[year] = df['roa']

roe_df = pd.DataFrame(roe_dict)
roe_df.index = get_stock_name(roe_df.index)
print(roe_df)

roa_df = pd.DataFrame(roa_dict)
roa_df.index = get_stock_name(roa_df.index)
print(roa_df)



#%%

import pandas as pd
from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip
from jqdatadir.china.common.jqDataLogin import login
from jqdatadir.china.common.handJqDataToFile import *
import logging as log

login()

# 指定查询对象为恒瑞医药（600276.XSHG)的上市信息，限定返回条数为10
q=query(finance.STK_LIST).filter(finance.STK_LIST.code=='600276.XSHG').limit(10)
df=finance.run_query(q)
print(df)

#q=finance.run_query(query(finance.STK_LIST).filter(finance.STK_LIST.start_date>=“2018-01-01”)
#df=finance.run_query(q)
#print(df)
