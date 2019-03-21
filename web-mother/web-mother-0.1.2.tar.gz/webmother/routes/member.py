# coding=utf-8

import config
from webmother.http_handler import member_handler as h

base = '{}/{}/member'.format(config.VER, config.PLATFORM)
routes = [

    # 组织成员的增删改查
    (rf"/{base}/org/([a-f0-9]*)/user/([@\\.\w]+)", h.MemberHandler),

    # 获取组织的成员列表
    (rf"/{base}/org/([a-f0-9]*)/list", h.MembersHandler)
]
