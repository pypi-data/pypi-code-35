# coding=utf-8

import config
from webmother.http_handler import mine_handler as h

base = '{}/{}/mine'.format(config.VER, config.PLATFORM)
routes = [
    # 获取我的组织身份列表
    (rf"/{base}/identities", h.QueryIdentitiesHandler),

    # 获取我的VIP身份列表
    (rf"/{base}/vip", h.GetVipHandler),
]
