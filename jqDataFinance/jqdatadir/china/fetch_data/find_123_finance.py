# encoding:utf-8
import os

import requests
import datetime
from jqdatadir.china.fetch_data.find_2b_finance import *
from jpype import *

'''
    20190724
    查找123法则,在日线中查找
    中间间隔>3
    1 明显趋势 顶底都高于/低于前顶底
    2 横盘趋势  ABC 顶底点的大小关系不明确   左尖/右尖三角,乱形都有
    
    只处理 123趋势 和 突破 2B 其他不识别  资金越大,周期级别越高,10万下做日线
    
    趋势不明显,经过的时间就长,趋势明显经过的时间就短
    
    
'''
url_season = "http://47.94.198.204:8281/json/data.json"
url_week = "http://47.94.198.204:8281/json/dataWeek.json"
url_hour = "http://47.94.198.204:8281/json/dataHour.json"
bar_path = "D:\\\\ideaWorkspace\\python\\jqJson\\"


def judge_area_2b(point_current_area_c):
    ''''
        判断 2B 的相对点位水平
    '''
    return point_current_area_c > 0.984 and point_current_area_c < 1.016


def handler_period(key, dict_ali_season, period, last_point):
    '''
    处理逻辑
    :param key:
    :param dict_ali_season:
    :param period:
    :return: true/false 是否有趋势 , 1 up 2 down 3 棋盘
    '''
    dict_value_season_ali = dict_ali_season[key]

    # 最后的时间是什么时候  point  percent days dates
    list_m_point_ali = dict_value_season_ali['point']
    list_m_days_ali = dict_value_season_ali['days']  # 用来防止当前C点的位置就是最新的位置,这样可能C点未调整完成
    list_m_dates_ali = dict_value_season_ali['dates']
    # print(list_m_day_ali)
    list_m_percent_ali = dict_value_season_ali['percent']

    #
    season_point_len = len(list_m_point_ali)
    area_up_ac = 1.03
    # area_up_ab = 1.1
    area_down_ac = 0.97
    # area_down_ab = 0.9
    position_back_sace = 0.45

    #  e点-c点-顺势 b点-d点-反转 可能是 2B   表示可以2B买入
    point_current_area_c = list_m_point_ali[season_point_len - 1] / list_m_point_ali[season_point_len - 3]
    point_current_area_b = list_m_point_ali[season_point_len - 2] / list_m_point_ali[season_point_len - 4]
    twoB_reslut_c = judge_area_2b(point_current_area_c)
    twoB_reslut_b = judge_area_2b(point_current_area_b)

    point_current_area = list_m_point_ali[season_point_len - 2] / last_point._values[0]
    if season_point_len >= 5:
        # --------------------------abcde  一些趋势中横盘情况,加速情况,造成的 ABC三点不一定是趋势 但ABCDE却是趋势
        # 当前e点> a点* area_up_ac and b点>e点* area_up or d点>e点*area_up_ac
        if list_m_point_ali[season_point_len - 1] > list_m_point_ali[season_point_len - 5] * area_up_ac \
                and ((list_m_point_ali[season_point_len - 4] > list_m_point_ali[season_point_len - 1] * area_up_ac) \
                     or (list_m_point_ali[season_point_len - 2] > list_m_point_ali[season_point_len - 1] * area_up_ac)):
            # d点-e点)+e 的中间值< 当前天收盘价   表示回调结束
            if (list_m_point_ali[season_point_len - 2] - list_m_point_ali[season_point_len - 1]) / position_back_sace \
                    + list_m_point_ali[season_point_len - 1] < last_point._values[0]:
                if twoB_reslut_c:
                    print(key, "%s is up-trend c点 %s,e点 %s abcde形态 底部2B盘整点" % (period, list_m_point_ali[season_point_len - 3], list_m_point_ali[season_point_len - 1]))
                if twoB_reslut_b:
                    print(key, "%s is up-trend b点 %s,d点 %s abcde形态 顶部2B盘整点 " % (period, list_m_point_ali[season_point_len - 4], list_m_point_ali[season_point_len - 2]))
                if twoB_reslut_b and twoB_reslut_c:
                    print("abcde形态 顶底2B盘整")
                print(key, "%s is up-trend abcde形态 last-point %s" % (period, last_point._values[0]), list_m_dates_ali[-5:], list_m_point_ali[-5:])
                return True, 1
        # abcde  一些趋势中横盘情况,加速情况,造成的 ABC三点不一定是趋势 但ABCDE却是趋势  当前e点　＜ a点* area_down_ac and b点<e点* area_down_ac or d点<e点*area_down_ac
        elif list_m_point_ali[season_point_len - 1] < list_m_point_ali[season_point_len - 5] * area_down_ac \
                and ((list_m_point_ali[season_point_len - 4] < list_m_point_ali[season_point_len - 1] * area_down_ac) \
                     or (list_m_point_ali[season_point_len - 2] < list_m_point_ali[season_point_len - 1] * area_down_ac)):
            # d点-e点)+e 的中间值< 当前天收盘价   表示回调结束
            if (list_m_point_ali[season_point_len - 2] - list_m_point_ali[season_point_len - 1]) / position_back_sace + list_m_point_ali[season_point_len - 1] > last_point._values[
                0]:
                if twoB_reslut_c:
                    print(key, "%s is down-trend c点 %s,e点 %s abcde形态 顶部2B盘整点" % (period, list_m_point_ali[season_point_len - 3], list_m_point_ali[season_point_len - 1]))
                if twoB_reslut_b:
                    print(key, "%s is down-trend b点 %s,d点 %s abcde形态 底部2B盘整点 " % (period, list_m_point_ali[season_point_len - 4], list_m_point_ali[season_point_len - 2]))
                if twoB_reslut_b and twoB_reslut_c:
                    print("abcde形态 顶底2B盘整")
                print(key, "%s is down-trend abcde形态 last-point %s" % (period, last_point._values[0]), list_m_dates_ali[-5:], list_m_point_ali[-5:])
                return True, 1

    # abc 当前c点> a点* area_up_ac and b点>c点* area_up_ab
    if list_m_point_ali[season_point_len - 1] > list_m_point_ali[season_point_len - 3] * area_up_ac \
            and list_m_point_ali[season_point_len - 2] > list_m_point_ali[season_point_len - 1] * area_up_ac:
        #  b点-C点)+c < 当前天收盘价   表示回调结束
        if (list_m_point_ali[season_point_len - 2] - list_m_point_ali[season_point_len - 1]) * position_back_sace + list_m_point_ali[season_point_len - 1] < last_point._values[
            0]:
            if point_current_area > 0.984 and point_current_area > 1.016:
                print(key, "%s is up-trend last_point %s abc  2B顶部盘整点" % (period, last_point._values[0]), list_m_dates_ali[-3:], list_m_point_ali[-3:])
            else:
                print(key, "%s is up-trend last_point %s abc形" % (period, last_point._values[0]), list_m_dates_ali[-3:], list_m_point_ali[-3:])
            return True, 1
    # abc 当前c点 < a点* area_down_ac and b点　＜　c点* area_down_ac
    elif list_m_point_ali[season_point_len - 1] < list_m_point_ali[season_point_len - 3] * area_down_ac \
            and list_m_point_ali[season_point_len - 2] < list_m_point_ali[season_point_len - 1] * area_down_ac:
        # b点-C点 的中间值< 当前天收盘价  > 当前天收盘价下区间    表示回调结束
        if (list_m_point_ali[season_point_len - 2] - list_m_point_ali[season_point_len - 1]) * position_back_sace + list_m_point_ali[season_point_len - 1] > last_point._values[
            0]:
            if point_current_area > 0.984 and point_current_area > 1.016:
                print(key, "%s is down-trend last_point %s abc形态 2B底部盘整点" % (period, last_point._values[0]), list_m_dates_ali[-3:], list_m_point_ali[-3:])
            else:
                print(key, "%s is down-trend last_point %s abc形态 " % (period, last_point._values[0]), list_m_dates_ali[-3:], list_m_point_ali[-3:])
        return True, 2
    return False, 3


def read_csv():
    dict_ali_season = query_taobao_json(url_season, "season")  # 取得趋势区间文件
    dict_ali_week = query_taobao_json(url_week, "week")  # 取得趋势区间文件
    dict_ali_hour = query_taobao_json(url_hour, "hour")  # 取得趋势区间文件
    # list_tb_stock = dict_ali_season.keys()

    # 从文件夹中读取相应的数据做 hmm (隐马尔可夫)模型计算
    pathDir = os.listdir(bar_path)  # 获取filepath文件夹下的所有Bars的文件

    for key in list(dict_ali_week):  # 循环每个品种
        if str(key).__contains__('8888'):
            continue
        # 取 2B 区间点的上下值
        last_point = get_last_point_by_file(pathDir, key)  # 最新一天的收盘价

        # is_have_season, trend_num_season = handler_period(key, dict_ali_season, "season", last_point)
        is_have_week, trend_num_week = handler_period(key, dict_ali_week, "week", last_point)
        if is_have_week:
            is_have_hour, trend_num_hour = handler_period(key, dict_ali_hour, "hour", last_point)
            print("\n")
    pass


if __name__ == '__main__':
    read_csv()
    # print(1656.5 /1711)
    pass
