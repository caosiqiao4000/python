# encoding:utf-8
import os

import demjson
import requests
import datetime
from jqdatadir.china.common.util_file import *

'''
    20190724
    查找2B法则,在日线中查找
    中间间隔>3
    1 明显趋势 顶底都高于/低于前顶底
    2 横盘趋势  ABC 顶底点的大小关系不明确   左尖/右尖三角,乱形都有
    
    只处理 趋势 和 2B 其他不识别
    
'''
url_season = "http://47.94.198.204:8281/json/data.json"
url_week = "http://47.94.198.204:8281/json/dataWeek.json"
url_hour = "http://47.94.198.204:8281/json/dataHour.json"
bar_path = "D:\\\\ideaWorkspace\\python\\jqJson\\"


def get_last_point_by_file(pathDir, key):
    '''
    取得文件中的最近收盘价
    :param pathDir:
    :param key:
    :return:
    '''
    # ------------------------
    ## 依据名称找到对应的文件
    stockNameCN = str(key).split("_")[0]
    # print("======== ",stockNameCN)
    selected = [x for x in pathDir if x.__contains__(stockNameCN) and x.__contains__('day')]  # 选出同一个品种的三个文件
    # selected_week = [x for x in pathDir if x.__contains__(stockNameCN) and x.__contains__('week')]  # 选出同一个品种的三个文件
    # path_week = bar_path + selected[0]
    #合成两周为一个BAR的数据文件

    

    # ['000547.XSHE_航天发展day.csv', '000547.XSHE_航天发展month.csv', '000547.XSHE_航天发展week.csv']
    path_one = bar_path + selected[0]
    # data = pd.read_csv(path_one, index_col=0)
    data = read_csv_local(path_one, False)
    # print(data.tail(2),data.keys())
    return data.tail(1).loc[:, 'close']
    # print(key,data.tail(1).loc[:,'open'])
    pass

def read_csv_calu():
    dict_ali_season = query_taobao_json(url_season, "season")  # 取得趋势区间文件
    dict_ali_week = query_taobao_json(url_week, "week")  # 取得趋势区间文件
    list_tb_stock = dict_ali_season.keys()

    # 从文件夹中读取相应的数据做 hmm (隐马尔可夫)模型计算
    pathDir = os.listdir(bar_path)  # 获取filepath文件夹下的所有Bars的文件

    for key in list(list_tb_stock):  # 循环每个品种
        dict_value_season_ali = dict_ali_season[key]
        dict_value_week_ali = dict_ali_week[key]

        # 最后的时间是什么时候  point  percent days dates
        list_m_point_ali = dict_value_season_ali['point']
        list_k_point_ali = dict_value_week_ali['point']
        list_m_percent_ali = dict_value_season_ali['percent']
        list_k_percent_ali = dict_value_week_ali['percent']
        # 取 2B 区间点的上下值
        last_point = get_last_point_by_file(pathDir, key)#最新一天的收盘价
        last_point_max_area_m, last_point_min_area_m = get_max_min_area(last_point._values[0])
        last_point_max_area_k, last_point_min_area_k = get_max_min_area(last_point._values[0], area=0.01)
        # 查找符合 point 条件的位置索引
        current_trend_m = list_m_percent_ali[len(list_m_percent_ali) - 1]
        selected_point_m = [x for x in range(0, len(list_m_point_ali) - 1) if list_m_point_ali[x] > last_point_min_area_m and list_m_point_ali[x] < last_point_max_area_m
                            and ((list_m_percent_ali[x] < 0 and current_trend_m < 0) or (list_m_percent_ali[x] > 0 and current_trend_m > 0))]
        current_trend_k = list_k_percent_ali[len(list_k_percent_ali) - 1]
        selected_point_k = [x for x in range(0, len(list_k_point_ali) - 1) if list_k_point_ali[x] > last_point_min_area_k and list_k_point_ali[x] < last_point_max_area_k
                            and ((list_k_percent_ali[x] < 0 and current_trend_k < 0) or (list_k_percent_ali[x] > 0 and current_trend_k > 0))]
        # 最后的时间是什么时候  point  percent days dates
        list_m_dates_ali = dict_value_season_ali['dates']
        list_k_dates_ali = dict_value_week_ali['dates']
        # 找出 索引对应的 日期
        datenow = datetime.datetime.now().strftime('%Y-%m-%d');
        datenow_new = datetime.datetime.strptime(datenow, '%Y-%m-%d')
        # 找出 索引对应的 日期 限制一定的时间内, ----------- 最终符合 point,时间 条件的位置索引
        sel_recent_time_2b_m_index = [i for i in selected_point_m if
                                      (datenow_new - datetime.datetime.strptime(str(list_m_dates_ali[i]).replace('.0', ''), '%Y%m%d')).days < 1200]
        sel_recent_time_2b_k_index = [i for i in selected_point_k if
                                      (datenow_new - datetime.datetime.strptime(str(list_k_dates_ali[i]).replace('.0', ''), '%Y%m%d')).days < 200]

        if len(sel_recent_time_2b_m_index) > 1:
            print(key, last_point_max_area_m, last_point_min_area_m, '\nmonth 2b ', sel_recent_time_2b_m_index, [list_m_point_ali[x] for x in sel_recent_time_2b_m_index],
                  [list_m_dates_ali[x] for x in sel_recent_time_2b_m_index])
        if len(sel_recent_time_2b_k_index) > 1:
            print(key, last_point_max_area_k, last_point_min_area_k, '\nweek 2b ', sel_recent_time_2b_k_index, [list_k_point_ali[x] for x in sel_recent_time_2b_k_index],
                  [list_k_dates_ali[x] for x in sel_recent_time_2b_k_index])
        if len(sel_recent_time_2b_k_index) > 1 or len(sel_recent_time_2b_m_index) > 1:
            print("\n")
        continue
        # else:
        # return
        # print(last_point_max_area_m, '---xxx-------', last_point_min_area_m, '\n')
        # list_m_percent_ali = dict_value_season_ali['percent']
        # list_k_percent_ali = dict_value_week_ali['percent']
    pass


if __name__ == '__main__':
    read_csv_calu()
    # print(1656.5 /1711)
    pass
