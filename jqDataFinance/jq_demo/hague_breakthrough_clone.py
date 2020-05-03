# coding: utf-8
if __name__ == '__main__':
    import jqsdk

    params = {
        'token': '5ecffde1e4df3dd2b10ad6bcdd4a5880',
        'algorithmId': 6,
        'baseCapital': 20000,  # 初始资金
        'frequency': 'minute',  # 运行频率 day minute
        'startTime': '2017-06-01',
        'endTime': '2019-08-01',
        'name': "hague_breakthrough_clone",
    }
    jqsdk.run(params)

# 克隆自聚宽文章：https://www.joinquant.com/post/21462
# 标题：单品种分钟级别回测期货海龟进阶版
# 作者：pittjia

# 克隆自聚宽文章：https://www.joinquant.com/post/1401
# 标题：【量化课堂】海龟策略
# 作者：JoinQuant量化课堂

'''
================================================================================
总体回测前
================================================================================
'''


# 导入函数库

# 总体回测前要做的事情
def initialize(context):
    set_params()  # 1设置策参数
    set_variables()  # 2设置中间变量
    set_backtest(context)  # 3设置回测条件


# 1
# 设置策略参数
def set_params():
    # symbol 和 security 二选一
    # 合约
    g.future_index = 'TA'
    # 最近一次交易的合约
    g.last_future = None
    # 标的代码
    g.future = None
    # 系统1入市的trailing date
    g.short_in_date = 20
    # 系统2入市的trailing date
    g.long_in_date = 55
    # 系统1 exiting market trailing date
    g.short_out_date = 10
    # 系统2 exiting market trailing date
    g.long_out_date = 20
    # 最大unit数目
    g.limit_unit = 4
    # 每次交易unit数目
    g.unit = 0
    # 加仓次数
    g.add_time = 0
    # 持仓状态
    g.position = 0
    # 记录期货最高价
    g.price_mark = 0
    # 初始化计数器,不要在盘中开启策略。用来控制分钟级别的策略每隔半小时执行一次
    g.run_num = -1
    # 可承受的最大损失率
    g.loss = 0.1
    # 若超过最大损失率，则调整率为：
    g.adjust = 0.8
    # 计算N值的天数
    g.number_days = 20
    # 系统1所配金额占总金额比例
    g.ratio = 0.8


# 2
# 设置中间变量
def set_variables():
    # 系统1的突破价格
    g.break_price1 = 0
    # 系统2的突破价格
    g.break_price2 = 0
    # 系统1执行且系统2不执行
    g.system1 = True


# 3
# 设置回测条件
def set_backtest(context):
    # 作为判断策略好坏和一系列风险值计算的基准
    # 和上面的两行代码二选一
    set_benchmark(get_future_code(g.future_index))

    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 过滤掉order系列API产生的比error级别低的log
    # log.set_level('order', 'error')
    # 输出内容到日志 log.info()
    cash = context.portfolio.starting_cash
    log.info('初始函数开始运行且全局只运行一次 %s ' % cash)

    ### 期货相关设定 ###
    # 设定账户为金融账户
    set_subportfolios([SubPortfolioConfig(cash, type='futures')])
    # 期货类每笔交易时的手续费是：买入时万分之0.23,卖出时万分之0.23,平今仓为万分之23
    set_order_cost(OrderCost(open_commission=0.000023, close_commission=0.000023, close_today_commission=0.0023), type='futures')
    # 设定保证金比例
    set_option('futures_margin_rate', 0.15)
    # 设置期货交易的滑点
    set_slippage(StepRelatedSlippage(2))

    # 运行函数（reference_security为运行时间的参考标的；传入的标的只做种类区分，因此传入'IF1512.CCFX'或'IH1602.CCFX'是一样的）
    # 开盘前运行
    run_daily(before_market_open, time='before_open', reference_security=get_future_code(g.future_index))
    # 开盘时运行
    run_daily(while_open, time='every_bar', reference_security=get_future_code(g.future_index))
    # 收盘后运行
    run_daily(after_market_close, time='after_close', reference_security=get_future_code(g.future_index))


