#coding=utf8

from tjquant import client_sqlite as client
import sqlite3
import time
# 取消下面两行的注释，并把连接的路径设置为本地的数据库文件位置。
# client.conn=sqlite3.connect('demo.db')
# client.cursor=client.conn.cursor()

client.GetStkPrice('SH600000.stk',0,99999999999999)
print time.strftime('%Y:%m:%d %H:%M:%S')
# client.GetStkPriceAll(20110101000000)
# print time.strftime('%Y:%m:%d %H:%M:%S')

stocklist = []
codes = client.GetStkCodeST22047()
for code in codes:
    if (code[2:4] == '00' or code[2:4] == '60' or code[2:4] == '30') and (code[0:2] == 'SZ' or code[0:2] == 'SH'):
        stocklist.append(code)
print stocklist.__len__()
print time.strftime('%Y:%m:%d %H:%M:%S')
for line in stocklist:
    client.GetStkPrice(line,0,99999999999999)
print time.strftime('%Y:%m:%d %H:%M:%S')
res = client.GetStkPriceGroup(stocklist[:100],0,99999999999999)
print time.strftime('%Y:%m:%d %H:%M:%S')
#stocklist=stocklist[:10]