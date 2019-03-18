# coding: utf8
from __future__ import absolute_import
from flask import g

from farbox_lite.render.apis.data import get_doc, get_data, get_paginator as _get_paginator, get_connected_one
from farbox_lite.template_system.functions.namespace.utils.category import Category
from farbox_lite.utils import smart_unicode
from farbox_lite.utils.functional import cached_property
from farbox_lite.utils.web.cache_for_function import cache_result
from farbox_lite.utils.web.path import get_request_offset_path_without_prefix, get_request_path_without_prefix



class DocList(object):
    def __init__(self, namespace=''):
        self.pager_name = ''
        self.namespace = namespace
        self.min_per_page = 0

        self.sort = None # 可能设置某个排序的状态

        self.request_path = get_request_path_without_prefix()


    def set_min_per_page(self, min_per_page):
        if isinstance(min_per_page, int) and min_per_page >=0:
            self.min_per_page = min_per_page
        return '' # return nothing


    def set_sort(self, sort):
        if not isinstance(sort, (str, unicode, int, bool)):
            return # ignore
        if isinstance(sort, (str, unicode)):
            sort = smart_unicode(sort)[:10]
        self.sort = sort


    def get_paginator(self, name):
        return _get_paginator(name)

    def get_pager(self, name):
        return _get_paginator(name)


    @cached_property
    def all_categories(self):
        # 这个返回的是原生的数据对象，self.get_categories 则是 wrap 过的 Category 类实例化对象
        # all categories
        return get_data(type='folder', limit=1000, with_page=False) or []
        #return self.get_categories(sort='')
        # , level=

    @cache_result
    def get_categories(self, path='', level=0, sort='position', ignore_hidden=True):
        # 获取分类的通用函数
        kwargs = {}
        _categories = get_data(type='folder', limit=300, with_page=False, path=path, level=level, sort=sort, **kwargs) or []
        categories = []
        for c in _categories:
            if ignore_hidden: # path 以 _开头的，ignore
                if c.get('path', '').startswith('_'):
                    continue
            categories.append(Category(c))
        return categories


    @cached_property
    def category(self):
        # /xxx/<category_path>
        # 根据路径，获得当前的 category 对象
        if self.request_path == '/':
            return None
        doc = get_doc(path=get_request_offset_path_without_prefix(offset=1), match=True)
        if doc and doc.get('type') != 'folder':
            return None
        else:
            return Category(doc)
        
    @staticmethod
    def to_category(category_doc):
        if isinstance(category_doc, Category):
            return category_doc
        if category_doc and isinstance(category_doc, dict) and category_doc.get('type')=='folder':
            return Category(category_doc)
        return None


    @cached_property
    def categories(self):
        # 不是纯dict数据，而是Category包裹的
        category_objs = get_data(type='folder', limit=300, with_page=False, sort='position')
        categories = []
        for category_obj in category_objs:
            if category_obj.get('path', '').startswith('_'):
                continue
            categories.append(Category(category_obj))
        return categories

    @cached_property
    def sub_categories(self):
        parent_category = self.category
        if parent_category: # 当前有 category 的 url 命中，相当于子目录
            category_objs = get_data(types='folder', path=parent_category['path'], level=1, limit=300, with_page=False)
        else:
            category_objs = []
        categories = []
        for category_obj in category_objs:
            if category_obj.get('path', '').startswith('_'):
                continue
            categories.append(Category(category_obj))
        return categories



    @cached_property
    def context_doc(self):
        # 上下文对象
        doc_in_g = getattr(g, 'doc', None)
        return doc_in_g


    @cached_property
    def next_one(self):
        return self.get_pre_next_one(is_next=True)

    @cached_property
    def previous_one(self):
        return self.get_pre_next_one(is_next=False)

    @cached_property
    def pre_one(self):
        return self.previous_one

    @cached_property
    def current_folder_next_one(self):
        # 当前目录下的
        return self.get_pre_next_one(is_next=True, same_folder=True)

    @cached_property
    def current_folder_previous_one(self):
        # 当前目录下的
        return self.get_pre_next_one(is_next=False, same_folder=True)

    @cached_property
    def current_folder_pre_one(self):
        return self.current_folder_previous_one()

    def get_pre_next_one(self, is_next=True, same_folder=None):
        doc = self.context_doc
        if not doc:
            return # ignore

        date = doc.get('date')
        if not date:
            return

        if same_folder is None and doc.get('type') != 'post': # same_folder未指定，并且是post类型的，则全站
            same_folder = True

        related_doc = get_connected_one(doc=doc, same_folder=same_folder, position='>' if is_next else '<')
        return related_doc




