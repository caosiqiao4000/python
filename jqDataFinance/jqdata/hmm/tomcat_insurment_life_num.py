# encoding:utf-8

'''
20190528
 给所有品种 生命周期 排序
 幅度大,时间小 - 暴涨暴跌  幅度小,时间大 - 盘整      其他是正常趋势

 按与历史的位置来划分反转的概率  超过80% 的反转概率大,未超过 10%的,可能是假反转,还是在上一个趋势中 的 次级调整

    按周更新,发现可以投资性
    超过80%的    关注 123 法则 反转
    如果 其他关注 趋势的发展情况
    在盘整时,可能会反转,也可以会继续原来的趋势,要尽量避开 降低仓位

    20190622
    使用生命周期 周来分段 计算其他的 HMM (隐马尔可夫)结果  计算其他的连续状态,和转换状态概率

'''
import requests
from pyquery import PyQuery as pq
import demjson
import pandas as pd
import os

url_month = "http://47.94.198.204:8281/json/data.json"
url_week = "http://47.94.198.204:8281/json/dataWeek.json"
csv_bar_path = r'D:\ideaWorkspace\python\jqJson'


def query_taobao_json(url, date_period):
    htmlText = requests.get(url).text
    # json_life = json.loads(htmlText)
    json_life_two = demjson.decode(htmlText)
    # print(json_life)
    print(type(json_life_two))
    return json_life_two
    pass


def fetch_life_by_aliyun():
    dict_month = query_taobao_json(url_month, "moonth")
    dict_week = query_taobao_json(url_week, "week")
    # df = pd.DataFrame(columns=["name", "month", "week", "avg_m_w","des_m","des_w"])  # 创建一个空的dataframe
    dict_week_calu = {}
    dict_month_calu = {}
    # 从文件夹中读取相应的数据做 hmm (隐马尔可夫)模型计算
    pathDir = os.listdir(csv_bar_path)  # 获取filepath文件夹下的所有的文件
    print(type(pathDir))
    for key in dict_week:
        dict_value_month = dict_month[key]
        dict_value_week = dict_week[key]
        # 最后的时间是什么时候
        list_m_dates = dict_value_month['dates']
        list_k_dates = dict_value_week['dates']
        # 经过的天数
        list_m_days = dict_value_month['days']
        list_k_days = dict_value_week['days']
        str_des_one = "last month   %s ,  last week   %s\n" % (list_m_dates[len(list_m_dates) - 1],
                                                               list_k_dates[len(list_k_dates) - 1])
        # print(key, "  ", str_des_one, file=file_des)
        print(key, "  ", str_des_one)

        is_day_list = pathDir.__contains__("day")
        files = []
        for allDir in pathDir:
            # child = os.path.join('%s\\%s' % (csv_bar_path, allDir))
            files.append(allDir)  # .decode('gbk')是解决中文显示乱码问题
            # print child
            # if os.path.isdir(child):
            #     print child
            #     simplepath = os.path.split(child)
            #     print simplepath
        # print(files)

        # =======================
        # list_month = dict_value_month['deript'].__str__().split("#")
        # print(list_month)
        # print(current_trend_days_month)
        # print(list_month[2], list_month[4], list_month[6], list_month[8], list_month[10])
        # =======================
        # list_week = dict_value_week['deript'].__str__().split("#")
        # print(list_week[2], list_week[4], list_week[6], list_week[8], list_week[10])

    # print(dict_week_calu, "\n")
    # print(dict_month_calu)
    # print(df)
    pass


fetch_life_by_aliyun()
