# coding=utf-8

from tweb import base_handler, myweb
from tweb.error_exception import ErrException, ERROR
from tornado import gen
import json
from webmother.service.async_wrap import ctrl_catalog


class CatalogHandler(base_handler.BaseHandler):
    """
    分类节点基本操作：增删改查（CRUD）
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, cid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        catalog = json.loads(self.request.body.decode('utf-8'))
        if 'name' not in catalog:
            raise ErrException(ERROR.E40000, extra='not name field')

        ret = yield ctrl_catalog.create(cid, catalog, passport, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def get(self, cid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_catalog.read(cid, passport, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def put(self, cid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        catalog = json.loads(self.request.body.decode('utf-8'))
        ret = yield ctrl_catalog.update(cid, catalog, passport, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def delete(self, cid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_catalog.change_status(cid, 'remove', passport, access_token)
        return self.write(ret)


class StatusHandler(base_handler.BaseHandler):
    """
    节点状态操作，只存在更新操作
    """

    @myweb.authenticated
    @gen.coroutine
    def put(self, cid, action):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_catalog.change_status(cid, action, passport, access_token)
        return self.write(ret)


class ChildrenHandler(base_handler.BaseHandler):
    """
    获取子节点列表
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, cid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_catalog.children(cid, passport, access_token)
        return self.write({'list': ret})


class MovingHandler(base_handler.BaseHandler):
    """
    节点状态操作，只存在更新操作
    """

    @myweb.authenticated
    @gen.coroutine
    def put(self, cid, cid_to):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_catalog.move(cid, cid_to, passport, access_token)
        return self.write(ret)
