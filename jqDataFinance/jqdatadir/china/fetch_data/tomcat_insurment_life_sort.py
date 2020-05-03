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
import datetime

import requests
import demjson
import pandas as pd

url_half_y = "http://47.94.198.204:8281/json/dataBig.json"
url_season = "http://47.94.198.204:8281/json/data.json"
url_week = "http://47.94.198.204:8281/json/dataWeek.json"
url_hour = "http://47.94.198.204:8281/json/dataHour.json"

my_orders_list = ('*', "*")
dict_key_list = ('品种名称', 'halfy-天系数', 'halfy-幅度系数', 'season-天', 'season-幅度', '2周-天',
                 '2周-幅度', 'hour-天', 'hour-幅度', '品种机会总描述')


def query_taobao_json(url, date_period):
    htmlText = requests.get(url).text
    # json_life = json.loads(htmlText)
    json_life_two = demjson.decode(htmlText)
    # print(json_life)
    print(type(json_life_two))
    return json_life_two
    pass


def save_data_file(dict_new_result_valid):
    datenow = datetime.datetime.now().strftime('%Y%m%d');
    df_excel = pd.DataFrame(dict_new_result_valid, columns=dict_new_result_valid.keys())
    try:
        df_excel.to_excel(r'..\..\..\file\calu_life_all_%s.xlsx' % datenow, encoding='utf-8')
    except Exception as e:
        df_excel.to_excel(r'..\..\..\file\calu_life_all2_%s.xlsx' % datenow, encoding='utf-8')

    # df = pd.DataFrame(list(dict_m_k_valid.items()), index=range(0, len(dict_m_k_valid)),
    #                   columns=['name', 'value'])  # 创建一个空的dataframe
    # # df['next'] = list_next_line
    # df = df.sort_values(['value'])
    print("共选出 ", len(dict_new_result_valid.get(dict_key_list[0])))
    # df.to_csv(r'..\..\..\file\calu_life_all.csv', encoding='utf-8')
    pass


def calu_life_weigh(list_week, my_period, current_trend_days, descript):
    '''
    对取得的生命周期来排序
    :param list_week:       <class 'list'>: ["['上证", '总(上涨天数-下跌天数)', '312', '总(上涨幅度-下跌幅度)', '113.79', '总有效天数,幅度为', '84', '超过历史多少次天数', '13', '超过历史多少次幅度', "15']"]
    :param my_period:               是 week , month 周期
    :param current_trend_days:      day list 最后一个趋势天数,看正负来判断趋势方向
    :return:
    '''
    base_total_num = (int(list_week[6]) - 1) / 2
    print_str = "\n" + my_period + '\t' + descript + "\n\t"
    if base_total_num < 1:
        print_str += "单边总次数太少,淘汰,为 %s\n" % list_week
        return
    current_days = float(list_week[8])
    weigh_day = current_days / base_total_num  # 当前超过的天数次数/单边总次数
    current_scale = float(list_week[10].replace("']", ""))
    weigh_scale = current_scale / base_total_num
    if weigh_day == 0 or weigh_scale == 0:
        if weigh_day + weigh_scale > 0.1:
            if current_trend_days > 0:
                print_str += "----反转趋势向 上涨 未确定或者创 新最小区间记录\n"
            elif current_trend_days < 0:
                print_str += "----反转趋势向 下跌 未确定或者创 新最小区间记录\n"
        else:
            print_str += "----反转趋势未确立 很可能只是个小反弹\n"
    elif weigh_scale / weigh_day > 1.5:
        if current_trend_days > 0:
            print_str += "这是相对暴涨-后期会变得盘整\n"
        elif current_trend_days < 0:
            print_str += "这是相对暴跌-后期会变得盘整\n"
    elif weigh_scale / weigh_day < 0.4:
        print_str += "这是相对盘整----后期可能会有现趋势暴发行情\n"

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
    return [my_period, weigh_day, weigh_scale, (weigh_scale + weigh_day) / 2, print_str]


