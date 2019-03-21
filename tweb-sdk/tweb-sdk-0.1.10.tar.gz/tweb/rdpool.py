#!/usr/bin/python
# coding:utf-8

import redis
import config
from tornado.options import options

# Redis客户端对象
rds = None


def init():
    if not config.Redis['active']:
        return

    global rds

    env = options.env

    if rds is None:
        rds = redis.Redis(host=config.Redis[env]['host'], port=config.Redis[env]['port'], decode_responses=True)


