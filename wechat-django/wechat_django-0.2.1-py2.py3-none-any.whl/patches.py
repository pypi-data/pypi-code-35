# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.http import urlencode
import logging

from wechatpy import (
    exceptions as excs, WeChatClient as _Client, WeChatOAuth as _OAuth)
from wechatpy.constants import WeChatErrorCode
from wechatpy.client import api

from .oauth import WeChatSNSScope


class WeChatMaterial(api.WeChatMaterial):
    def get_raw(self, media_id):
        return self._post(
            'material/get_material',
            data={
                'media_id': media_id
            }
        )


class WeChatMessage(api.WeChatMessage):
    def send_articles(self, user_id, articles, account=None):
        try:
            return super(WeChatMessage, self).send_articles(
                user_id, articles, account)
        except excs.WeChatClientException as e:
            # 对于主动发送图文消息,只发送一条
            # 参见 https://mp.weixin.qq.com/cgi-bin/announce?action=getannouncement&announce_id=115383153198yAvN
            if e.errcode == WeChatErrorCode.INVALID_MESSAGE_TYPE:
                return super(WeChatMessage, self).send_articles(
                    user_id, articles[:1], account)
            raise


class WeChatClient(_Client):
    """继承原有WeChatClient添加日志功能 追加accesstoken url获取"""
    appname = None
    # 增加raw_get方法
    material = WeChatMaterial()
    message = WeChatMessage()

    ACCESSTOKEN_URL = None

    def _fetch_access_token(self, url, params):
        """自定义accesstoken url"""
        return super(WeChatClient, self)._fetch_access_token(
            self.ACCESSTOKEN_URL or url, params)

    def _request(self, method, url_or_endpoint, **kwargs):
        self._update_log(method=method, url=url_or_endpoint, **kwargs)
        try:
            rv = super(WeChatClient, self)._request(
                method, url_or_endpoint, **kwargs)
            self._log(logging.DEBUG)
            return rv
        except Exception as e:
            if isinstance(e, excs.WeChatClientException):
                self._log(logging.WARNING)
            else:
                self._log(logging.ERROR)
            raise

    def _handle_result(self, res, method=None, url=None, *args, **kwargs):
        resp = res.content if hasattr(res, "content") else res
        self._update_log(resp=resp)
        return super(WeChatClient, self)._handle_result(
            res, method, url, *args, **kwargs)

    @property
    def _logger(self):
        return logging.getLogger("wechat.api.{appname}".format(
            type=type,
            appname=self.appname
        ))

    def _update_log(self, **kwargs):
        if not hasattr(self, "_log_kwargs"):
            self._log_kwargs = dict()
        self._log_kwargs.update(kwargs)

    def _log(self, level):
        msg = "{method}\t{url}".format(
            method=self._log_kwargs["method"],
            url=self._log_kwargs["url"]
        )
        for k, v in self._log_kwargs.items():
            msg += "\t{k}: {v}".format(k=k, v=v)
        kwargs = dict()
        if level >= logging.WARNING:
            kwargs["exc_info"] = True
        self._logger.log(level, msg)
        self._log_kwargs.clear()


class WeChatOAuth(_OAuth):
    OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize"
    QRCONNECT_URL = "https://open.weixin.qq.com/connect/qrconnect"

    def __init__(self, app_id, secret):
        super(WeChatOAuth, self).__init__(app_id, secret, "")

    def authorize_url(self, redirect_uri, scope=WeChatSNSScope.BASE, state=""):
        return self.OAUTH_URL + "?" + urlencode(dict(
            appid=self.app_id,
            redirect_uri=redirect_uri,
            response_type="code",
            scope=scope,
            state=state
        )) + "#wechat_redirect"

    def qrconnect_url(self, redirect_uri, state=""):
        return self.QRCONNECT_URL + "?" + urlencode(dict(
            appid=self.app_id,
            redirect_uri=redirect_uri,
            response_type="code",
            scope="snsapi_login",
            state=state
        )) + "#wechat_redirect"