def star_sort(dict_half_y_calu, dict_season_calu, dict_week_calu, dict_hour_calu, dict_half_y):
    '''

    :param dict_half_y_calu:
    :param dict_season_calu:
    :param dict_week_calu:
    :param dict_hour_calu:      保存的
    :param dict_half_y:         阿里的字典数据  用来取半年周的单边次数
    :return:

    # 依据权重排序  关注点为:::高风险区(可能反转区)和机会区( <0.2
    # 目的 是要找出交易机会  周,月线小于0.2
            month   week  同方向 才加,       不同方向 周反向进入 >0.6时 加
    高                     大小周期都要反转,得分高
    中
    低
    未明                    趋势不是很明确    不持仓
    '''
    dict_new_result_valid = {dict_key_list[0]: [], dict_key_list[1]: [], dict_key_list[2]: [], dict_key_list[3]: [],
                             dict_key_list[4]: [], dict_key_list[5]: [], dict_key_list[6]: [],
                             dict_key_list[7]: [], dict_key_list[8]: [], dict_key_list[9]: []}  # 保存有用的品种信息 组装DF输出文件用
    list_next_line = []  # 打印拼接字符串
    # index = 0 是半年趋势危险系数 1是季度危险系数 2是周趋势进场系数 3 同向 2周趋势危险提醒系数
    opportunity_danger_coefficient = (0.45, 0.75, 1.4, 0.9)
    for key in dict_season_calu:
        list_next_line.append("\n")
        tuple_halfy = dict_half_y_calu.get(key)  # 时间与幅度的保存的数据
        tuple_m = dict_season_calu.get(key)  # 时间与幅度的保存的数据
        tuple_k = dict_week_calu.get(key)
        tuple_hour = dict_hour_calu.get(key)
        '''
           BTC/USD         ['month', 0.0, 0.0, 0.0, 'last month   20190604.0 ,  last week   20190609.0\nmonth\t----反转趋势向 下跌 未确定或者创 新最小区间记录\n单边总次数为 2.0 超过天数次数 0.0 超过幅度次数 0.0 \n', -4.0] 
 ['week', 0.05405405405405406, 0.05405405405405406, 0.05405405405405406, 'week\t上涨进入正常趋势区间,关注 进入区间\n单边总次数为 18.5 超过天数次数 0.05405405405405406 超过幅度次数 0.05405405405405406 \n', 4.0]
        '''
        # print(key, tuple_m, "\n", tuple_k, "\n", tuple_h)
        # -------------------------------------------------------------------
        ###
        day_hour_trend = tuple_hour[5]  ##  现在的方向天数
        day_k_trend = tuple_k[5]  ## 现在的方向天数
        if tuple_halfy and len((tuple_halfy)) >= 6:
            day_h_trend = tuple_halfy[5]
        else:
            day_h_trend = 0  ## 现在的方向天数
        if tuple_m and len((tuple_m)) >= 6:
            days_m_trend = tuple_m[5]
        else:
            days_m_trend = 0  ## 现在的方向天数
        # -------------------------------------------------------------------
        '''
           		季度周,2周 同方向				            季度周,2周 不同方向
半年周,季度周	危险提示 季度周2周 >0.75 时间+幅度>1.4		危险提示 季度周>0.75 时间+幅度>1.4	
,2周,小时	    机会值为 2周,小时 <0.45				        机会值为 2周,小时 >0.75 时间+幅度>1.4     
        '''
        if tuple_m:
            str_des_one = '只做顺趋势的交易 不做反转 '  # 拼接
            isShow = False  # 是否有进场的机会或者 已经进入高风险区
            if (day_k_trend < 0 and days_m_trend < 0) or (day_k_trend > 0 and days_m_trend > 0):  # 同方向了
                if tuple_m[2] + tuple_m[1] > opportunity_danger_coefficient[2] \
                        or tuple_m[2] > opportunity_danger_coefficient[1] \
                        or tuple_m[1] > opportunity_danger_coefficient[1]:  # 时间或者幅度
                    str_des_one = str_des_one + " 关注同向 季度周高风险区,除非早就上船,否则不做 考虑适当减仓\n"
                    if tuple_k[2] + tuple_k[1] > opportunity_danger_coefficient[2] \
                            or (tuple_k[2] > opportunity_danger_coefficient[1]
                                or tuple_k[1] > opportunity_danger_coefficient[1]):  # 时间或者幅度
                        str_des_one = str_des_one + "------------同向 关注 2周高风险区 考虑适当减仓\n"
                else:  # 在 季度周 低风险区
                    if tuple_k[2] + tuple_k[1] < opportunity_danger_coefficient[1] \
                            or (tuple_k[2] < opportunity_danger_coefficient[0] and tuple_k[2] > 0 \
                                and tuple_k[1] < opportunity_danger_coefficient[0]
                                and tuple_k[1] > 0):  # 2周的 时间或者幅度 在低位区
                        str_des_one = str_des_one + "------------同向 关注 2周 可能加仓 寻找 进场 机会区\n"
                        if (day_k_trend < 0 and day_hour_trend < 0) or (
                                day_k_trend > 0 and day_hour_trend > 0):  # 2周与小时区 都为同向 下跌/上涨
                            if tuple_hour[2] + tuple_hour[1] < opportunity_danger_coefficient[1] and (
                                    tuple_hour[2] < opportunity_danger_coefficient[0]) or tuple_hour[1] < \
                                    opportunity_danger_coefficient[0]:  # 小时区 时间或者幅度 在低位区
                                str_des_one = str_des_one + "------------关注2周与小时区 都为同向 小时区  可能可以开仓 寻找 进场 机会区\n"
                                isShow = True
                        else:  # 小时区与2周趋势相反  2周与季度周相同
                            if tuple_hour[2] + tuple_hour[1] > opportunity_danger_coefficient[2] or (
                                    tuple_hour[2] > opportunity_danger_coefficient[1]) or tuple_hour[1] > \
                                    opportunity_danger_coefficient[1]:  # 小时区 时间或者幅度 在高危区
                                str_des_one = str_des_one + "------------关注 小时区与其2周趋势相反  可能有回调加仓的机会 寻找 进场 机会区\n"
                                isShow = True
            else:  # 月与周不同方向   回调加仓或者减仓
                # 不同方向 季度周 在高危区时  周反向进入 >0,75时  可以 考虑减仓
                if tuple_m[2] + tuple_m[1] > opportunity_danger_coefficient[2] or tuple_m[2] > \
                        opportunity_danger_coefficient[1] or \
                        tuple_m[1] > opportunity_danger_coefficient[1]:  # 时间或者幅度
                    str_des_one = str_des_one + "------------关注不同向 季度周高风险区,除非早就上船,否则不做反趋势交易 考虑适当减仓\\n"
                    pass
                else:  # 不同方向 季度周 不在高危区时  周反向进入 >0,45时  可以回调考虑加仓
                    if tuple_k[2] + tuple_k[1] > opportunity_danger_coefficient[1] \
                            or (tuple_k[2] > opportunity_danger_coefficient[0]
                                or tuple_k[1] > opportunity_danger_coefficient[0]):  # 时间或者幅度
                        str_des_one = str_des_one + "------------不同向 关注 2周,季度周 可能可以回调加仓 寻找 进场 机会区\n"
                        if day_hour_trend > 0 and day_k_trend > 0 or (day_hour_trend < 0 and day_k_trend < 0):
                            # 2周与小时区同向
                            if tuple_hour[2] + tuple_hour[1] > opportunity_danger_coefficient[1] \
                                    or (tuple_hour[2] > opportunity_danger_coefficient[0]
                                        or tuple_hour[1] > opportunity_danger_coefficient[0]):  # 时间或者幅度
                                isShow = True
                        else:  # 小时区与2周 方向相反 (与季度周相同)
                            if tuple_hour[2] + tuple_hour[1] < opportunity_danger_coefficient[2] \
                                    or (tuple_hour[2] < opportunity_danger_coefficient[1]
                                        or tuple_hour[1] < opportunity_danger_coefficient[1]):  # 时间或者幅度
                                isShow = True
                            pass
            # if tuple_hour[2] + tuple_hour[1] < opportunity_danger_coefficient[1] or (
            #         tuple_hour[2] < opportunity_danger_coefficient[0]) or tuple_hour[1] < \
            #         opportunity_danger_coefficient[0]:  # 时间或者幅度
            #     str_des_one = str_des_one + "------------关注 小时区 可能可以回调加仓 寻找 进场 机会区\n"
            #     isShow = True
        if day_k_trend < 0 and (str(key).__contains__('XSHG') or str(key).__contains__('XSHE')):
            isShow = False
        # 已经有仓位的要显示情况
        for name in my_orders_list:
            if str(key).__contains__(name):
                isShow = True
        # 超过历史0.9的极危险区要显示 不做反转,所以不提示了
        # if tuple_halfy:
        #     dict_value_dict_half_y = dict_half_y[str(key).strip()]  # 一个品种的数据
        #     # 最后的时间是什么时候
        #     list_halfy_days = dict_value_dict_half_y['days']
        #     if (tuple_halfy[1] > opportunity_danger_coefficient[3] or tuple_halfy[2] > opportunity_danger_coefficient[
        #         3]) and len(list_halfy_days) > 12:
        #         isShow = True
        # if tuple_m[1] > opportunity_danger_coefficient[3] or tuple_m[2] > opportunity_danger_coefficient[3] \
        #         or tuple_k[1] > opportunity_danger_coefficient[3] or tuple_k[2] > opportunity_danger_coefficient[3]:
        #     isShow = True
        if isShow:
            #### 半年周 只参与警报,不参与 机会
            if tuple_halfy:
                if tuple_halfy[2]  + tuple_halfy[1] > opportunity_danger_coefficient[2] or tuple_halfy[2] > \
                        opportunity_danger_coefficient[1] or \
                        tuple_halfy[1] > opportunity_danger_coefficient[1]:
                    str_des_one = str_des_one + "------------关注 半年期高风险区\n"
            str_des_one += '半年周方向 %s 季度周方向 %s 2周方向 %s 小时区方向 %s\t' % (
                day_h_trend, days_m_trend, day_k_trend, day_hour_trend)  # 月,周 走势方向
            if tuple_halfy:
                str_des_one = str_des_one + tuple_halfy[4]
            if tuple_m:
                str_des_one = str_des_one + tuple_m[4]
            str_des_one = str_des_one + tuple_k[4]
            str_des_one += tuple_hour[4] + "\n\n"
            print(key, str_des_one, "\n")
            # ----------------------------
            dict_new_result_valid[dict_key_list[0]].append(str(key).strip())
            dict_new_result_valid[dict_key_list[1]].append('%.3f' % tuple_halfy[1])
            dict_new_result_valid[dict_key_list[2]].append('%.3f' % tuple_halfy[2])
            dict_new_result_valid[dict_key_list[3]].append('%.3f' % tuple_m[1])
            dict_new_result_valid[dict_key_list[4]].append('%.3f' % tuple_m[2])
            dict_new_result_valid[dict_key_list[5]].append('%.3f' % tuple_k[1])
            dict_new_result_valid[dict_key_list[6]].append('%.3f' % tuple_k[2])
            dict_new_result_valid[dict_key_list[7]].append('%.3f' % tuple_hour[1])
            dict_new_result_valid[dict_key_list[8]].append('%.3f' % tuple_hour[2])
            dict_new_result_valid[dict_key_list[9]].append(str_des_one)
        else:
            print(key, "没有机会")
    ###########  保存筛选结果到文件
    save_data_file(dict_new_result_valid)
    pass


