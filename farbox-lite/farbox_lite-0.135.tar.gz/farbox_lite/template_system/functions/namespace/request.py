# coding: utf8
from __future__ import absolute_import
from flask import request as _request, g
import copy, re, os, time

from farbox_lite.utils.functional import cached_property, curry
from farbox_lite.utils import smart_unicode
from farbox_lite.utils.lazy import to_int
from farbox_lite.utils.mime import guess_type
from farbox_lite.utils.url import join_url, is_same_url, decode_url_arg as _decode_url_arg, encode_url_arg as _encode_url_arg

from farbox_lite.utils.web.response import force_redirect
from farbox_lite.utils.web.request import get_visitor_ip, get_language, get_user_agent
from farbox_lite.utils.web.path import get_request_offset_path, get_request_offset_path_without_prefix, get_path
from farbox_lite.utils.web.url import get_url_with_prefix, get_url_without_prefix
from farbox_lite.utils.web.cache_for_function import cache_result





class Request(object):
    def __init__(self):
        self.url_fields = ['path', 'url', 'base_url', 'url_root', ]
        self.fields = ['form', 'args', 'values', 'method',
              'json', 'host', 'data', 'account_id', 'cookies']
        self.safe_fields = ['form', 'args', 'values', 'method', 'json', 'data', 'referrer']
        self.keep_url_safe = getattr(g, 'keep_request_url_safe', False)
        self.__setattr__ = lambda key,value: None # not allowed

        self.set_property_allowed = True


    def __getattr__(self, item):
        if item == 'refer':
            item = 'referrer'

        if self.keep_url_safe:
            if item in self.safe_fields:
                return getattr(_request, item)
            else:
                return None
        if item in self.url_fields:
            # url 相关的调用, 要先过滤掉prefix
            value = getattr(_request, item, None)
            return get_url_without_prefix(value)
        elif item.startswith('_') and item.lstrip('_') in self.url_fields:
            # 比如 request._path, request._url 返回原始的 _request 上属性
            real_item = item.lstrip('_')
            value = getattr(_request, real_item, None)
            return value
        elif item in self.fields:
            return getattr(_request, item, None)
        elif item == 'url_without_host':
            return _request.url.replace(_request.url_root, '/')
        elif item == 'user_agent':
            user_agent = copy.copy(_request.user_agent)
            user_agent._parser = None
            return user_agent
        elif re.match('^_?path_?\d+$', item): # request.path1
            offset_c = re.search('\d+', item)
            i = offset_c.group()
            return self.get_n_path(i, raw=item.startswith('_'))
        elif re.match('^_?offset_path_?\d+$', item): # request.offset_path_1
            offset_c = re.search('\d+', item)
            i = offset_c.group()
            return self.get_offset_path(i, raw=item.startswith('_'))

        else:
            return self.__dict__.get(item)


    def get_offset_path(self, offset=None, raw=True):
        offset = to_int(offset) or 1
        path = get_path()
        if not raw:
            path = get_url_without_prefix(path)
        return get_request_offset_path(offset, path=path)


    def get_n_path(self, n=0, raw=True):
        # 将 _request.path 按照 / 分割，获得某posiiton上的一部分，不包括 /
        path_parts = _request.path.strip("/").split("/")
        n = to_int(n) -1
        try:
            value = path_parts[n]
        except:
            value = ''
        if raw:
            return value
        else:
            return get_url_without_prefix(value)


    @cached_property
    def raw_user_agent(self):
        return _request.environ.get('HTTP_USER_AGENT') or ''

    @cached_property
    def url_path(self):
        return '/'+get_path()

    @cached_property
    def ip(self):
        return get_visitor_ip()

    @cached_property
    def lang(self):
        return get_language(_request.environ)

    @cached_property
    def language(self):
        return self.lang

    @cached_property
    def protocol(self):
        protocol = _request.environ.get('HTTP_X_PROTOCOL') or 'http'
        return protocol.lower()

    @cached_property
    def is_https(self):
        return self.protocol=='https'

    @cached_property
    def ext(self):
        return self.get_ext()

    @cached_property
    def mime_type(self):
        return self.get_mime_type()


    @cached_property
    def user_agent(self):
        return get_user_agent()


    @staticmethod
    def redirect(url, code=302):
        url = smart_unicode(url)
        force_redirect(url, code=code)


    def get_mime_type(self, path=''):
        if not isinstance(path, (str, unicode)):
            path = smart_unicode(path)
        path = path or get_path()
        if path and isinstance(path, (str, unicode)):
            return guess_type(path) or ''
        else:
            return ''


    def get_ext(self, path=''):
        if not isinstance(path, (str, unicode)):
            path = smart_unicode(path)
        path = path or _request.path
        ext = os.path.splitext(path)[-1] or ''
        ext = ext.lstrip('.').lower()
        return ext

    @staticmethod
    def join(base_url, **kwargs):
        if isinstance(base_url, (str, unicode)):
            return join_url(base_url, **kwargs)
        else:
            return base_url

    @staticmethod
    def decode_url_arg(arg):
        return _decode_url_arg(arg)

    @staticmethod
    def encode_url_arg(arg):
        return _encode_url_arg(arg)


    @cached_property
    def context_doc(self):
        # 上下文对象
        doc_in_g = getattr(g, 'doc', None)
        return doc_in_g



@cache_result
def request():
    return Request()


