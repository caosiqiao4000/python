# encoding:utf-8
from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip
import csv
from jqdata.china.common.jqDataLogin import login
from jqdata.china.common.handJqDataToFile import *

login()

json_path = r'D:\\\\ideaWorkspace\\python\\jqJson\\'

# auth('18680538805', 'zzzz00000000')  # 依次输入账号、密码，链接到平台数据库
'''
动力煤是郑交所品种。原先交易单位200吨每手;简称动煤,代码“TC"。从1605合约开始改为每手100吨。简称郑煤,代码“ZC"
修改合约交易代码 本次合约修改将强麦合约交易代码一并修改, 强麦合约交易 代码由 WS 改为 WH(QM 合约自动废止), 为其英文 WHEAT 的前两个 字母
甲醇标准合约内容将会进行更改：
由现在的50吨/手，降低到10吨/手。代码由ME改为MA，甲醇新合约规则从1506合约开始使用。及1506以前的合约都是me，50吨/手；1506及以后的都是MA，10吨/手
'''


def readCsv():
    csv_file = csv.reader(open(r'..\..\..\file\聚宽期货合约代码表201905.csv', "r", encoding="utf-8"))
    # // print(csv_file)
    tuple_no_exist = ("WS9999.XZCE", "TC9999.XZCE", "WT9999.XZCE", "RO9999.XZCE", "GN9999.XZCE","ER9999.XZCE","ME9999.XZCE")
    # tuple_no_exist
    for stu in csv_file:
        if len(stu) > 0:
            aa_stu = str(stu[0])
            bb_stu = aa_stu.split("\t")
            # print(len(bb_stu),bb_stu)
            if bb_stu[0].__contains__("合约"):
                if bb_stu[2] in tuple_no_exist:
                    continue
                # print(len(bb_stu), bb_stu)
                # test2(bb_stu[1])
                getDataByCodeToFile(bb_stu[2], bb_stu[0], path=json_path)

# def test1():
#     # 抓取期货数据  郑商所XZCE AP 苹果  大商所XDCE A豆一 C 玉米 玉米淀粉合约	CS
#     # 上期所 白银合约	AG9999.XSGE
#     dictFuturn = {"AP": "苹果合约", "A": "豆一合约", "B": "豆二合约", "AG": "白银合约", "C": "玉米合约"}
#
#     for key in dictFuturn:
#         # 获取某一天的主力合约对应的期货合约代码，指定日期为'2018-05-06'
#         mainFuturnBySiglin = get_dominant_future(key)
#         datenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
#         print("主力合约 " + mainFuturnBySiglin + " - " + dictFuturn.get(key) + " ------------ " + datenow)
#         # df = get_bars(mainFuturnBySiglin, dayNumBar, unit='1d',
#         #               fields=['date', 'open', 'high', 'low', 'close'],
#         #               include_now=False, fq_ref_date=datenow,
#         #               end_dt=datenow)
#         # print(df.head(2))
#         # print(df.tail(2))
#
#         # https://www.joinquant.com/help/api/help?name=JQData#
#         # get_dominant_future-%E8%8E%B7%E5%8F%96%E4%B8%BB%E5%8A%9B%E5%90%88%E7%BA%A6%E5%AF%B9%E5%BA%94%E7%9A%84%E6%A0%87%E7%9A%84
#         # 获取期货可交易合约列表

# def activeFuturn_query(futurnName):
#     mainFuturnByList = get_future_contracts(futurnName)
#     print("可交易合约列表 ", mainFuturnByList)

# dayNumBar = 100000
# def test3(futurnCode):
#     datenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
#     df0 = get_bars(futurnCode, dayNumBar, unit='1d',
#                    fields=['date', 'open', 'high', 'low', 'close'],
#                    include_now=False, fq_ref_date=datenow,
#                    end_dt=datenow)
#     print(df0.head(2))
#     print(df0.tail(2))
#     print(df0.size)

# 增加单个看好合约
def addOne(futurnCode, futurnName):
    getDataByCodeToFile(futurnCode, futurnName, path=r'D:\\\\ideaWorkspace\\python\\jqJson\\')


# if __name__ == '__main__':
# addOne("B1907.XDCE", "豆二合约")
def start_fetch():
    readCsv()
    # test1()

    # test2("C9999.XDCE")
    # test2("C8888.XDCE")
    # test2("AP9999.XZCE")  # 苹果合约
    # test2("AP8888.XZCE")
    # activeFuturn_query("ZC")
    # addOne("B1907.XDCE", "豆二合约")
    # addOne("000016.XSHG", "上证50")
    # add_shang_hai_50("000016.XSHG", "上证50")
start_fetch()