def handle_double_day_str(double_day):
    after_day_str = str(double_day)
    return after_day_str[:4] + "-" + after_day_str[4:6] + "-" + after_day_str[6:8]


def sort_life():
    dict_half_y = query_taobao_json(url_half_y, "halfY")  # 取得趋势区间文件
    dict_season = query_taobao_json(url_season, "season")  # 取得趋势区间文件
    dict_week = query_taobao_json(url_week, "week")
    dict_hour = query_taobao_json(url_hour, "hour")
    print(dict_hour.keys(), "共 %s 个品种" % len(dict_hour.keys()))
    # df = pd.DataFrame(columns=["name", "month", "week", "avg_m_w","des_m","des_w"])  # 创建一个空的dataframe
    dict_week_calu = {}  # 时间与幅度的保存的数据
    dict_season_calu = {}
    dict_half_y_calu = {}
    dict_hour_calu = {}

    for key in dict_week:
        ## 聚乙烯合约_L9999   TA9999
        # if str(key).__contains__("EUR-USD") == False:
        #     continue
        # -----------------------------------------------------------------------------------------------
        dict_value_dict_half_y = dict_half_y[key]  # 一个品种的数据
        dict_value_season = dict_season[key]  # 一个品种的数据
        dict_value_week = dict_week[key]
        dict_value_hour = dict_hour[key]

        # 最后的时间是什么时候
        list_m_dates = dict_value_season['dates']
        list_k_dates = dict_value_week['dates']
        list_hour_dates = dict_value_hour['dates']
        if list_m_dates[0] > 20150000.0:  ## 至少要有四年的数据
            print(key, "----------------dates 历史数据不多 ", list_m_dates[0])
            continue

        list_halfy_days = dict_value_dict_half_y['days']
        list_m_days = dict_value_season['days']
        list_k_days = dict_value_week['days']
        list_hour_days = dict_value_hour['days']
        str_des_one = "-----------------last month   %s ,  last week   %s,  last hour   %s\n" % (
            list_m_dates[len(list_m_dates) - 1],
            list_k_dates[len(list_k_dates) - 1], list_hour_dates[len(list_hour_dates) - 1])
        print(key, "  ", str_des_one)

        list_halfy_deript = dict_value_dict_half_y['deript'].__str__().split("#")
        list_month_deript = dict_value_season['deript'].__str__().split("#")
        # <class 'list'>: ["['上证", '总(上涨天数-下跌天数)', '312', '总(上涨幅度-下跌幅度)', '113.79', '总有效天数,幅度为', '84', '超过历史多少次天数', '13', '超过历史多少次幅度', "15']"]
        list_week_deript = dict_value_week['deript'].__str__().split("#")
        list_hour_deript = dict_value_hour['deript'].__str__().split("#")
        # -------------------------------------------------------------------------------------------------
        ########################### 计算 大趋势下的回调连续天数后反转的概率 #########################################################

        ########################### 计算 得分 ##########################################################################
        ##先计算 周
        key_name = key + "        "
        ## ------------------------------------------------------------------ 周数据里要消除 最后趋势天数过低的情况
        # last_right_days_k = find_real_peroid_trend(key, list_k_days)
        last_right_days_k = int(list_k_days[-1])  # 最新趋势的天数
        dict_week_calu[key_name] = calu_life_weigh(list_week_deript, "week", last_right_days_k,
                                                   dict_value_week['deript'].__str__())
        ## ------------------------------------------------------------------ 月数据里要消除 最后趋势天数过低的情况
        last_right_days_m = int(list_m_days[-1])  # 最新趋势的天数
        dict_season_calu[key_name] = calu_life_weigh(list_month_deript, "season", last_right_days_m,
                                                     dict_value_season['deript'].__str__())
        ## ------------------------------------------------------------------ 月数据里要消除 最后趋势天数过低的情况
        last_right_days_halfy = int(list_halfy_days[-1])  # 最新趋势的天数
        dict_half_y_calu[key_name] = calu_life_weigh(list_halfy_deript, "halfY", last_right_days_halfy,
                                                     dict_value_dict_half_y['deript'].__str__())
        ## ------------------------------------------------------------------ 月数据里要消除 最后趋势天数过低的情况
        last_right_days_hour = int(list_hour_days[-1])  # 最新趋势的天数
        dict_hour_calu[key_name] = calu_life_weigh(list_hour_deript, "hour", last_right_days_hour,
                                                   dict_value_hour['deript'].__str__())
        ########################################################################################### 设置最后的趋势方向
        dict_hour_calu[key_name].append(last_right_days_hour)
        dict_week_calu[key_name].append(last_right_days_k)
        # print(key)
        # 添加最后一天的正负值用来判断方向
        if last_right_days_m:
            if dict_season_calu[key_name]:
                dict_season_calu[key_name].append(last_right_days_m)
        if last_right_days_halfy:
            if dict_half_y_calu[key_name]:
                dict_half_y_calu[key_name].append(last_right_days_halfy)
        ###############################################################################
        tuple_halfy = dict_half_y_calu.get(key_name);  # 时间与幅度的保存的数据
        tuple_m = dict_season_calu.get(key_name);  # 时间与幅度的保存的数据
        tuple_k = dict_week_calu.get(key_name);
        tuple_hour = dict_hour_calu.get(key_name);
        if tuple_halfy:  # 如果没有月数据就拼接到周描述里
            tuple_halfy[4] = str_des_one + tuple_halfy[4]
        elif tuple_m:
            tuple_m[4] = str_des_one + tuple_m[4]
        elif tuple_k:
            tuple_k[4] = str_des_one + tuple_k[4]
        else:
            tuple_hour[4] = str_des_one + tuple_hour[4]

        # df.append(dict_week)
        # df.append(dict_month)

    # print(dict_week_calu, "\n")
    # print(dict_month_calu)
    star_sort(dict_half_y_calu, dict_season_calu, dict_week_calu, dict_hour_calu, dict_half_y)
    # print(df)
    pass


# def get_des_file():
#     file = open(r'..\..\..\file\calu_life_all_des.csv', "w", encoding='utf-8')
#     return file


# def sort_test():
#     df = pd.DataFrame([['a', 1, 'c'], ['a', 3, 'a'], ['a', 2, 'b'],
#                        ['c', 3, 'a'], ['c', 2, 'b'], ['c', 1, 'c'],
#                        ['b', 2, 'b'], ['b', 3, 'a'], ['b', 1, 'c']], columns=['A', 'B', 'C'])
#     print(df)
#     # df.groupby('A', sort=False).apply(lambda x: x.sort_values('B', ascending=True)).reset_index(drop=True)
#     df = df.sort_values(['A', 'B'],inplace=False)
#     print(df)

if __name__ == '__main__':
    sort_life()
# sort_test()
