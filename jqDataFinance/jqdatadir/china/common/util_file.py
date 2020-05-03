# encoding:utf-8
import demjson
import pandas as pd
import requests


def query_taobao_json(url, date_period):
    '''
    请求一个网页地址 转化成json
    :param url:
    :param date_period:
    :return:
    '''
    htmlText = requests.get(url).text
    # json_life = json.loads(htmlText)
    json_life_two = demjson.decode(htmlText)
    # print(json_life)
    print(type(json_life_two))
    return json_life_two
    pass


def read_csv_local(local_csv_path,is_print = True):
    '''
    读取电脑本机的文件
    :param local_csv_path:
    :return:
    '''
    if is_print:
        print("现在读取 ", local_csv_path)
    f = open(local_csv_path)
    return pd.read_csv(f, index_col=0)


def get_max_min_area(value_temp, area=0.03):
    '''
    在一个数值列表里,取index的值的相应区间上下值
    :param list_m_point_ali:
    :return:
    '''
    return value_temp * (1 + area), value_temp * (1 - area)
    pass
