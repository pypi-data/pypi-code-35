# coding: utf8
from __future__ import absolute_import
from flask import  g, request
from farbox_lite.utils.web.data import make_tree as _make_tree

from farbox_lite.render.apis.data import get_paginator as _get_paginator, get_doc as _get_doc,\
    get_data as _get_data, has_doc as _has_doc
from farbox_lite.utils.web.path import get_request_offset_path
from farbox_lite.utils.web.cache_for_function import cache_result



class Data(object):
    @staticmethod
    @cache_result
    def make_tree(docs, kept_fields=None):
        return _make_tree(docs, kept_fields)

    @staticmethod
    @cache_result
    def get_data(*args, **kwargs):
        return _get_data(*args, **kwargs)


    @staticmethod
    @cache_result
    def get_paginator(index_or_name=0):
        return _get_paginator(index_or_name)


    @staticmethod
    @cache_result
    def get_doc(path=None, match=True, **kwargs):
        # 有指定在某个目录下的，则补全 path 本身, 可以使用 url其实
        path = path or ''
        root = kwargs.pop('root', None) or ''
        if root and isinstance(root, (str, unicode)) and len(root) < 100:
            path = '/%s/%s' % (root.strip('/'), path.strip('/'))
            path = path.replace('//', '/') # 两个 // 是不允许的

        doc = _get_doc(path, match=match, **kwargs)
        if not doc:
            return doc
        as_context_doc = kwargs.get('as_context_doc')
        if as_context_doc and doc:
            g.doc = doc
        return doc

    def doc(self):
        # 返回纯粹的一个 doc 对象，比如一个 csv 类型的
        offset_path = get_request_offset_path(1)
        _doc = _get_doc(offset_path)
        if not _doc:
            _doc = _get_doc(request.path)
        return _doc

    @staticmethod
    def has(path): # , must_doc=False
        return _has_doc(path)



# 这种固定变量空间，要慎重使用 cached_property
#default_variables = {
#    'h': Html(),
#}

@cache_result
def d():
    return Data()

@cache_result
def data():
    return Data()
