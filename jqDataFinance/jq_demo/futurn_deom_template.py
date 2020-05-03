# 导入函数库
from jqdatadir import *

## 初始化函数，设定基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 过滤掉order系列API产生的比error级别低的log
    # log.set_level('order', 'error')
    # 输出内容到日志 log.info()
    log.info('初始函数开始运行且全局只运行一次')

    ### 期货相关设定 ###
    # 设定账户为金融账户
    set_subportfolios([SubPortfolioConfig(cash=context.portfolio.starting_cash, type='index_futures')])
    # 期货类每笔交易时的手续费是：买入时万分之0.23,卖出时万分之0.23,平今仓为万分之23
    set_order_cost(OrderCost(open_commission=0.000023, close_commission=0.000023,close_today_commission=0.0023), type='index_futures')
    # 设定保证金比例
    set_option('futures_margin_rate', 0.15)

    # 设置期货交易的滑点
    set_slippage(FixedSlippage(0.2))
    # 运行函数（reference_security为运行时间的参考标的；传入的标的只做种类区分，因此传入'IF1512.CCFX'或'IH1602.CCFX'是一样的）
      # 开盘前运行
    run_daily( before_market_open, time='before_open', reference_security='IF1512.CCFX')
      # 开盘时运行
    run_daily( market_open, time='open', reference_security='IF1512.CCFX')
      # 收盘后运行
    run_daily( after_market_close, time='after_close', reference_security='IF1512.CCFX')


## 开盘前运行函数
def before_market_open(context):
    # 输出运行时间
    log.info('函数运行时间(before_market_open)：'+str(context.current_dt.time()))

    # 给微信发送消息（添加模拟交易，并绑定微信生效）
    # send_message('美好的一天~')

    ## 获取要操作的股票(g.为全局变量)
      # 获取当月沪深300指数期货合约
    g.IF_current_month = get_future_contracts('IF')[0]
      # 获取下季沪深300指数期货合约
    g.IF_next_quarter = get_future_contracts('IF')[2]

## 开盘时运行函数
def market_open(context):
    log.info('函数运行时间(market_open):'+str(context.current_dt.time()))

    ## 交易

    # 当月合约
    IF_current_month = g.IF_current_month
    # 下季合约
    IF_next_quarter = g.IF_next_quarter

    # 合约列表
    # 当月合约价格
    IF_current_month_close = get_bars(IF_current_month, count=1, unit='1d', fields=['close'])["close"]
    # 下季合约价格
    # IF_next_quarter_close = hist[IF_next_quarter][0]
    IF_next_quarter_close = get_bars(IF_next_quarter, count=1, unit='1d', fields=['close'])["close"]
    print(IF_current_month_close)
    print(IF_next_quarter_close)
    # 计算差值
    CZ = IF_current_month_close - IF_next_quarter_close

    # 获取当月合约交割日期
    end_data = get_CCFX_end_date(IF_current_month)

    # 判断差值大于80，且空仓，则做空当月合约、做多下季合约；当月合约交割日当天不开仓
    if (CZ > 80):
        if (context.current_dt.date() == end_data):
            # return
            pass
        else:
            if (len(context.portfolio.short_positions) == 0) and (len(context.portfolio.long_positions) == 0):
                log.info('开仓---差值：', CZ)
                # 做空1手当月合约
                order(IF_current_month, 1, side='short')
                # 做多1手下季合约
                order(IF_next_quarter, 1, side='long')
    # 如有持仓，并且基差缩小至70内，则平仓
    if (CZ < 70):
        if(len(context.portfolio.short_positions) > 0) and (len(context.portfolio.long_positions) > 0):
            log.info('平仓---差值：', CZ)
            # 平仓当月合约
            order_target(IF_current_month, 0, side='short')
            # 平仓下季合约
            order_target(IF_next_quarter, 0, side='long')

## 收盘后运行函数
def after_market_close(context):
    log.info(str('函数运行时间(after_market_close):'+str(context.current_dt.time())))
    # 得到当天所有成交记录
    trades = get_trades()
    for _trade in trades.values():
        log.info('成交记录：'+str(_trade))
    log.info('一天结束')
    log.info('##############################################################')

########################## 获取期货合约信息，请保留 #################################
# 获取金融期货合约到期日
def get_CCFX_end_date(fature_code):
    # 获取金融期货合约到期日
    return get_security_info(fature_code).end_date
