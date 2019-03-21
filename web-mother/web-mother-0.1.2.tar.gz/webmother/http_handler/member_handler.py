# coding=utf-8

from tweb import base_handler, myweb
from tornado import gen
import json
from webmother.service.async_wrap import ctrl_member


class MemberHandler(base_handler.BaseHandler):
    """
    组织成员的增删改查
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, oid, indicator):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))

        ret = yield ctrl_member.member_create(oid, indicator, data, identity, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def get(self, oid, uid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_member.member_read(oid, uid, identity, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def put(self, oid, uid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))

        ret = yield ctrl_member.member_update(oid, uid, data, identity, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def delete(self, oid, uid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_member.member_remove(oid, uid, identity, access_token)
        return self.write(ret)


class MembersHandler(base_handler.BaseHandler):
    """
    获取组织下的用户列表
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, oid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        array = yield ctrl_member.members_query(oid, identity, access_token)
        return self.write({'list': array})


