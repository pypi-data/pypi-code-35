#!/usr/bin/python
# coding:utf-8

from tornado.options import options
import config
import pymysql
from DBUtils.PooledDB import PooledDB
from contextlib import contextmanager

# 数据库连接池
pool = None


def init():
    if not config.Mysql['active']:
        return

    env = options.env

    global pool
    if pool is None:
        config_opt = {
            'host': config.Mysql[env]['host'],
            'port': config.Mysql[env]['port'],
            'user': config.Mysql[env]['user'],
            'password': config.Mysql[env]['pwd'],
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor
        }
        pool = PooledDB(pymysql, **config_opt)


@contextmanager
def create_cursor():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        yield conn, cursor
    finally:
        cursor.close()
        conn.close()


