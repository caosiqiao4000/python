# coding: utf-8
'''
双均线策略，当五日均线位于十日均线上方则买入，反之卖出。
'''
# from jqboson.api.settings import set_benchmark,set_option
# import logging as log

if __name__ == '__main__':
    import jqsdk
    params = {
        'token':'8add836db38a3450ccbf0d5653f90f8b',
        'algorithmId':7,
        'baseCapital':20000,#初始资金
        'frequency':'day',#运行频率
        'startTime':'2017-06-01',
        'endTime':'2019-08-01',
        'name':"Test1",
    }
    jqsdk.run(params)

# 导入聚宽函数库
import jqdatadir

# 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    # 定义一个全局变量, 保存要操作的股票
    # 000001 XSHG(股票:平安银行) XSHE
    g.security = '601318.XSHG'
    # 设定沪深300作为基准
    set_benchmark('601318.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    #设置成交量比例  设定成交量比例，根据实际行情限制每个订单的成交量.
    set_option('order_volume_ratio', 0.15)

# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context, data):
    security = g.security
    # 获取股票的收盘价
    close_data = attribute_history(security, 200, '1d', ['close'])
    # 取得过去五天的平均价格
    MA5 = close_data['close'].mean()
    # 取得上一时间点价格
    current_price = close_data['close'][-1]
    # 取得当前的现金
    cash = context.portfolio.cash

    # 如果上一时间点价格高出五天平均价5%, 则全仓买入
    if current_price > 1.05*MA5 and  current_price*100<cash:
        # 用所有 cash 买入股票
        order_value(security, current_price*100)
        # 记录这次买入
        log.info("Buying %s" % (security))
    # 如果上一时间点价格低于五天平均价, 则空仓卖出
    elif (current_price < 0.95*MA5
            and context.portfolio.positions[security].closeable_amount > 0):
        # 卖出所有股票,使这只股票的最终持有量为0
        order_target(security, 0)
        # 记录这次卖出
        log.info("Selling %s" % (security))
    # 画出上一时间点价格
    record(stock_price=current_price)