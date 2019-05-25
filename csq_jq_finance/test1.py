# coding: utf-8

##### 下方代码为 IDE 运行必备代码 #####
# from jqboson.api.settings import set_benchmark,set_option
# import logging as log


if __name__ == '__main__':
    import jqsdk
    params = {
        'token':'8add836db38a3450ccbf0d5653f90f8b',
        'algorithmId':1,
        'baseCapital':1000000,#初始资金
        'frequency':'day',#运行频率
        'startTime':'2017-06-01',
        'endTime':'2017-08-01',
        'name':"Test1",
    }
    jqsdk.run(params)

##### 下面是策略代码编辑部分 #####
# 导入聚宽函数库
import jqdata
def initialize(context):
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    log.info('initialize run only once')
    run_daily(market_open, time='open', reference_security='000300.XSHG')

def market_open(context):
    # 输出开盘时间
    log.info('(market_open):' + str(context.current_dt.time()))