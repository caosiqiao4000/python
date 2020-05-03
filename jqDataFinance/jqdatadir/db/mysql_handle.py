#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 给本地数据库删除一些不要的数据和给股票查询出相应的行业代码
import pymysql
import datetime
from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip
# from jqDataFinance.jqdata.china.common.jqDataLogin import login
from jqdatadir.china.common.jqDataLogin import login

login()
datenow = datetime.datetime.now().strftime('%Y-%m-%d');

# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "cfpdb")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


# 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()

def updata_mysql(stockIndustryCode, stockCode,stockName):
    # SQL 更新语句
    sql = "UPDATE stock_base_info SET stock_industry = '%s' WHERE stock_code = '%s'" % (
        stockIndustryCode, stockCode)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # print("更新 %s 行业为 %s"%(stockName,stockIndustryCode))
    except:
        # 发生错误时回滚
        db.rollback()


def del_item_mysql(stockCode):
    # SQL 删除语句
    sql = "DELETE FROM stock_base_info WHERE stock_code = %s" % (stockCode)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        return True
    except:
        # 发生错误时回滚
        db.rollback()
        return False


# print("Database version : %s " % data)
def handle_jqdata(stockCode, stockName):
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
    try:
        if df['market_cap'][0] < 120:
            # 取出总市值
            print(stockCodeMarket, stockName, " 总市值 ", df['market_cap'][0])
            return False, stockName
        # 获取贵州茅台("600519.XSHG")的所属行业数据
        d_industry = get_industry(stockCodeMarket, datenow)
        d_industry = str(d_industry);
        if (d_industry.__contains__("保险") | d_industry.__contains__("理财")):
            print(d_industry)
            return True, "C070202"
        elif (d_industry.__contains__("银行")):
            print(d_industry)
            return True, "C070101"
        elif (d_industry.__contains__("证券")):
            print(d_industry)
            return True, "C070201"
        else:
            return True, "C000000"
    except:
        return True, "error"

def start_jq_fetch():
    # SQL 查询语句
    sql = "SELECT stock_name,stock_code,total_grade FROM stock_base_info"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print(results.__len__())

        for row in results:
            stock_code = row[1]
            stock_name = row[0]
            isBigValue, industryCode = handle_jqdata(stock_code, stock_name)
            if (str(industryCode) == "error"):
                continue
            if (isBigValue):
                updata_mysql(industryCode, stock_code, stock_name)
            else:
                if (del_item_mysql(stock_code)):
                    print("删除 %s %s" % (stock_code, stock_name))
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()

start_jq_fetch()
# stock_code ="601318"
# stock_name="中国平安"
# handle_jqdata(stock_code,stock_name)
# isBigValue, industryCode = handle_jqdata(stock_code, stock_name)
# if (isBigValue):
#     updata_mysql(industryCode, stock_code, stock_name)
# else:
#     if (del_item_mysql(stock_code)):
#         print("删除 %s %s" % (stock_code, stock_name))