# -*- coding: utf-8 -*-
# @Time    : 2019-04-04 15:59
# @Author  : zhoucl
# @Email   : zhoucl09164@hundsun.com
# @File    : test-mysql.py
# @Software: PyCharm

import pymysql

if __name__ == "test-mysql":
    # 第一步 建立连接，获取连接对象
    conn = pymysql.Connect(host="10.20.18.191", port=10080, user="test05", passwd="test05", db="database05", charset="utf8")
    print("Opened database successfully")

    # 第二步 通过连接对象，获取游标对象
    cur = conn.cursor()

    # 第三步 执行查询语句
    cur.execute("select * from test")

    # 第四步 获取结果
    for row in cur.fetchall():
        print("id = {}|name = {}".format(row[0], row[1]))

    # insert
    # cur.execute("insert into test(id,name) values(1,'zhouzhou');")
    # 事务提交
    # conn.commit()

    # cur.execute("select * from test")
    # print(cur.rowcount)
    # for row in cur.fetchall():
    #     print("id = {}|name = {}".format(row[0], row[1]))

    # 最后关闭资源
    cur.close()
    conn.close()

    # 关闭之后 不能继续操作！
    # cur.execute("select * from test")
    # print(cur.rowcount)
    # for row in cur.fetchall():
    #     print("id = {}|name = {}".format(row[0], row[1]))
