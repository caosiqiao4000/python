# encoding:utf-8
import datetime

from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip

# my_path = "C:\\Program Files\\apache-tomcat-7.0.75\\apache-tomcat-7.0.75\\webapps\\ROOT\\json\\"
my_path = "D:\\ideaWorkspace\\python\\jqJson"
field_params = ['date', 'open', 'high', 'low', 'close', 'volume']
field_params_index = ['open', 'high', 'low', 'close', 'volume']
datenow = datetime.datetime.now().strftime('%Y-%m-%d');
# 获取366天前的日期
date_hour_start = (datetime.date.today() - datetime.timedelta(days=566)).strftime('%Y-%m-%d')
start_date_str = "2005-01-01"


def getDataByCodeToFile(stockCodeMarket, stockName, monthNumBar=800, numBar=100000,
                        path=my_path):

    df = get_bars(stockCodeMarket, numBar, unit='1d', fields=field_params,
                  include_now=True, fq_ref_date=datenow,
                  end_dt=datenow)
    if df.size < 700:
        print(stockCodeMarket, stockName, "数量少于 700", df.size)
        return
    print(stockCodeMarket + " - " + stockName + " ------------ " + datenow)
    # df_zero_day = df[df.volume == 0]
    # if len(df_zero_day) > 10 and len(df_zero_day) / df.size * 1.0 > 0.05:
    #     print(stockName, stockCodeMarket, "xxxxxxxxxxxxxxxxx---- 超过10天有无效值---------------\n")
    #     return
    # print(df.head(1))
    # print(df.tail(1))
    datenow_new = datetime.datetime.strptime(datenow, '%Y-%m-%d')
    date_jq = datetime.datetime.strptime(str(df.tail(1)["date"].iloc[0]), '%Y-%m-%d')
    # date_jq = df.tail(1)["date"].iloc[0]
    delta = datenow_new - date_jq
    if delta.days > 40:
        print(stockName, stockCodeMarket, " ----------------40已经没交易,可能已经停止交易 ")
        return
    df.loc[:, "trend"] = df.loc[:, 'close'] - df.loc[:, 'open']  # 用来判断一天上涨还是下跌
    df.to_csv(
        path + stockCodeMarket + "_" + stockName + "day.csv")
    # -----------------------------------------------------------------------
    # df0 = get_bars(stockCodeMarket, 15000, unit='60m', fields=field_params,
    #                include_now=True, fq_ref_date=datenow,
    #                end_dt=datenow)
    # print(df0[0:1])
    # print(df0.tail(1))
    # df0.loc[:, "trend"] = df0.loc[:, 'close'] - df0.loc[:, 'open']  # 用来判断一天上涨还是下跌
    # df0.to_csv(
    #     path + stockCodeMarket + "_" + stockName + "hour.csv")
    # ---------------------------------------------------------------------------------
    df1 = get_bars(stockCodeMarket, numBar, unit='1w', fields=field_params,
                   include_now=True, fq_ref_date=datenow,
                   end_dt=datenow)
    print(df1[0:1])
    print(df1.tail(1))
    df1.loc[:, "trend"] = df1.loc[:, 'close'] - df1.loc[:, 'open']  # 用来判断一天上涨还是下跌
    df1.to_csv(
        path + stockCodeMarket + "_" + stockName + "week.csv")
    # -------------------------------------------------------------------------------------
    df2 = get_bars(stockCodeMarket, monthNumBar, unit='1M', fields=field_params,
                   include_now=True, fq_ref_date=datenow,
                   end_dt=datenow)
    print(df2.head(1))
    print(df2.tail(1))
    df2.loc[:, "trend"] = df2.loc[:, 'close'] - df2.loc[:, 'open']  # 用来判断一天上涨还是下跌
    df2.to_csv(
        path + stockCodeMarket + "_" + stockName + "month.csv")


def getIndexDataByCodeToFile(stockCodeMarket, stockName, path=my_path):
    # panel = get_price(['000001.XSHG', '000819.XSHG', '000300.XSHG'], start_date=startdate_str, end_date=datenow,
    #     #                   frequency='5d', fields=['open', 'close'],
    #     #                   skip_paused=True, fq='pre')
    #     # print(panel)

    ##  daily
    df0 = get_price(stockCodeMarket, start_date=start_date_str, end_date=datenow,
                    frequency='1d', fields=field_params_index,
                    skip_paused=True, fq='pre')
    df0.insert(0, 'date', df0.index)
    print(df0.head(1))
    print(df0.tail(1))
    # print(df0.columns)
    df0.loc[:, "trend"] = df0.loc[:, 'close'] - df0.loc[:, 'open']  # 用来判断一天上涨还是下跌
    df0.to_csv(
        path + stockCodeMarket + "_" + stockName + "day.csv")
    # ---------------------------------------------------------------------------hour
    df1 = get_price(stockCodeMarket, start_date=date_hour_start, end_date=datenow,
                    frequency='60m', fields=field_params_index,
                    skip_paused=True, fq='pre')
    df1.insert(0, 'date', df1.index)
    print(df1.head(1))
    print(df1.tail(1))
    df1.loc[:, "trend"] = df1.loc[:, 'close'] - df1.loc[:, 'open']  # 用来判断一天上涨还是下跌
    df1.to_csv(
        path + stockCodeMarket + "_" + stockName + "hour.csv")
    # ---------------------------------------------------------------------------week
    df2 = get_price(stockCodeMarket, start_date=start_date_str, end_date=datenow,
                    frequency='5d', fields=field_params_index,
                    skip_paused=True, fq='pre')
    df2.insert(0, 'date', df2.index)
    print(df2.head(2))
    print(df2.tail(2))
    df2.loc[:, "trend"] = df2.loc[:, 'close'] - df2.loc[:, 'open']  # 用来判断一天上涨还是下跌
    df2.to_csv(
        path + stockCodeMarket + "_" + stockName + "week.csv")
    # ---------------------------------------------------------------------------week
    df2 = get_price(stockCodeMarket, start_date=start_date_str, end_date=datenow,
                    frequency='22d', fields=field_params_index,
                    skip_paused=True, fq='pre')
    df2.insert(0, 'date', df2.index)
    print(df2.head(2))
    print(df2.tail(2))
    df2.loc[:, "trend"] = df2.loc[:, 'close'] - df2.loc[:, 'open']  # 用来判断一天上涨还是下跌
    df2.to_csv(
        path + stockCodeMarket + "_" + stockName + "month.csv")
    pass
