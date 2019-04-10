# -*- coding: utf-8 -*-
# @Time    : 2019-04-04 15:39
# @Author  : zhoucl
# @Email   : zhoucl09164@hundsun.com
# @File    : test-sqlite.py
# @Software: PyCharm

import sqlite3

if __name__ == "__main__":
    db_file = r"e:\测试开发转型\05数据库操作+爬虫\sqlite-dll-win64-x64-3270200\mydb.db"
    #第一步 建立连接，获取连接对象
    conn = sqlite3.connect(db_file) #文件不存在会自动创建
    print("Opened database successfully")

    #第二步 通过连接对象，获取游标对象
    cur = conn.cursor()

    #第三步 执行查询语句
    cur.execute("select * from test")

    #第四步 获取结果
    for row in cur.fetchall():
        print("id = {}|name = {}".format(row[0],row[1]))

    #insert
    #cur.execute("insert into test(id,name) values(1,'zhouzhou');")
    #事务提交
    #conn.commit()

    # cur.execute("select * from test")
    # print(cur.rowcount)
    # for row in cur.fetchall():
    #     print("id = {}|name = {}".format(row[0], row[1]))


    #最后关闭资源
    cur.close()
    conn.close()

    #关闭之后 不能继续操作！
    # cur.execute("select * from test")
    # print(cur.rowcount)
    # for row in cur.fetchall():
    #     print("id = {}|name = {}".format(row[0], row[1]))


