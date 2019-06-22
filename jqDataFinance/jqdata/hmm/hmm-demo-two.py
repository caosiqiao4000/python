# encoding:utf-8
'''
https://www.baidu.com/link?url=QIzmq0v9NtyvrwYPWr8Y2OaYVATxhGuTxa_S9nmOOwErn9C7tJhaJo2GomUeIbXU9FQy6qfEFJKMiyzdF3QiZvLV3YmJCVl38TvFrfofDgG&wd=&eqid=a09c2435000fe494000000065d0c58ac
https://blog.csdn.net/a19990412/article/details/82735155

 依据 天数 高低价 收盘价,成交量
'''
from hmmlearn import hmm
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import sys
sys.path.append('D:\\Program Files\\JoinQuant-Desktop-Py3\\Python\\')

# n = 6  # 6个隐藏状态
n = 4  # 6个隐藏状态

def start_hmm(local_csv_path,name_file):
    data = pd.read_csv(local_csv_path, index_col=0)
    volume = data['volume']
    close = data['close']
    print(close[0:4])

    # lows = np.array(data['low'])
    # print(lows)
    # print(np.log(lows))

    logDel = np.log(np.array(data['high'])) - np.log(np.array(data['low']))  # 将 最高最低 数据处理到 小值数
    logRet_1 = np.array(np.diff(np.log(close)))  # 收盘价格 依据公式计算所有数据的差异 收敛到一定 小值数
    logRet_5 = np.log(np.array(close[5:])) - np.log(np.array(close[:-5]))  # 收盘价 相差 五日 ? 计算 EMA 么
    logVol_5 = np.log(np.array(volume[5:])) - np.log(np.array(volume[:-5]))

    # 保持所有的数据长度相同
    logDel = logDel[5:]
    logRet_1 = logRet_1[4:]
    close = close[5:]

    Date = pd.to_datetime(data.index[5:])  # 从第五个开始的日期列
    A = np.column_stack([logDel, logRet_5, logVol_5])  # 合成 多维 列 数组
    model = hmm.GaussianHMM(n_components=n, covariance_type="full", n_iter=2000)
    model.fit(A)  # 训练模型————学习问题
    # model = hmm.GaussianHMM(n_components=n, covariance_type="full", n_iter=3000).fit(A)
    hidden_states = model.predict(A)  # 验证 得出隐藏状态结果   #估计 预测 状态序列————解码问题
    print(type(hidden_states), len(hidden_states))
    # print(hidden_states)

    # plt.figure(figsize=(25, 18))
    plt.figure(figsize=(50, 36))
    for i in range(n):
        pos = (hidden_states == i)  # 推断出来的可能状态 true用来显示当前色彩
        # plt.plot_date(Date[pos], close[pos], 'o', label='hidden state %d' % i, lw=2)
        plt.plot_date(Date[pos], close[pos], '.', label='hidden state %d' % i, lw=2)
        plt.legend()
    plt.show()

    res = pd.DataFrame({'Date': Date, 'logReg_1': logRet_1, 'state': hidden_states}).set_index('Date')
    return res
    # res.to_csv("file/300_4.csv")
    # series = res.logReg_1  # 收盘价格

    # templist = []
    # plt.figure(figsize=(25, 18))
    # for i in range(n):
    #     pos = (hidden_states == i)  # 推断出来的可能状态 true用来显示当前色彩
    #     pos = np.append(1, pos[:-1])  # 将 true 转化成1  false转化成 0
    #     res['state_ret%d' % i] = series.multiply(pos)  # 收盘价格 对应位置相乘
    #     # exp：高等数学里以自然常数e为底的指数函数
    #     # numpy.exp()：返回e的幂次方，e是一个常数为2.71828
    #     data_i = np.exp(res['state_ret%d' % i].cumsum())  # cumsum 累加 当前状态 当前日期之前的收盘价
    #     templist.append(data_i[-1])
    #     plt.plot_date(Date, data_i, '-', label='hidden state %d' % i)
    #     plt.legend()
    # plt.show()

    # templist = np.array(templist).argsort() # 排序   模拟买卖
    # long = (hidden_states == templist[-1]) + (hidden_states == templist[-2])  # 买入
    # short = (hidden_states == templist[0]) + (hidden_states == templist[1])  # 卖出
    # long = np.append(0, long[:-1])
    # short = np.append(0, short[:-1])
    #
    # plt.figure(figsize=(25, 18))
    # res['ret'] = series.multiply(long) - series.multiply(short)
    # plt.plot_date(Date, np.exp(res['ret'].cumsum()), 'r-')
    # plt.show()





