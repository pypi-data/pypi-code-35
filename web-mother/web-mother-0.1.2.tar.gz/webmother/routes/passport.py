# coding=utf-8

import config
from webmother.http_handler import passport_handler as h

base = '{}/{}/passport'.format(config.VER, config.PLATFORM)
routes = [

    # 获取分类节点可以授权的空白模板
    (rf"/{base}/catalog/([a-f0-9]*)/tpl", h.PassportTplHandler),

    # 分类圈定的资源向特定组织的颁发许可证（增删改查）
    (rf"/{base}/catalog/([a-f0-9]*)/org/([a-f0-9]*)", h.PassportHandler),

    # 查询针对分类圈定的资源颁发了哪些许可证，都有些什么权限
    (rf"/{base}/catalog/([a-f0-9]*)/list", h.PassportsHandler),
]
