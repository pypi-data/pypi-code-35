# -*- coding: utf-8 -*-

# @Date    : 2019-03-30
# @Author  : Peng Shiyu

"""
利用上下文管理器管理MySQL的链接对象
https://blog.csdn.net/mouday/article/details/88873764
"""

from __future__ import unicode_literals, print_function
import MySQLdb


class DataBase(object):
    def __init__(self, hostname, username, password, database, port, charset='utf8'):
        self.conn = MySQLdb.Connect(
            host=hostname,
            user=username,
            passwd=password,
            db=database,
            port=port,
            charset=charset,
            autocommit=True
        )
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()


def main():
    database = {
        "hostname": "127.0.0.1",
        "username": "root",
        "password": "123456",
        "database": "demo",
        "port": 3306
    }

    with DataBase(**database) as cursor:
        sql = "select name, age from student"
        cursor.execute(sql)
        rows = cursor.fetchall()

    for name, age in rows:
        print("name: {} age: {}".format(name, age))
    """
    name: jimi age: 23
    name: jack age: 23
    name: tom age: 23
    name: tom age: 23
    """


if __name__ == '__main__':
    main()
