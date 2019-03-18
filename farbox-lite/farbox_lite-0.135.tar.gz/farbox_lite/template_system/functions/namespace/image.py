# coding: utf8
from __future__ import absolute_import

import re, random, os
from flask import g, request
from jinja2.runtime import Undefined

from farbox_lite.utils.functional import curry, cached_property
from farbox_lite.utils import smart_unicode
from farbox_lite.utils.lazy import get_value_from_data, to_int, string_to_int
from farbox_lite.utils.mime import guess_type

from farbox_lite.utils.web.path import get_request_offset_path_without_prefix
from farbox_lite.utils.web.cache_for_function import cache_result

from farbox_lite.render.apis.data import get_data, get_paginator, has_doc, get_doc

from farbox_lite.template_system.functions.namespace.utils.doc_list_utils import DocList

_max = max



class Image(object):
    # 一个具体图片的文档对象 wrap 之后的 data obj
    def __init__(self, doc):
        if not isinstance(doc, dict):
            doc = {}
        if doc and not doc.get('type')=='image': # 必须保证是图片类型
            doc = None

        self.md5 = doc.get('md5') or doc.get('path') # md5值
        self.id = doc.get('id') or doc.get('_id')
        self.raw = doc or {}

        self.is_image = True # 在某些场合，可以用于判断当前是否 Image 对象

    def __nonzero__(self):
        return bool(self.raw)


    def __getattr__(self, item):
        if item in self.raw:
            return self.raw.get(item)
        return self.__dict__.get(item, Undefined())

    @cached_property
    def length(self):
        return len(self.list_obj)


    @cached_property
    def name(self):
        path = self.raw.get('path') or ''
        pathname = os.path.split(path)[-1]
        return pathname


    @cached_property
    def url(self):
        return '/' + self.raw['path'].strip('/').lower()

    @cached_property
    def cover(self):
        return self.url




class Images(DocList):
    def __init__(self):
        DocList.__init__(self, 'images')

    def __getattr__(self, item):
        # 找不到attribute的时候，会调用getattr
        if re.match('^recent_?\d+$', item): # 获得最近的几篇文章
            limit = re.search('\d+', item).group()
            limit = to_int(limit)
            return self.get_recent(limit)

    def __getitem__(self, item):
        if hasattr(self.list_obj, '__getitem__'):
            return self.list_obj.__getitem__(item)

    def __nonzero__(self):
        return bool(self.list_obj)

    def __iter__(self):
        # 返回一个迭代器，用于 for 的命令
        obj = self.list_obj
        self.pager_name = 'images'
        if hasattr(obj, '__iter__'):
            return obj.__iter__()
        return obj


    def return_image_objs(self, docs):
        if not docs:
            return []
        objs = [Image(doc) for doc in docs]
        return objs



    def get_recent(self, limit=8):
        limit = to_int(limit, 8)
        limit = min(100, limit)
        image_docs = get_data(type='image', limit=limit, with_page=False, sort='-date')
        return self.return_image_objs(image_docs)


    def get_recent_images(self, limit=8):
        return self.get_recent(limit)


    def get_one(self, path):
        return self.find_one(path)


    @property
    def pager(self):
        # 由于获得分页的数据对象
        # 比如可以直接调用  posts.pager....
        return get_paginator(self.pager_name)

    @property
    def paginator(self):
        return self.pager


    @property
    def all(self):
        self.pager_name = 'all_images'
        return self._all


    @cached_property
    def _all(self):
        # 所有日志
        image_docs = get_data(types='image', pager_name='all_images', min_limit=self.min_per_page)
        return self.return_image_objs(image_docs)


    @cached_property
    def image(self):
        # 得到当前 url 下对应的 图片
        url_path = get_request_offset_path_without_prefix(offset=1)
        image_doc = self.get_one(url_path)
        if image_doc:
            g.file_doc = image_doc
        return Image(image_doc)


    @cached_property
    def list_obj(self):
        pager_name = 'images'
        # 针对默认 的 url 规则，自动对应默认的 posts 的调用
        if self.keywords: # 关键词搜索放在最前面
            return get_data(type='image', keywords=request.args.get('s'), limit=50, pager_name=pager_name, min_limit=self.min_per_page, sort=self.sort)
        if self.under is not None: # 指定了 under
            return get_data(type='image', path=self.under, pager_name=pager_name, min_limit=self.min_per_page, sort=self.sort)
        if self.request_path.startswith('/category/'): # 指定目录下的
            return get_data(type='image', path=get_request_offset_path_without_prefix(1), pager_name=pager_name, min_limit=self.min_per_page, sort=self.sort)
        # at last
        _images = get_data(type='image', pager_name=pager_name, min_limit=self.min_per_page, sort=self.sort)
        return self.return_image_objs(_images)

    @cached_property
    def counts(self):
        self_list_obj = self.list_obj # 先行调用
        if self.pager:
            return self.pager.total_count
        else:
            return 0

    @cached_property
    def images_count(self):
        return self.counts


@cache_result
def images():
    return Images()