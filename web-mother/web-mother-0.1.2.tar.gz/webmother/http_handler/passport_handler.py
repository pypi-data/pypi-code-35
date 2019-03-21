# coding=utf-8

from tweb import base_handler, myweb
from tornado import gen
import json
from webmother.service.async_wrap import ctrl_passport


class PassportTplHandler(base_handler.BaseHandler):
    """
    获取分类节点的授权列表
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, cid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_passport.get_passport_tpl(cid, passport, access_token)
        return self.write(ret)


class PassportHandler(base_handler.BaseHandler):
    """
    分类向组织的授权(实际上就是操作分类节点与组织之间的关系)
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, cid, oid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        try:
            data = json.loads(self.request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            data = None

        ret = yield ctrl_passport.passport_create(cid, oid, data, passport, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def get(self, cid, oid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_passport.passport_read(cid, oid, passport, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def put(self, cid, oid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))
        ret = yield ctrl_passport.passport_update(cid, oid, data, passport, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def delete(self, cid, oid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_passport.passport_remove(cid, oid, passport, access_token)
        return self.write(ret)


class PassportsHandler(base_handler.BaseHandler):
    """
    获取分类节点的授权列表
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, cid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_passport.passports_query(cid, passport, access_token)
        return self.write({'list': ret})

