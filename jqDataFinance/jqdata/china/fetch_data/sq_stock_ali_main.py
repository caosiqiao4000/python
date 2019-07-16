# encoding:utf-8

## 只要import就会执行
# import jqdata.china.fetch_data.FetchChinaMarketByJq as fetch_china_market
# import jqdata.china.fetch_data.pingAnFutrueDataByJq as fetch_pingan_futrue
import jqdata.china.fetch_data.tomcat_insurment_life_sort as bar_life_analyze

class Csq_stock_dream():
    def __init__(self):
        print("-------- class Csq_stock_dream init ------------------")
        pass

    def fetch_all_bar(self):
        # 从 聚宽 取期货和股票的bar数据
        # fetch_china_market.start_fetch()
        # fetch_pingan_futrue.start_fetch()
        print("fetch_all_bar is call")
        pass

    def analyze_stock_life(self):
        print("analyze_stock_life is call")
        # bar_life_analyze.start_analyze()


if __name__ == '__main__':
    stock_dream = Csq_stock_dream
    # 从 聚宽 取期货和股票的bar数据
    # stock_dream.fetch_all_bar()
    # 依据 java 计算好的周期 统计其中的逆大周期bar的反转概率   可以是 月,周,日
    stock_dream.analyze_stock_life

    pass