## 开盘前运行函数
def before_market_open(context):
    ## 获取要操作的期货(g.为全局变量)
    # 获取当月期货合约
    g.future = get_dominant_future(g.future_index)


## 开盘时运行函数
def while_open(context):
    if minute_execution_interval() == False:
        return

    if g.future == None:
        before_market_open(context)

    # 如果主力合约变更，平仓
    reset_feture()

    # 当月合约
    future = g.future

    # 获取当月合约交割日期
    end_date = get_CCFX_end_date(future)
    # 当月合约交割日当天不开仓
    # TODO 添加提前换仓代码
    if (context.current_dt.date() == end_date):
        return

    # 确定时间是周几
    # weekday = context.current_dt.isoweekday()
    # log.info("今天是周 %s" % weekday)

    # 计算ATR
    ATR = get_ATR_N(context, future, g.number_days)

    market_in(context, future, g.short_in_date, ATR)
    # stop_loss 检查收盘价是否亏损超出建仓成本价的 5%  stop_loss_2检查当前价格是否处于 10日的反向趋势
    if g.position != 0 and stop_loss(context, future) == False and stop_loss_2(context, future, g.short_out_date) == False:
        # log.info("while_open:！每隔开半小时执行一次 ", str(context.current_dt))
        ## 已经开过仓了，则判断是否需要加仓
        market_add(context, future, g.short_in_date, ATR)
        ## 已经开过仓了，则判断是否需要止损
        market_stop_loss(context, future, g.short_out_date, ATR)


## 收盘后运行函数
def after_market_close(context):
    # 得到当天所有成交记录
    trades = get_trades()
    if len(trades.values()) <= 0:
        return
        # log.info(str('函数运行时间(after_market_close):' + str(context.current_dt.time())))
    log.info(str('收盘后 函数运行时间(after_market_close):' + str(context.current_dt)))
    for _trade in trades.values():
        log.info('成交记录：' + str(_trade))
    log.info('#######################一天结束#######################################')
    # 查看融资融券账户相关相关信息(更多请见API-对象-SubPortfolio)
    p = context.portfolio.subportfolios[0]
    #' - - - - - - - - - - -前面是公共的,后面是区分的 - - - - - - - - - - - - - - - - - - -
    log.info('账户所属类型：', p.type)
    log.info('账户转帐：', p.inout_cash)
    log.info('账户有效金额：', p.available_cash)
    log.info('账户可转移金额：', p.transferable_cash)
    log.info('账户锁定金额：', p.locked_cash)
    log.info('账户多单金额：', p.long_positions)
    log.info('账户空单金额：', p.short_positions)
    log.info('总资产：', p.total_value)
    log.info('账户仓位总价：', p.positions_value)
    if str(p.type).__eq__('stock_margin'):
        log.info('查看融资融券账户相关相关信息(更多请见API-对象-SubPortfolio)：')
        log.info('净资产：', p.net_value)
        log.info('总负债：', p.total_liability)
        log.info('融资负债：', p.cash_liability)
        log.info('融券负债：', p.sec_liability)
        log.info('利息总负债：', p.interest)
        log.info('可用保证金：', p.available_margin)
        log.info('维持担保比例：', p.maintenance_margin_rate)
    elif str(p.type).__eq__('futures'):
        log.info('风险度：', p.margin)
    log.info('##############################################################')
    pass


########################## 自定义函数 #################################

# 分钟级别的回测，每隔多长时间执行一下策略
def minute_execution_interval():
    g.run_num += 1
    if g.run_num != 30:  # 如果这次运行的次数不是30,打断此次运行
        return False
    else:
        g.run_num = 0  # 条件满足,计数器归零,继续后边的代码
        return True


# 主力合约改变，平仓
# 如果期货标的改变，重置参数
def reset_feture():
    # 如果期货标的改变，重置参数
    if g.last_future == None:
        g.last_future = g.future
    elif g.last_future != g.future:
        # log.warn("主力合约改变，平仓！ last_future %s； cur_future%s" % (g.last_future, g.future))
        if g.position == -1:
            order_target(g.last_future, 0, side='short')
            g.position == 0
        elif g.position == 1:
            order_target(g.last_future, 0, side='long')
            g.position == 0
        g.last_future = g.future
        re_set()


