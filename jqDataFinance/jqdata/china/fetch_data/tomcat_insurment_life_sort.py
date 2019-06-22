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
'''
import requests
from pyquery import PyQuery as pq
import demjson
import pandas as pd

url_month = "http://47.94.198.204:8281/json/data.json"
url_week = "http://47.94.198.204:8281/json/dataWeek.json"


def query_taobao_json(url, date_period):
    htmlText = requests.get(url).text
    # json_life = json.loads(htmlText)
    json_life_two = demjson.decode(htmlText)
    # print(json_life)
    print(type(json_life_two))
    return json_life_two
    pass


# 对取得的生命周期来排序
def calu_life_weigh(list_week, my_period, current_trend_days, file_des):
    base_total_num = (int(list_week[6]) - 3) / 2
    print_str = my_period + "\t";
    if base_total_num == 0:
        print_str += "单边总次数为 %s" % list_week + "\n"
        return
    current_days = float(list_week[8]);
    weigh_day = current_days / base_total_num  # 当前超过的天数次数/单边总次数
    current_scale = float(list_week[10].replace("']", ""));
    weigh_scale = current_scale / base_total_num
    if weigh_day == 0 or weigh_scale == 0:
        if current_trend_days > 0:
            print_str += "----反转趋势向 上涨 未确定或者创 新最小区间记录\n"
        elif current_trend_days < 0:
            print_str += "----反转趋势向 下跌 未确定或者创 新最小区间记录\n"
    elif weigh_scale / weigh_day > 1.5:
        if current_trend_days > 0:
            print_str += "这是相对暴涨\n"
        elif current_trend_days < 0:
            print_str += "这是相对暴跌\n"
    elif weigh_scale / weigh_day < 0.4:
        print_str += "这是相对盘整\n"

    if weigh_scale > 0.85 or weigh_day > 0.85:
        if current_trend_days > 0:
            print_str += "上涨进入高风险区间,关注 右侧 反转\n"
        elif current_trend_days < 0:
            print_str += "下跌进入高风险区间,关注 右侧 反转\n"
    elif weigh_scale > 0.01 and weigh_day > 0.01:
        if current_trend_days > 0:
            print_str += "上涨进入正常趋势区间,关注 进入区间\n"
        elif current_trend_days < 0:
            print_str += "下跌进入正常趋势区间,关注 进入区间\n"

    print_str += "单边总次数为 %s 超过天数次数 %s 超过幅度次数 %s \n" % (base_total_num, weigh_day, weigh_scale)
    print(print_str, file=file_des)
    file_des.flush()
    return [my_period, weigh_day, weigh_scale, (weigh_scale + weigh_day) / 2, print_str]


# 依据权重排序  关注点为:::高风险区(可能反转区)和机会区( <0.2
# 目的 是要找出交易机会  周,月线小于0.2
'''
        month   week  同方向 才加,       不同方向 周反向进入 >0.6时 加
