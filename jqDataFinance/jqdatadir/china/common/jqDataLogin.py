from jqdatasdk import *  # 平台给的包，务必加载，地址：https://github.com/JoinQuant/jqdatasdk/archive/master.zip

#https://www.joinquant.com/help/api/help?name=JQData#%E7%99%BB%E5%BD%95JQData
def login():
     return  auth('18680538805', 'zzzz00000000')  # 依次输入账号、密码，链接到平台数据库
    # 查询是否连接成功






login()
is_auth = is_auth()
print(is_auth)
# 查询当日剩余可调用数据条数
count = get_query_count()
print(count)
# qdatadir/china/common/jqDataLogin.py
# auth('18680538805', 'zzzz00000000')  # 依次输入账号、密码，链接到平台数据库