# 止损函数---跟随止损
def stop_loss(context, future):
    # 获取当前的期货价格
    close_price = get_cur_price(context, future)
    # 判断今日是否出现最高价
    if g.position != 0:
        set_price_mark(context, future)  # 记录 建仓价格
    else:
        return
    # 得到止损信号
    signal = get_risk_signal(context, future, close_price)

    # 止损平仓
    if signal:
        log.info("stop_loss:！ future is %s； close_price is %s" % (future, close_price))
        log.info("stop_loss:！ signal is %s" % (signal))
        order_target(future, 0, side='short')
        order_target(future, 0, side='long')
        if context.portfolio.positions[future].total_amount == 0 and context.portfolio.short_positions[future].total_amount == 0:
            log.info("stop_loss 止损平仓!")
            g.position = 0
            g.price_mark = 0
            # 重新初始化参数
            re_set()
            return True
    else:
        return False


# 多头：若当前价格低于前out_date天的收盘价的最小值, 则卖掉所有持仓
# 空头：若当前价格大于前out_date天的收盘价的最大值, 则卖掉所有持仓
def stop_loss_2(context, future, out_date):
    # 获取当前的期货价格
    current_price = get_cur_price(context, future)
    # log.info("stop_loss_2:！ future is %s； current_price is %s； position is %s" % (future, current_price, g.position))
    # Function for leaving the market
    price = attribute_history(future, out_date, '30m', ('close'))
    # log.info("stop_loss_2:！ current_price is %s； min close price is %s" % (current_price, min(price['close']))
    # log.info("stop_loss_2:！ current_price is %s； min close price is %s" % (current_price, max(price['close']))
    # 检测否需要多头平仓
    if g.position == 1:
        # 若当前价格低于前out_date天的收盘价的最小值, 则卖掉所有持仓
        if current_price < min(price['close']):
            order_target(future, 0, side='short')
            order_target(future, 0, side='long')
            log.info("stop_loss_2 多头 止损平仓! %s out_date-days min(price['close'] %s" % (out_date, min(price['close'])))
            if context.portfolio.positions[future].total_amount == 0 and context.portfolio.short_positions[future].total_amount == 0:
                g.position = 0
                g.price_mark = 0
                # 重新初始化参数
                re_set()
                return True
            else:
                log.info("stop_loss_2 多头 止损平仓!失败")

    # 检测否需要空头平仓
    elif g.position == -1:
        if current_price > max(price['close']):
            order_target(future, 0, side='short')
            order_target(future, 0, side='long')
            log.info("stop_loss_2 空头 止损平仓! %s out_date-days max(price['close']) %s" % (out_date, max(price['close'])))
            if context.portfolio.positions[future].total_amount == 0 and context.portfolio.short_positions[future].total_amount == 0:
                g.position = 0
                g.price_mark = 0
                # 重新初始化参数
                re_set()
                return True
            else:
                log.info("stop_loss_2 空头 止损平仓!失败")

    return False


# 入市函数，里面包含入市的逻辑策略实现，并区分是多头入市，还是空头入市
# 入参：
# 出参：
def market_in(context, future, in_date, ATR):
    price_list = attribute_history(future, in_date + 1, '30m', ['close', 'high', 'low'])
    # 如果没有数据，返回
    if len(price_list) == 0:
        return

    close_price = price_list['close'].iloc[-1]

    # 没有开过仓，则判断开仓信息
    if g.position == 0:
        ## 开仓
        # 得到开仓信号
        open_signal = check_break(price_list, close_price, in_date)
        log_info_str = 'market_in:！ future is %s；position is %s； close_price is %s； open_signal is %s' % (future, g.position, close_price, open_signal)
        # 多头开仓
        if open_signal == 1 and g.position != 1:
            log.info(log_info_str, '多头开仓')
            market_in_long(context, future, ATR, close_price)
        # 空头开仓
        elif open_signal == -1 and g.position != -1:
            log.info(log_info_str, '空头开仓')
            market_in_short(context, future, ATR, close_price)