高                     大小周期都要反转,得分高
中                       
低                      
未明                    趋势不是很明确    不持仓  
'''
def star_sort(dict_month_calu, dict_week_calu):
    # print(dict_month_calu, "\n")
    # print(dict_week_calu, "\n")
    dict_m_k = {}
    list_next_line = []
    for key in dict_month_calu:
        list_next_line.append("\n")
        tuple_m = dict_month_calu.get(key);  # 时间与幅度的保存的数据
        tuple_k = dict_week_calu.get(key);
        '''
           BTC/USD         ['month', 0.0, 0.0, 0.0, 'last month   20190604.0 ,  last week   20190609.0\nmonth\t----反转趋势向 下跌 未确定或者创 新最小区间记录\n单边总次数为 2.0 超过天数次数 0.0 超过幅度次数 0.0 \n', -4.0] 
 ['week', 0.05405405405405406, 0.05405405405405406, 0.05405405405405406, 'week\t上涨进入正常趋势区间,关注 进入区间\n单边总次数为 18.5 超过天数次数 0.05405405405405406 超过幅度次数 0.05405405405405406 \n', 4.0]
        '''
        # print(key,tuple_m,"\n",tuple_k)
        ###
        day_k_trend = tuple_k[5]
        if tuple_m and len((tuple_m)) >= 6:
            day_m_trend = tuple_m[5]
        else:
            day_m_trend = 0
        if tuple_m:
            str_des_one = ''
            isShow = False
            if (day_k_trend < 0 and day_m_trend < 0) or (day_k_trend > 0 and day_m_trend > 0):  # 同方向了
                str_des_one = str_des_one + "月,周同方向\t"
                if tuple_m[2] > 0.8 or tuple_m[1] > 0.8:  # 时间或者幅度
                    str_des_one = str_des_one + " 关注 月高风险区\n"
                    isShow = True
                if tuple_k[2] > 0.7 or tuple_k[1] > 0.7:  # 时间或者幅度
                    str_des_one = str_des_one + " 关注 周高风险区\n"
                    isShow = True
                # if tuple_m[2] < 0.4:  # 时间或者幅度
                #     str_des_one = str_des_one + " 关注 月寻找进场机会区\n"
                #     isShow = True
                if tuple_k[2] < 0.45:  # 时间或者幅度
                    str_des_one = str_des_one + " 关注 周寻找 进场 机会区\n"
                    isShow = True
            else:  # 月与周不同方向   回调或者反转
                # 不同方向 周反向进入 >0.6时  可以回调考虑加仓
                str_des_one = str_des_one + "月,周 不同 方向\t"
                if tuple_m[2] > 0.8 or tuple_m[1] > 0.8:  # 时间或者幅度
                    str_des_one = str_des_one + " 关注 月高风险区\n"
                    isShow = True
                if tuple_k[2] > 0.3 or tuple_k[1] > 0.3:  # 时间或者幅度
                    str_des_one = str_des_one + " 关注 周 可能可以回调加仓 寻找 进场 机会区\n"
                    isShow = True
        else:  # 月度数据太少
            str_des_one = str_des_one + " 没有足够月线数据\t"
            # if tuple_k[2] > 0.8 or tuple_k[1] > 0.8:  # 时间或者幅度
            #     str_des_one = str_des_one + " 关注 周高风险区\n"
            #     isShow = True
            if tuple_k[2] < 0.4:  # 时间或者幅度
                str_des_one = str_des_one + " 关注 周寻找 进场 机会区\n"
                isShow = True
        if isShow:
            print(key, day_m_trend, day_k_trend)  # 月,周 走势方向
            if tuple_m:
                str_des_one = str_des_one + tuple_m[4]
            str_des_one = str_des_one + tuple_k[4]
            print(key, str_des_one, "\n")
            dict_m_k[key] = (str_des_one)
        else:
            print(key, "没有机会")
    ###########
    df = pd.DataFrame(list(dict_m_k.items()), index=range(0, len(dict_m_k)),
                      columns=['name', 'value'])  # 创建一个空的dataframe
    # df['next'] = list_next_line
    df = df.sort_values(['value'])
    print("共选出 ", len(dict_m_k))
    df.to_csv(r'..\..\..\file\calu_life_all.csv', encoding='utf-8')
    pass


def sort_life():
    dict_month = query_taobao_json(url_month, "moonth")
    dict_week = query_taobao_json(url_week, "week")
    # df = pd.DataFrame(columns=["name", "month", "week", "avg_m_w","des_m","des_w"])  # 创建一个空的dataframe
    dict_week_calu = {}
    dict_month_calu = {}
    file_des = get_des_file()

    for key in dict_week:
        dict_value_month = dict_month[key]
        dict_value_week = dict_week[key]
        # 最后的时间是什么时候
        list_m_dates = dict_value_month['dates']
        list_k_dates = dict_value_week['dates']

        list_m_days = dict_value_month['days']
        list_k_days = dict_value_week['days']
        str_des_one = "last month   %s ,  last week   %s\n" % (list_m_dates[len(list_m_dates) - 1],
                                                               list_k_dates[len(list_k_dates) - 1])
        print(key, "  ", str_des_one, file=file_des)

        # =======================
        list_month = dict_value_month['deript'].__str__().split("#")
        current_trend_days_month = dict_value_month['days']
        # print(list_month)
        # print(current_trend_days_month)
        # print(list_month[2], list_month[4], list_month[6], list_month[8], list_month[10])
        # =======================
        list_week = dict_value_week['deript'].__str__().split("#")
        current_trend_days_week = dict_value_week['days']
        # print(list_week[2], list_week[4], list_week[6], list_week[8], list_week[10])
        ##先计算 周
        key_name = key + "        "
        dict_week_calu[key_name] = calu_life_weigh(list_week, "week", int(current_trend_days_week[-1]), file_des)
        ##
        dict_month_calu[key_name] = calu_life_weigh(list_month, "month", int(current_trend_days_month[-1]), file_des)
        ### 设置最后的趋势方向
        dict_week_calu[key_name].append(list_k_days[len(list_k_days) - 1])
        # print(key)
        # 添加最后一天的正负值用来判断方向
        if list_m_days[len(list_m_days) - 1]:
            if dict_month_calu[key_name]:
                dict_month_calu[key_name].append(list_m_days[len(list_m_days) - 1])
        tuple_m = dict_month_calu.get(key_name);  # 时间与幅度的保存的数据
        tuple_k = dict_week_calu.get(key_name);
        if tuple_m:
            tuple_m[4] = str_des_one + tuple_m[4]
        else:
            tuple_k[4] = str_des_one + tuple_k[4]

        # df.append(dict_week)
        # df.append(dict_month)

    # print(dict_week_calu, "\n")
    # print(dict_month_calu)
    file_des.close()
    star_sort(dict_month_calu, dict_week_calu)
    # print(df)
    pass


def get_des_file():
    file = open(r'..\..\..\file\calu_life_all_des.csv', "w", encoding='utf-8')
    return file


# def sort_test():
#     df = pd.DataFrame([['a', 1, 'c'], ['a', 3, 'a'], ['a', 2, 'b'],
#                        ['c', 3, 'a'], ['c', 2, 'b'], ['c', 1, 'c'],
#                        ['b', 2, 'b'], ['b', 3, 'a'], ['b', 1, 'c']], columns=['A', 'B', 'C'])
#     print(df)
#     # df.groupby('A', sort=False).apply(lambda x: x.sort_values('B', ascending=True)).reset_index(drop=True)
#     df = df.sort_values(['A', 'B'],inplace=False)
#     print(df)


sort_life()
# sort_test()
