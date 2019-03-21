# coding=utf-8

import ucenter

from webmother.db import mongo
from webmother import routes


def init(app):

    # 初始化UCenter
    ucenter.init(app)

    # 初始化本系统数据库
    mongo.init()

    # 加载路由模块
    app.load_routes(routes)