# 加仓函数
def market_add(context, future, in_date, ATR):
    # log.info("market_add:！ future is %s； position is %s; ATR is %s" % (future, g.position, ATR))
    if g.position != 0:
        price_list = attribute_history(future, in_date + 1, '30m', ['close', 'high', 'low'])
        # 如果没有数据，返回
        if len(price_list) == 0:
            return

        close_price = price_list['close'].iloc[-1]

        # 获取是否加仓的信号
        signal = get_next_signal(close_price, g.last_price, ATR, g.position)

        # 判断加仓且持仓没有达到上限
        if signal == 1 and g.add_time < g.limit_unit:
            log.info("market_add:！ future is %s； close_price is %s" % (future, close_price))
            log.info("market_add:！ future is %s； signal is %s; add_time is %s" % (future, signal, g.add_time))
            market_add_internal(context, future, ATR, close_price)


# 止损函数
# (price <= last_price - 2*ATR and position==1) or (price >= last_price + 2*ATR and position==-1):  # 多头止损或空头止损
def market_stop_loss(context, future, out_date, ATR):
    if g.position != 0:
        price_list = attribute_history(future, out_date + 1, '30m', ['close', 'high', 'low'])
        # 如果没有数据，返回
        if len(price_list) == 0:
            return

        close_price = price_list['close'].iloc[-1]
        # log.info("market_stop_loss:！ future is %s； close_price is %s" % (future, close_price))

        # 获取是否止损的信号
        signal = get_next_signal(close_price, g.last_price, ATR, g.position)

        # 判断平仓止损
        if signal == -1:
            log.info("market_stop_loss:！ future is %s； signal is %s; add_time is %s" % (future, signal, g.add_time))
            close_postion(context, future, close_price)
            # 重新初始化参数
            re_set()


def get_ATR_N(context, future, number_days):
    price_list = attribute_history(future, number_days + 1, '30m', ['close', 'high', 'low'])
    # 如果没有数据，返回
    if len(price_list) == 0:
        return

    # 计算ATR
    ATR = get_ATR(price_list, number_days)

    # log.info("get_ATR_N:！ future is %s； ATR is %s; number_days is %s" % (future, ATR, number_days))

    return ATR


def get_ATR(price_list, T):
    TR_list = [max(price_list['high'].iloc[i] - price_list['low'].iloc[i], abs(price_list['high'].iloc[i] - price_list['close'].iloc[i - 1]),
                   abs(price_list['close'].iloc[i - 1] - price_list['low'].iloc[i])) for i in range(1, T + 1)]
    ATR = np.array(TR_list).mean()

    # log.info("get_ATR:！ ATR is %s； T is %s" % (ATR, T))
    return ATR


# 获取当前期货的价格
# 此处为昨天的收盘价
def get_cur_price(context, future):
    price_list = attribute_history(future, 2, '30m', ['close', 'high', 'low'])
    # 如果没有数据，返回
    if len(price_list) == 0:
        return

    close_price = price_list['close'].iloc[-1]

    # log.info("get_cur_price:！ future is %s； cur_price is %s " % (future, close_price))

    return close_price


