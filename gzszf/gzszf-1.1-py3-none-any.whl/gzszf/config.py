# -*- coding: utf-8 -*- 
# @Time : 2019/4/4 16:13 
# @Author : Allen 
# @Site :
import os

JVMPath = ''
guidance_jar_path = os.path.dirname(os.path.abspath(__file__)) + r'\resource\guidance.jar'
# 数据配置
db_config = {
    'user': "root",
    'password': "gzxiaoi",
    'host': "192.168.160.36",
    'port': "3306",
    'name': "gzszf_db",
}

# 参数配置
is_bool = True  # 是否需要指定下面时间，False则是当天时间
strStartCTime = '2019-03-12'  # 开始时间
strEndCTime = '2019-04-08'  # 结束时间
