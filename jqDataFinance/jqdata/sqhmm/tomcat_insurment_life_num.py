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
    当日冲销
    在多头市场统计 连续下跌 后的反转概率 或者反之亦然

'''
import requests
import demjson
import os
from jqdata.sqhmm.plot_hmm_sq import *

# import openpyxl

url_month = "http://47.94.198.204:8281/json/data.json"
url_week = "http://47.94.198.204:8281/json/dataWeek.json"
bar_path = r'D:\\ideaWorkspace\python\jqJson'

str_appear_num = ("D发生次数", "W发生次数", "M发生次数")
str_mid_num = ('D趋势幅度中位数', 'W趋势幅度中位数', 'M趋势幅度中位数')
str_continuous_bar_num = "连续上涨天数"


def query_taobao_json(url):
    htmlText = requests.get(url).text
    # json_life = json.loads(htmlText)
    json_life_two = demjson.decode(htmlText)
    # print(json_life)
    # print(type(json_life_two))
    return json_life_two


def handle_double_day_str(double_day):
    after_day_str = str(double_day)
    return after_day_str[:4] + "-" + after_day_str[4:6] + "-" + after_day_str[6:8]


def next_continuous_add(day_row, month_row, week_row, key):
    '''
    统计一只stock的连续性
    :param day_row:        月,周,天 趋势段数据Bar
    :param month_row:
    :param week_row:
    :param key:                 stock 上班_00001
    :return:
    '''
    ten_zeros = np.zeros(25, dtype=float)
    df_up = pd.DataFrame(
        {str_continuous_bar_num: np.arange(1, 26), str_appear_num[0]: ten_zeros, str_mid_num[0]: ten_zeros,
         str_appear_num[1]: ten_zeros, str_mid_num[1]: ten_zeros,
         str_appear_num[2]: ten_zeros, str_mid_num[2]: ten_zeros}).set_index(str_continuous_bar_num)
    df_down = pd.DataFrame(
        {str_continuous_bar_num: np.arange(-1, -26, step=-1), str_appear_num[0]: ten_zeros, str_mid_num[0]: ten_zeros,
         str_appear_num[1]: ten_zeros, str_mid_num[1]: ten_zeros,
         str_appear_num[2]: ten_zeros, str_mid_num[2]: ten_zeros}).set_index(str_continuous_bar_num)

    # day_row["percent"] = (day_row["high"] - day_row["low"]) / day_row["low"]
    df_up, df_down = add_appear_num_to_df(day_row, df_up, df_down, str_appear_num[0], str_mid_num[0])
    if len(week_row) > 0:
        df_up, df_down = add_appear_num_to_df(week_row, df_up, df_down, str_appear_num[1], str_mid_num[1])
    if len(month_row) > 0:
        df_up, df_down = add_appear_num_to_df(month_row, df_up, df_down, str_appear_num[2], str_mid_num[2])
    # --------------------------------
    # df_analyze_result = pd.concat(df_up, df_down)
    # 处理中位数
    df_up[str_mid_num[0]] = df_up[str_mid_num[0]] / df_up[str_appear_num[0]]
    df_up[str_mid_num[1]] = df_up[str_mid_num[1]] / df_up[str_appear_num[1]]
    df_up[str_mid_num[2]] = df_up[str_mid_num[2]] / df_up[str_appear_num[2]]
    df_down[str_mid_num[0]] = df_down[str_mid_num[0]] / df_down[str_appear_num[0]]
    df_down[str_mid_num[1]] = df_down[str_mid_num[1]] / df_down[str_appear_num[1]]
    df_down[str_mid_num[2]] = df_down[str_mid_num[2]] / df_down[str_appear_num[2]]

    # print("--------------------- ", key, " is success bar data analyze ", day_row.iloc[0]['date'],
    #       day_row.iloc[len(day_row) - 1]['date'])
    return df_up, df_down


def add_appear_num_to_df(period_row, df_up, df_down, str_appear_num, str_mid_num):
    '''
    统计连续次数 保存到 df 中    连续N 个 bar 出现次数和bar的幅度
    :param period_row:   区间Bars
    :param df_up:      上涨的df
    :param df_down:
    :param str_appear_num:  连续次数 保存到哪一个列名里
    :param str_mid_num:     中位数,保存到哪一个列名里
    :return:
    '''
    # for index, row in day_row.iterrows():
    day_row_size = period_row.shape[0]  # 当前 DF 总行数
    j = 0
    is_up = False
    for index in range(0, day_row_size):
        # print(index, period_row.iloc[index])
        if period_row["trend"].iloc[index] > 0:
            if is_up == False and j < 0:  # 由跌转涨了
                df_down.loc[j, str_appear_num] += 1
                temp_percent_high = period_row["high"].iloc[index + j:index]
                temp_percent_low = period_row["low"].iloc[index + j:index]
                # print("------down save temp_percent_high ----", temp_percent_high,
                #       "------down save temp_percent_low ----", temp_percent_low)
                df_down.loc[j, str_mid_num] += (min(temp_percent_low) - max(temp_percent_high)) / max(temp_percent_high)
                j = 0
            if index == day_row_size - 1:
                temp_percent_high = period_row["high"].iloc[index - j:index + 1]
                temp_percent_low = period_row["low"].iloc[index - j:index + 1]
                # print("------up end save temp_percent_high ----", temp_percent_high,
                #       "------up end save temp_percent_low ----", temp_percent_low)
                j += 1
                df_up.loc[j, str_appear_num] += 1
                df_up.loc[j, str_mid_num] += (max(temp_percent_high) - min(temp_percent_low)) / min(temp_percent_low)
            else:
                is_up = True
                j += 1
        elif period_row["trend"].iloc[index] < 0:
            if is_up == True and j > 0:  # 由涨转跌了
                df_up.loc[j, str_appear_num] += 1
                # temp_percent = period_row["percent"].iloc[index - j:index]
                temp_percent_high = period_row["high"].iloc[index - j:index]
                temp_percent_low = period_row["low"].iloc[index - j:index]
                # print("------up save temp_percent_high ----", temp_percent_high,
                #       "------up save temp_percent_low ----", temp_percent_low)
                # print("------up save temp_percent ----", temp_percent)
                df_up.loc[j, str_mid_num] += (max(temp_percent_high) - min(temp_percent_low)) / min(temp_percent_low)
                j = 0
            if index == day_row_size - 1:
                # temp_percent = period_row["percent"].iloc[index + j:index + 1]
                temp_percent_high = period_row["high"].iloc[index + j:index + 1]
                temp_percent_low = period_row["low"].iloc[index + j:index + 1]
                # print("------down end save temp_percent_high ----", temp_percent_high,
                #       "------down end save temp_percent_low ----", temp_percent_low)
                j -= 1
                df_down.loc[j, str_appear_num] += 1
                # df_down.loc[j, str_mid_num] += temp_percent.sum()
                df_down.loc[j, str_mid_num] += (min(temp_percent_low) - max(temp_percent_high)) / max(temp_percent_high)
                pass
            else:
                is_up = False
                j -= 1
    # print("-----------df_up----------------", df_up)
    # print("-------------df_down--------------", df_down)
    return df_up, df_down


def start_life_result_add(dict_month, dict_week, key, data_one, data_two, data_three, writer, sheet_name_e):
    '''
    统计一段区间 连续次数  要使用区间文件和Bar数据文件
    :param dict_month:      月趋势文件 JSON
    :param dict_week:        周趋势文件 JSON
    :param key:                 每个品种名称
    :param data_one:
    :param data_two:
    :param data_three:
    :return:
    '''
    dict_value_week = dict_week[key]
    dict_value_m = dict_month[key]

    # 最后的时间是什么时候
    list_k_dates = dict_value_week['dates']
    list_m_dates = dict_value_m['dates']
    str_des_one = "last month %s,last week   %s\n" % (
        list_m_dates[len(list_m_dates) - 1], list_k_dates[len(list_k_dates) - 1])
    # print(key, "  ", str_des_one, file=file_des)
    print(key, "  ", str_des_one)
    # 经过的天数
    # list_k_days = dict_value_week['days']
    list_m_days = dict_value_m['days']
    list_m_h_or_low = dict_value_m["point"]  # "percent" 月高低点
    list_m_percent = dict_value_m["percent"]  # 月高低点
    days_min = 1000
    startrow_excel = 0
    for index in range(len(list_m_dates)):  # 循环品种全部的趋势区间段
        if index == 0:
            continue
        befter_day_str = handle_double_day_str(list_m_dates[index - 1])  # 趋势端的后一个顶底点
        after_day_str = handle_double_day_str(list_m_dates[index])  # 趋势端的前一个顶底点
        ## 最新的周数据不全,可能会导入当前的趋势突然反转,但实际没有反转 这里要处理一下
        int_days = abs(int(list_m_days[index]))  # 当前天数
        if len(list_m_dates) - 1 > index:
            if int_days < days_min and int_days > 5:
                # 找出最小天数
                days_min = int_days
        else:
            if float(days_min) * 0.26 > int_days:
                print(key, '当前天数为 %s' % int_days, "错误 不符合最小趋势天数*0.5", '以前最小天数为 %s' % days_min, befter_day_str,
                      after_day_str)
                continue
        ####--------- 切片 趋势区间
        one_row = data_one[(data_one.date <= after_day_str) & (data_one.date >= befter_day_str)]
        two_row = data_two[(data_two.date < after_day_str) & (data_two.date > befter_day_str)]
        three_row = data_three[(data_three.date < after_day_str) & (data_three.date > befter_day_str)]
        # print(three_row.describe())
        ### ==== p-528
        diff_point = (list_m_h_or_low[index] - list_m_h_or_low[index - 1])
        df_stock_summary = pd.DataFrame({'起始日': befter_day_str,
                                         '终止日': after_day_str,
                                         '天数': str(int_days),
                                         '起始点数': list_m_h_or_low[index - 1],
                                         '终止点数': str(list_m_h_or_low[index]),
                                         '点差': str(diff_point),
                                         '变动百分比': str(list_m_percent[index])}, index=[0])
        # print(df_stock_summary)
        df_up, df_down = next_continuous_add(one_row, two_row, three_row, key)
        # ---------写入excel 清除  df_up, df_down 没有有效数据的行
        outfile_df_up = df_up[
            (df_up[str_appear_num[0]] > 0) | (df_up[str_appear_num[1]] > 0) | (df_up[str_appear_num[2]] > 0)]
        outfile_df_down = df_down[(df_down[str_appear_num[0]] > 0) | (df_down[str_appear_num[1]] > 0) | (
                df_down[str_appear_num[2]] > 0)]
        # ----------------写入excel
        if index == 1:
            df_stock_summary.to_excel(writer, sheet_name=sheet_name_e)
            startrow_excel += len(df_stock_summary) + 1
        else:
            df_stock_summary.to_excel(writer, sheet_name=sheet_name_e, startrow=startrow_excel)
            startrow_excel += len(df_stock_summary) + 1
        outfile_df_up.to_excel(writer, sheet_name=sheet_name_e, startrow=startrow_excel)
        startrow_excel += len(outfile_df_up) + 1
        outfile_df_down.to_excel(writer, sheet_name=sheet_name_e, startrow=startrow_excel)
        startrow_excel += len(outfile_df_down) + 1
        writer.save()
    pass


def fetch_life_by_aliyun(writer, is_gp):
    '''
     从阿里取得计算好的周期段数据 使用KEY 作 HMM 计算
    使用周期数据作分段   统计其中的隐状态连续分布个数,
    使用最近的状态,找出历史上相同的区间状态  统计概率

    目标是 找出顺大趋势里,的 连续后,最大的赢利概率和赢亏比
    :param writer:
    :param is_gp:   是否是  1. 股票 ,2 期货 ,3 jf
    :return:
    '''
    dict_month = query_taobao_json(url_month)  # 月趋势文件 JSON
    dict_week = query_taobao_json(url_week)
    print(type(dict_week), "\n", dict_week.keys())
    # print("\n", dict_week.get("上证_000001"))
    # df = pd.DataFrame(columns=["name", "month", "week", "avg_m_w","des_m","des_w"])  # 创建一个空的dataframe
    # 从文件夹中读取相应的数据做 hmm (隐马尔可夫)模型计算
    pathDir = os.listdir(bar_path)  # 获取filepath文件夹下的所有Bars的文件
    # print(type(pathDir))

    hmm_stock_num = HmmStockNum()
    list_tb_stock = dict_week.keys()
    if is_gp == 1:
        list_tb_qh = [j for j in list_tb_stock if
                      j.__contains__('XSHE') or j.__contains__('XSHG') or j.__contains__('STOCK')]  # 找出所有股票的
    elif is_gp == 2:
        list_tb_qh = [j for j in list_tb_stock if
                      j.__contains__('XZCE') or j.__contains__('XDCE') or j.__contains__('XSGE') or j.__contains__(
                          'XINE')]  # 找出所有期货的
    else:
        list_tb_qh = [j for j in list_tb_stock if j.__contains__('JF-')]  # 外汇
    print("--------共 %s 个品种" % len(list_tb_stock), "其中股票\合约\外汇 %s 只" % (len(list_tb_qh)))
    for key in list(list_tb_qh):  # 循环每个品种
        ## 依据名称找到对应的文件
        stockNameCN = str(key).split("_")[0]
        # print("======== ",stockNameCN)
        selected = [x for x in pathDir if x.__contains__(stockNameCN)]  # 选出同一个品种的三个文件
        selected.sort()
        # ['000547.XSHE_航天发展day.csv', '000547.XSHE_航天发展month.csv', '000547.XSHE_航天发展week.csv']
        path_one = bar_path + "\\" + selected[0]
        ## ====================开始分区间 统计 bar在大趋势下逆向运动的连续天数后反转的概率  的连续性
        data_one = hmm_stock_num.read_csv_local(path_one)  # day
        data_two = hmm_stock_num.read_csv_local(bar_path + "\\" + selected[1])  # month
        data_three = hmm_stock_num.read_csv_local(bar_path + "\\" + selected[2])  # week
        if 'trend' not in data_one.columns:
            data_one.loc[:, "trend"] = data_one.loc[:, 'close'] - data_one.loc[:, 'open']
            data_two.loc[:, "trend"] = data_two.loc[:, 'close'] - data_two.loc[:, 'open']
            data_three.loc[:, "trend"] = data_three.loc[:, 'close'] - data_three.loc[:, 'open']

        # 统计一段区间 连续次数
        if len(data_one) > 0:
            sheet_name_e = '%s' % (key)
            start_life_result_add(dict_month, dict_week, key, data_one, data_two, data_three, writer, sheet_name_e)
            print("---------------------------------------------------- ", key, " is success to save excel ")
        else:
            print("-----------------xxxxxx--------------- ", key, " data_one is null ")
        ## ---是否保存

        ######################################### -------------  开始 hmm 计算  结果保存到 CSV 文件中
        # one_hmm_result = hmm_stock_num.start_hmm(path_one)
        # print(one_hmm_result)
        # two_hmm_result = hmm_stock_num.start_hmm(csv_bar_path + "\\" + selected[1])
        # print(two_hmm_result)
        # three_hmm_result = hmm_stock_num.start_hmm(csv_bar_path + "\\" + selected[2])
        # print(three_hmm_result)
        ## ====================开始分区间 统计 HMM 隐状态的连续性
        # start_hmm_result_add(dict_week, key, one_hmm_result, two_hmm_result, three_hmm_result)
        # =======================
        # list_month = dict_value_month['deript'].__str__().split("#")
        # print(list_month)
        # print(current_trend_days_month)
        # print(list_month[2], list_month[4], list_month[6], list_month[8], list_month[10])
        # =======================
        # list_week = dict_value_week['deript'].__str__().split("#")
        # print(list_week[2], list_week[4], list_week[6], list_week[8], list_week[10])
    pass

# path_excel = '%s\\series\\csq_finance_series_analyze_futurn.xlsx' % (bar_path)
# path_excel = '%s\\series\\csq_finance_series_analyze_stock.xlsx' % (bar_path)
path_excel = '%s\\series\\csq_finance_series_analyze_jf.xlsx' % (bar_path)
# with pd.read_excel(path_excel) as reader:  # doctest: +SKIP
#     print(reader)
with pd.ExcelWriter(path_excel) as writer:  # doctest: +SKIP
    # 是否是  1. 股票 ,2 期货 ,3 jf
    fetch_life_by_aliyun(writer, 3)
    writer.close()
