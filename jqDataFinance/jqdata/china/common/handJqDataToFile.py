# encoding:utf-8
import datetime

from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip

# my_path = "C:\\Program Files\\apache-tomcat-7.0.75\\apache-tomcat-7.0.75\\webapps\\ROOT\\json\\"
my_path = "D:\\ideaWorkspace\\python\\jqJson"
field_params = ['date', 'open', 'high', 'low', 'close', 'volume']


def getDataByCodeToFile(stockCodeMarket, stockName, monthNumBar=800, numBar=100000,
                        path=my_path):
    datenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
    df = get_bars(stockCodeMarket, numBar, unit='1d', fields=field_params,
                  include_now=False, fq_ref_date=datenow,
                  end_dt=datenow)
    if df.size < 1700:
        print(stockCodeMarket, stockName, "数量少于 1700", df.size)
        return
    print(stockCodeMarket + " - " + stockName + " ------------ " + datenow)
    print(df.head(2))
    print(df.tail(2))
    df.to_csv(
        path + stockCodeMarket + "_" + stockName + "day.csv")

    df1 = get_bars(stockCodeMarket, numBar, unit='1w', fields=field_params,
                   include_now=False, fq_ref_date=datenow,
                   end_dt=datenow)
    print(df1[0:2])
    print(df1.tail(2))
    df1.to_csv(
        path + stockCodeMarket + "_" + stockName + "week.csv")

    df2 = get_bars(stockCodeMarket, monthNumBar, unit='1M', fields=field_params,
                   include_now=False, fq_ref_date=datenow,
                   end_dt=datenow)
    print(df2.head(2))
    print(df2.tail(2))
    df2.to_csv(
        path + stockCodeMarket + "_" + stockName + "month.csv")


def get_day_data_by_code_to_file(stockCodeMarket, stockName, monthNumBar=800, numBar=100000,
                                 path=my_path):
    datenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
    df = get_bars(stockCodeMarket, monthNumBar, unit='1d', fields=field_params,
                  include_now=False, fq_ref_date=datenow,
                  end_dt=datenow)
    if df.size < 1700:
        print(stockCodeMarket, stockName, "数量少于 1700", df.size)
        return
    print(stockCodeMarket + " - " + stockName + " ------------ " + datenow)
    print(df.head(2))
    print(df.tail(2))
    df.to_csv(
        path + stockCodeMarket + "_" + stockName + "&day.csv")

    df1 = get_bars(stockCodeMarket, numBar / 4, unit='60m', fields=field_params,
                   include_now=False, fq_ref_date=datenow, end_dt=datenow)
    print(df1[0:2])
    print(df1.tail(2))
    df1.to_csv(
        path + stockCodeMarket + "_" + stockName + "&hour.csv")

    df2 = get_bars(stockCodeMarket, numBar, unit='15m', fields=field_params,
                   include_now=False, fq_ref_date=datenow, end_dt=datenow)
    print(df2.head(2))
    print(df2.tail(2))
    df2.to_csv(
        path + stockCodeMarket + "_" + stockName + "&fiveteen.csv")
