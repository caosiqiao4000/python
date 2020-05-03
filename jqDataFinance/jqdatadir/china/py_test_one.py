# from jqdatadir import macro
from jqdatasdk import *
import numpy as np
import pandas as pd

# q = query(macro.MAC_MONEY_SUPPLY_YEAR
#           ).limit(100)
# df = macro.run_query(q)
# print(df)

# list_down = pd.DataFrame(
#     {"连续下跌天数": np.arange(1, 11), '发生次数': np.zeros(10, dtype=int), '趋势幅度中位数': np.zeros(10, dtype=float)}).set_index(
#     "连续下跌天数")
# print(list_down)
# # list_down[5,"发生次数"] = list_down[5,"发生次数"]+1
# print(list_down.loc[2])
# list_down.loc[2,"发生次数"] = list_down.loc[2,"发生次数"] + 1
# print(list_down)

df2 = pd.DataFrame({'A': 5.,
                    'B': pd.Timestamp('20130102'),
                    'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                    'D': np.array([3] * 4, dtype='int32'),
                    'E': pd.Categorical(["test", "train", "test", "train"]),
                    'F': 'foo',
                    'G': np.arange(1, 5)}).set_index("A")
# print(df2, "\n---------------------------------")
# print(df2[0:3],"\n---------------------------------")
# print(df2.loc[5],"\n---------------------------------")
# print(df2['G'].iloc[0:2], "\n---------------------------------")
# print(df2['G'].iloc[2 - 0:4].sum(), "\n---------------------------------")
# df2.loc[:,["add"]] = df2['D']+df2['G']
# df2["add"] = (df2['D']+df2['G'])/df2['D']
# df2.loc[:,"H"] = df2.loc[:,'G']
print(df2)
# bar_path = r'D:\\ideaWorkspace\python\jqJson'
# path_excel = '%s\\series\\csq_test_analyze.xlsx' % (bar_path)
# with pd.ExcelWriter(path_excel) as writer:  # doctest: +SKIP
#     startrow_excel = 0
#     for x in range(0, 4):
#         df3 = df2.copy()
#         df4 = df2.copy()
#         df4 = df4.drop('C', axis=1)
#         df4.loc[:, "H"] = df2.loc[:, 'G'] + 1
#         print("---------- df4 \n", df4)
#
#         sheet_name_e = 'data_df2_%s' % x
#         print(x, "----", sheet_name_e)
#         df2.to_excel(writer, sheet_name=sheet_name_e)
#         startrow_excel += len(df2) + 2
#         df3.to_excel(writer, sheet_name=sheet_name_e, startrow=startrow_excel)
#         startrow_excel += len(df3) + 2
#         df4.to_excel(writer, sheet_name=sheet_name_e, startrow=startrow_excel)
#         startrow_excel += len(df4) + 2
#         writer.save()

# df1=pd.DataFrame({'key':['a','b','c'],'data1':[1,2,3]})
# df2=pd.DataFrame({'key':['e','d','f'],'data2':[4,5,6]})
# df3=pd.merge(df1,df2)
# print(df3)


# str_appear_num = ("d发生次数", "w发生次数", "m发生次数")
# print(str_appear_num[0])
# ten_zeros = np.zeros(10, dtype=float)
# df_up = pd.DataFrame({"d连续上涨天数": np.arange(1, 11), str_appear_num[0]: np.arange(1, 11)})
# print(df_up)

# print(np.arange(-1, -11, step=-1))
# list = [np.arange(5,222,step=2)]
# print(type(list))
# print(list.copy())
