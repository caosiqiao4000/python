# coding: utf-8
'''
多股票持仓示例
'''
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

def initialize(context):
    # 初始化此策略
    # 设置我们要操作的股票池
    g.stocks = ['000001.XSHE','000002.XSHE','000004.XSHE','000005.XSHE']
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)

# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context, data):
    # 循环每只股票
    for security in g.stocks:
        # 得到股票之前3天的平均价
        vwap = data[security].vwap(200)
        # 得到上一时间点股票平均价
        price = data[security].close
        # 得到当前资金余额
        cash = context.portfolio.cash

        # 如果上一时间点价格小于三天平均价*0.995，并且持有该股票，卖出
        if price < vwap * 0.995 and context.portfolio.positions[security].closeable_amount > 0:
            # 下入卖出单
            order(security,-100)
            # 记录这次卖出
            log.info("Selling %s" % (security))
        # 如果上一时间点价格大于三天平均价*1.005，并且有现金余额，买入
        elif price > vwap * 1.005 and cash > 0:
            # 下入买入单
            order(security,100)
            # 记录这次买入
            log.info("Buying %s" % (security))