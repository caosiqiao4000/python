# encoding:utf-8
from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip
import datetime
import csv
from jqdata.china.common.jqDataLogin import login
from jqdata.china.common.handJqDataToFile import *

login()


# auth('18680538805', 'zzzz00000000')  # 依次输入账号、密码，链接到平台数据库

def readCsv():
    csv_file = csv.reader(open(r'C:\Users\Administrator\Desktop\聚宽期货合约代码表201905.csv', "r", encoding="utf-8"))
    # // print(csv_file)
    for stu in csv_file:
        if len(stu) > 0:
            aa_stu = str(stu[0])
            bb_stu = aa_stu.split("\t")
            # print(len(bb_stu),bb_stu)
            if bb_stu[0].__contains__("合约"):
                # print(len(bb_stu), bb_stu)
                # test2(bb_stu[1])
                getDataByCodeToFile(bb_stu[1], bb_stu[0], path=r'D:\\\\ideaWorkspace\\python\\jqJson\\')


dayNumBar = 100000


def test1():
    # 抓取期货数据  郑商所XZCE AP 苹果  大商所XDCE A豆一 C 玉米 玉米淀粉合约	CS
    # 上期所 白银合约	AG9999.XSGE
    dictFuturn = {"AP": "苹果合约", "A": "豆一合约","B": "豆二合约", "AG": "白银合约", "C": "玉米合约"}

    for key in dictFuturn:
        # 获取某一天的主力合约对应的期货合约代码，指定日期为'2018-05-06'
        mainFuturnBySiglin = get_dominant_future(key)
        datenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        print("主力合约 " + mainFuturnBySiglin + " - " + dictFuturn.get(key) + " ------------ " + datenow)
        # df = get_bars(mainFuturnBySiglin, dayNumBar, unit='1d',
        #               fields=['date', 'open', 'high', 'low', 'close'],
        #               include_now=False, fq_ref_date=datenow,
        #               end_dt=datenow)
        # print(df.head(2))
        # print(df.tail(2))

        # https://www.joinquant.com/help/api/help?name=JQData#
        # get_dominant_future-%E8%8E%B7%E5%8F%96%E4%B8%BB%E5%8A%9B%E5%90%88%E7%BA%A6%E5%AF%B9%E5%BA%94%E7%9A%84%E6%A0%87%E7%9A%84
        # 获取期货可交易合约列表
        mainFuturnByList = get_future_contracts(key)
        print("可交易合约列表 ", mainFuturnByList)


def test2(futurn,):
    datenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
    df0 = get_bars(futurn, dayNumBar, unit='1d',
                   fields=['date', 'open', 'high', 'low', 'close'],
                   include_now=False, fq_ref_date=datenow,
                   end_dt=datenow)
    print(df0.head(2))
    print(df0.tail(2))
    print(df0.size)

def addOne(futurnCode,futurnName):
    getDataByCodeToFile(futurnCode, futurnName, path=r'D:\\\\ideaWorkspace\\python\\jqJson\\')

readCsv()
# test1()
# addOne("B1907.XDCE","豆二合约")
# test2("C9999.XDCE")
# test2("C8888.XDCE")
# test2("AP9999.XZCE")
# test2("AP8888.XZCE")
