# coding=utf-8

from tweb import base_handler, myweb
from tornado import gen
from webmother.service.async_wrap import ctrl_mine


class QueryIdentitiesHandler(base_handler.BaseHandler):
    """
    查询我的组织身份列表
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self):
        appid = self.get_argument('appid')
        t = self.get_argument('type', '0')
        member_type = int(t) if t.isdecimal() else 0

        uid = self.request.headers.get('x-user-id')
        access_token = self.request.headers.get('x-access-token')

        array = yield ctrl_mine.query_identities(appid, uid, access_token, member_type=member_type)
        return self.write({'list': array})


class GetVipHandler(base_handler.BaseHandler):
    """
    获取我的VIP客户身份，如果没有，则默认添加到vip/0的VIP会员组
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self):
        appid = self.get_argument('appid')
        uid = self.request.headers.get('x-user-id')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_mine.get_vip_identity(appid, uid, access_token)
        return self.write(ret)