# 多头入市：
# 决定系统1、系统2是否应该入市，更新系统1和系统2的突破价格
# 海龟将所有资金分为2部分：一部分资金按系统1执行，一部分资金按系统2执行
# 输入：
# 输出：none
def market_in_long(context, future, ATR, close_price):
    # log.info("market_in_long:！ future is %s； ATR is %s; close_price is %s; position is %s" % (future, ATR, close_price, g.position))

    # 检测否需要空头平仓
    if g.position == -1:
        order_target(future, 0, side='short')
        if context.portfolio.short_positions[future].total_amount == 0:
            g.price_mark = 0
            # 重新初始化参数
            re_set()
            log.info('空头平仓成功:', context.current_dt, future)
            log.info('----------------------------------------------------------')
    # 多头开仓
    g.unit = get_unit(context.portfolio.total_value, ATR, g.future_index)
    order(future, g.unit, side='long')
    if context.portfolio.positions[future].total_amount > 0:
        g.position = 1
        g.price_mark = context.portfolio.long_positions[future].price
        log.info('多头建仓成功:', context.current_dt, future, g.unit)
        log.info('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        # g.add_time = 1
        g.last_price = close_price
        g.last_future = future


# 空头入市：
# 决定系统1、系统2是否应该入市，更新系统1和系统2的突破价格
# 海龟将所有资金分为2部分：一部分资金按系统1执行，一部分资金按系统2执行
# 输入：
# 输出：none
def market_in_short(context, future, ATR, close_price):
    # log.info("market_in_short:！ future is %s； ATR is %s; close_price is %s; position is %s" % (future, ATR, close_price, g.position))

    # 检测否需要多头平仓
    if g.position == 1:
        order_target(future, 0, side='long')
        if context.portfolio.positions[future].total_amount == 0:
            g.price_mark = 0
            # 重新初始化参数
            re_set()
            log.info('多头平仓成功:', context.current_dt, future)
            log.info('----------------------------------------------------------')
    # 空头开仓
    g.unit = get_unit(context.portfolio.total_value, ATR, g.future_index)
    order(future, g.unit, side='short')
    if context.portfolio.short_positions[future].total_amount > 0:
        g.position = -1
        g.price_mark = context.portfolio.short_positions[future].price  # 建仓成本 trade price+commission
        log.info('空头建仓成功:', context.current_dt, future, g.unit)
        log.info('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        # g.add_time = 1
        g.last_price = close_price
        g.last_future = future


# 加仓函数：需要考虑是多头加仓还是空头加仓
# (price >= last_price + 0.5*ATR and position==1) or (price <= last_price - 0.5*ATR and position==-1)
def market_add_internal(context, future, ATR, close_price):
    g.unit = get_unit(context.portfolio.total_value, ATR, g.future_index)

    log.info("market_add_internal:！ future is %s； ATR is %s; close_price is %s; position is %s; unit is %s" % (future, ATR, close_price, g.position, g.unit))

    # 多头加仓
    if g.position == 1:
        order(future, g.unit, side='long')
        g.price_mark = context.portfolio.long_positions[future].price
        log.info('多头加仓成功:', context.current_dt, future, g.unit)
        g.last_price = close_price
        g.add_time += 1
    # 空头加仓
    elif g.position == -1:
        order(future, g.unit, side='short')
        g.price_mark = context.portfolio.short_positions[future].price
        log.info('空头加仓成功:', context.current_dt, future, g.unit)
        g.last_price = close_price
        g.add_time += 1


# 平仓函数:平仓止损
# (price <= last_price - 2*ATR and position==1) or (price >= last_price + 2*ATR and position==-1)
# TODO 这部分的代码可以优化一下的，分阶段平仓
def close_postion(context, future, close_price):
    if g.position == 0:
        return
    log.info("close_postion:！ future is %s； close_price is %s; position is %s" % (future, close_price, g.position))

    # 多头平仓
    if g.position == 1:
        Order_state = order_target(future, 0, side='long')
        if Order_state:
            g.price_mark = 0
            g.position = 0
            log.info('close_postion:！多头止损成功:', context.current_dt, future)
            log.warn("close_postion:！多头止损成功:！ price is %s； last price is %s" % (close_price, g.last_price))
            log.info('----------------------------------------------------------')
        else:
            log.info('close_postion:！ 多头止损失败:', context.current_dt, future)
    # 空头平仓
    elif g.position == -1:
        Order_state = order_target(future, 0, side='short')
        if Order_state:
            g.price_mark = 0
            g.position = 0
            log.info('close_postion:！ 空头止损成功:', context.current_dt, future)
            log.warn("close_postion:！ 空头止损成功:！ price is %s； last price is %s" % (close_price, g.last_price))
            log.info('----------------------------------------------------------')
        else:
            log.info('close_postion:！ 空头止损失败:', context.current_dt, future)


# 重置参数
def re_set():
    # 每次交易unit数目
    g.unit = 0
    # 加仓次数
    g.add_time = 0
    # 持仓状态
    g.position = 0


# 检查是否突破奇安通道时间窗口
def check_break(price_list, price, T):
    up = max(price_list['high'].iloc[-T - 1:-2])
    down = min(price_list['low'].iloc[-T - 1:-2])
    log.info('current-close %s, %s days, max high %s,min low %s' % (price, T, up, down))
    if price > up:
        return 1
    elif price < down:
        return -1
    else:
        return 0


# 获取下一个信号：加仓或止损
def get_next_signal(price, last_price, ATR, position):
    # log.info("get_next_signal:！ price is %s； last_price is %s; ATR is %s; position is %s" % (price, last_price, ATR, position))

    if (price >= last_price + 0.5 * ATR and position == 1) or (price <= last_price - 0.5 * ATR and position == -1):  # 多头加仓或空头加仓
        return 1
    elif (price <= last_price - 2 * ATR and position == 1) or (price >= last_price + 2 * ATR and position == -1):  # 多头止损或空头止损
        return -1
    else:
        return 0


# 获取当前出于什么仓位情况：0为未持仓，1为持多，-1为持空
def get_position(context):
    try:
        tmp = context.portfolio.positions.keys()[0]
        if not context.portfolio.long_positions[tmp].total_amount and not context.portfolio.short_positions[tmp].total_amount:
            return 0
        elif context.portfolio.long_positions[tmp].total_amount:
            return 1
        elif context.portfolio.short_positions[tmp].total_amount:
            return -1
        else:
            return 0
    except:
        return 0


# 获取风险信号，根据该信号看做什么处理
def get_risk_signal(context, future, close_price):
    # log.info("get_risk_signal:！ future is %s； close_price is %s; price_mark is %s; position is %s" % (future, close_price, g.price_mark, g.position))

    if g.position == -1:
        if close_price >= 1.05 * g.price_mark:
            log.info("空头仓位止损，时间： " + str(context.current_dt))
            log.warn("空头仓位止损: price is %s； price_mark is %s" % (context.portfolio.short_positions[future].price, g.price_mark))
            return True
        else:
            return False
    elif g.position == 1:
        if close_price <= 0.95 * g.price_mark:
            log.info("多头仓位止损，时间： " + str(context.current_dt))
            log.warn("多头仓位止损: price is %s； price_mark is %s" % (context.portfolio.long_positions[future].price, g.price_mark))
            return True
        else:
            return False


# 空仓记录最低价
# 多仓记录最高价
def set_price_mark(context, future):
    if g.position == -1:
        g.price_mark = min(context.portfolio.short_positions[future].price, g.price_mark)
    elif g.position == 1:
        g.price_mark = max(context.portfolio.long_positions[future].price, g.price_mark)


# 获取单位购买的头寸
def get_unit(cash, ATR, symbol):
    future_coef_list = {'A': 10, 'AG': 15, 'AL': 5, 'AU': 1000,
                        'B': 10, 'BB': 500, 'BU': 10, 'C': 10,
                        'CF': 5, 'CS': 10, 'CU': 5, 'ER': 10,
                        'FB': 500, 'FG': 20, 'FU': 50, 'GN': 10,
                        'HC': 10, 'I': 100, 'IC': 1, 'IF': 300,
                        'IH': 1, 'J': 100, 'JD': 5, 'JM': 60,
                        'JR': 20, 'L': 5, 'LR': 10, 'M': 10,
                        'MA': 10, 'ME': 10, 'NI': 1, 'OI': 10,
                        'P': 10, 'PB': 5, 'PM': 50, 'PP': 5,
                        'RB': 10, 'RI': 20, 'RM': 10, 'RO': 10,
                        'RS': 10, 'RU': 10, 'SF': 5, 'SM': 5,
                        'SN': 1, 'SR': 10, 'T': 10000, 'TA': 5,
                        'TC': 100, 'TF': 10000, 'V': 5, 'WH': 20,
                        'WR': 10, 'WS': 50, 'WT': 10, 'Y': 10,
                        'ZC': 100, 'ZN': 5}
    return (cash * 0.01 / ATR) / future_coef_list[symbol]


# 获取当前可用现金可以购买的期货手数
def get_cash_can_bug(cash, symbol, current_price):
    future_coef_list = {'A': 10, 'AG': 15, 'AL': 5, 'AU': 1000,
                        'B': 10, 'BB': 500, 'BU': 10, 'C': 10,
                        'CF': 5, 'CS': 10, 'CU': 5, 'ER': 10,
                        'FB': 500, 'FG': 20, 'FU': 50, 'GN': 10,
                        'HC': 10, 'I': 100, 'IC': 1, 'IF': 300,
                        'IH': 1, 'J': 100, 'JD': 5, 'JM': 60,
                        'JR': 20, 'L': 5, 'LR': 10, 'M': 10,
                        'MA': 10, 'ME': 10, 'NI': 1, 'OI': 10,
                        'P': 10, 'PB': 5, 'PM': 50, 'PP': 5,
                        'RB': 10, 'RI': 20, 'RM': 10, 'RO': 10,
                        'RS': 10, 'RU': 10, 'SF': 5, 'SM': 5,
                        'SN': 1, 'SR': 10, 'T': 10000, 'TA': 5,
                        'TC': 100, 'TF': 10000, 'V': 5, 'WH': 20,
                        'WR': 10, 'WS': 50, 'WT': 10, 'Y': 10,
                        'ZC': 100, 'ZN': 5}
    return (cash) / (future_coef_list[symbol] * current_price)


########################## 获取期货合约信息，请保留 #################################
# 获取金融期货合约到期日
def get_CCFX_end_date(future_code):
    # 获取金融期货合约到期日
    return get_security_info(future_code).end_date


########################## 获取期货合约信息，请保留 #################################
# 获取当天时间正在交易的期货主力合约
def get_future_code(symbol):
    future_code_list = {'A': 'A9999.XDCE', 'AG': 'AG9999.XSGE', 'AL': 'AL9999.XSGE', 'AU': 'AU9999.XSGE',
                        'B': 'B9999.XDCE', 'BB': 'BB9999.XDCE', 'BU': 'BU9999.XSGE', 'C': 'C9999.XDCE',
                        'CF': 'CF9999.XZCE', 'CS': 'CS9999.XDCE', 'CU': 'CU9999.XSGE', 'ER': 'ER9999.XZCE',
                        'FB': 'FB9999.XDCE', 'FG': 'FG9999.XZCE', 'FU': 'FU9999.XSGE', 'GN': 'GN9999.XZCE',
                        'HC': 'HC9999.XSGE', 'I': 'I9999.XDCE', 'IC': 'IC9999.CCFX', 'IF': 'IF9999.CCFX',
                        'IH': 'IH9999.CCFX', 'J': 'J9999.XDCE', 'JD': 'JD9999.XDCE', 'JM': 'JM9999.XDCE',
                        'JR': 'JR9999.XZCE', 'L': 'L9999.XDCE', 'LR': 'LR9999.XZCE', 'M': 'M9999.XDCE',
                        'MA': 'MA9999.XZCE', 'ME': 'ME9999.XZCE', 'NI': 'NI9999.XSGE', 'OI': 'OI9999.XZCE',
                        'P': 'P9999.XDCE', 'PB': 'PB9999.XSGE', 'PM': 'PM9999.XZCE', 'PP': 'PP9999.XDCE',
                        'RB': 'RB9999.XSGE', 'RI': 'RI9999.XZCE', 'RM': 'RM9999.XZCE', 'RO': 'RO9999.XZCE',
                        'RS': 'RS9999.XZCE', 'RU': 'RU9999.XSGE', 'SF': 'SF9999.XZCE', 'SM': 'SM9999.XZCE',
                        'SN': 'SN9999.XSGE', 'SR': 'SR9999.XZCE', 'T': 'T9999.CCFX', 'TA': 'TA9999.XZCE',
                        'TC': 'TC9999.XZCE', 'TF': 'TF9999.CCFX', 'V': 'V9999.XDCE', 'WH': 'WH9999.XZCE',
                        'WR': 'WR9999.XSGE', 'WS': 'WS9999.XZCE', 'WT': 'WT9999.XZCE', 'Y': 'Y9999.XDCE',
                        'ZC': 'ZC9999.XZCE', 'ZN': 'ZN9999.XSGE', 'IH': '000016.XSHG', 'IF': '000300.XSHG', 'IC': '000905.XSHG'}
    try:
        return future_code_list[symbol]
    except:
        return 'WARNING: 无此合约'


########################## 自动移仓换月函数 #################################
def position_auto_switch(context, pindex=0, switch_func=None, callback=None):
    """
    期货自动移仓换月。默认使用市价单进行开平仓。
    :param context: 上下文对象
    :param pindex: 子仓对象
    :param switch_func: 用户自定义的移仓换月函数.
        函数原型必须满足：func(context, pindex, previous_dominant_future_position, current_dominant_future_symbol)
    :param callback: 移仓换月完成后的回调函数。
        函数原型必须满足：func(context, pindex, previous_dominant_future_position, current_dominant_future_symbol)
    :return: 发生移仓换月的标的。类型为列表。
    """
    import re
    subportfolio = context.subportfolios[pindex]
    symbols = set(subportfolio.long_positions.keys()) | set(subportfolio.short_positions.keys())
    switch_result = []
    for symbol in symbols:
        match = re.match(r"(?P<underlying_symbol>[A-Z]{1,})", symbol)
        if not match:
            raise ValueError("未知期货标的：{}".format(symbol))
        else:
            dominant = get_dominant_future(match.groupdict()["underlying_symbol"])
            cur = get_current_data()
            symbol_last_price = cur[symbol].last_price
            dominant_last_price = cur[dominant].last_price
            if dominant > symbol:
                for p in (subportfolio.long_positions.get(symbol, None), subportfolio.short_positions.get(symbol, None)):
                    if p is None:
                        continue
                    if switch_func is not None:
                        switch_func(context, pindex, p, dominant)
                    else:
                        amount = p.total_amount
                        # 跌停不能开空和平多，涨停不能开多和平空。
                        if p.side == "long":
                            symbol_low_limit = cur[symbol].low_limit
                            dominant_high_limit = cur[dominant].high_limit
                            if symbol_last_price <= symbol_low_limit:
                                log.warning("标的{}跌停，无法平仓。移仓换月取消。".format(symbol))
                                continue
                            elif dominant_last_price >= dominant_high_limit:
                                log.warning("标的{}涨停，无法开仓。移仓换月取消。".format(symbol))
                                continue
                            else:
                                log.info("进行移仓换月：({0},long) -> ({1},long)".format(symbol, dominant))
                                order_target(symbol, 0, side='long')
                                order_target(dominant, amount, side='long')
                                switch_result.append({"before": symbol, "after": dominant, "side": "long"})
                            if callback:
                                callback(context, pindex, p, dominant)
                        if p.side == "short":
                            symbol_high_limit = cur[symbol].high_limit
                            dominant_low_limit = cur[dominant].low_limit
                            if symbol_last_price >= symbol_high_limit:
                                log.warning("标的{}涨停，无法平仓。移仓换月取消。".format(symbol))
                                continue
                            elif dominant_last_price <= dominant_low_limit:
                                log.warning("标的{}跌停，无法开仓。移仓换月取消。".format(symbol))
                                continue
                            else:
                                log.info("进行移仓换月：({0},short) -> ({1},short)".format(symbol, dominant))
                                order_target(symbol, 0, side='short')
                                order_target(dominant, amount, side='short')
                                switch_result.append({"before": symbol, "after": dominant, "side": "short"})
                                if callback:
                                    callback(context, pindex, p, dominant)
    return switch_result
