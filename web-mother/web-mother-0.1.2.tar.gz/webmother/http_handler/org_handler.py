# coding=utf-8

from tweb import base_handler, myweb
from tweb.error_exception import ErrException, ERROR
from tornado import gen
import json
from webmother.service.async_wrap import ctrl_org


class OrgHandler(base_handler.BaseHandler):
    """
    分类节点基本操作：增删改查（CRUD）
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, oid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))
        if 'name' not in data:
            raise ErrException(ERROR.E40000, extra='not name field')

        ret = yield ctrl_org.create(oid, data, identity, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def get(self, oid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_org.read(oid, identity, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def put(self, oid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))
        ret = yield ctrl_org.update(oid, data, identity, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def delete(self, oid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_org.change_status(oid, 'remove', identity, access_token)
        return self.write(ret)


class StatusHandler(base_handler.BaseHandler):
    """
    节点状态操作，只存在更新操作
    """

    @myweb.authenticated
    @gen.coroutine
    def put(self, oid, action):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_org.change_status(oid, action, identity, access_token)
        return self.write(ret)


class ChildrenHandler(base_handler.BaseHandler):
    """
    获取子节点列表
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, parent):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        array = yield ctrl_org.children(parent, identity, access_token)
        return self.write({'list': array})


class MovingHandler(base_handler.BaseHandler):
    """
    节点状态操作，只存在更新操作
    """

    @myweb.authenticated
    @gen.coroutine
    def put(self, oid, oid_to):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_org.move(oid, oid_to, identity, access_token)
        return self.write(ret)


class OurPassportsHandler(base_handler.BaseHandler):
    """
    获取我们(组织)的授权列表
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, oid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        array = yield ctrl_org.our_passports(oid, identity, access_token)

        return self.write({'list': array})


class AppHandler(base_handler.BaseHandler):
    """
    应用创建/删除，所谓应用就是赋能一个组织节点具有接入能力
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, oid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_org.app_activate(oid, identity, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def delete(self, oid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_org.appid_deactivate(oid, identity, access_token)
        return self.write(ret)


class VipHandler(base_handler.BaseHandler):

    @myweb.authenticated
    @gen.coroutine
    def post(self):
        """
        针对客户添加会员组
        """
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        appid = self.get_argument('appid')

        data = json.loads(self.request.body.decode('utf-8'))
        level = data.get('level')
        display = data.get('display')

        ret = yield ctrl_org.vip_create(appid, level, display, identity, access_token)
        return self.write(ret)


class VipsHandler(base_handler.BaseHandler):
    @myweb.authenticated
    @gen.coroutine
    def get(self):
        """
        查询会员组列表
        """
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        appid = self.get_argument('appid')

        array = yield ctrl_org.vip_query(appid, identity, access_token)
        return self.write({'list': array})
