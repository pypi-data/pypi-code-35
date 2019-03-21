# coding=utf-8

import config
from webmother.http_handler import catalog_handler as h

base = '{}/{}/catalog'.format(config.VER, config.PLATFORM)
routes = [
    # 分类节点的增删改查，增时参数会解析成父节点ID，删改查时则解析成本节点
    (rf"/{base}/([a-f0-9]*)", h.CatalogHandler),
    # 分类节点的状态操作
    (rf"/{base}/([a-f0-9]*)/do/(\w*)", h.StatusHandler),

    # 查询子节点
    (rf"/{base}/([a-f0-9]*)/children", h.ChildrenHandler),

    # 移动节点
    (rf"/{base}/([a-f0-9]*)/move/([a-f0-9]*)", h.MovingHandler),
]
