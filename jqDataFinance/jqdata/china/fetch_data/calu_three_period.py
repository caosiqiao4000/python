# encoding:utf-8
'''
20190603
计算三个周期数据的图表表现关系,及其他


'''
import datetime
import json, re

def on_start(big_period,mid_period,min_period,type_calu = 1):
    '''
    :param big_period: 最大周期数据 dataframe
    :param mid_period:
    :param min_period:
    :param type_calu:  1 算最高/低的时间/幅度 3 算连续涨跌天数
    :return:
    '''
    print(len(big_period),len(mid_period),len(min_period))
    for key in big_period:
        print(key)
        dict_one_big = big_period.get(key)
        dict_one_mid = mid_period.get(key)
        dict_one_min = min_period.get(key)
        # print(dict_one_big)
        for key_one in dict_one_big:
            print(key_one)
        return

    pass




def main_test():
    with open(r'D:\ideaWorkspace\python\jqJson\000016.XSHG_上证50&day.json', 'r',
              encoding='utf-8') as f:
        dict_day = json.loads(f.read())
        # print(type(dict_day))
        # print(jdict_day.get("date"))
        with open(r'D:\ideaWorkspace\python\jqJson\000016.XSHG_上证50&hour.json', 'r',
                  encoding='utf-8') as f_hour:
            dict_hour = json.loads(f_hour.read())
            with open(r'D:\ideaWorkspace\python\jqJson\000016.XSHG_上证50&fiveteen.json', 'r',
                      encoding='utf-8') as f_fiveteen:
                dict_fiveteen = json.loads(f_fiveteen.read())
                on_start(dict_day,dict_hour,dict_fiveteen)
    pass

main_test()