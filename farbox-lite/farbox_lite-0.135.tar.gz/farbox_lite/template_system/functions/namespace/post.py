# coding: utf8
from __future__ import absolute_import
import re
from flask import g, request
from farbox_markdown.util import is_a_markdown_file

from farbox_lite.render.apis.data import get_data, get_paginator, get_doc
from farbox_lite.template_system.functions.namespace.utils.doc_list_utils import DocList
from farbox_lite.utils import smart_unicode
from farbox_lite.utils.functional import curry, cached_property
from farbox_lite.utils.web.path import get_request_offset_path_without_prefix
from farbox_lite.utils.web.cache_for_function import cache_result
from farbox_lite.utils.lazy import get_value_from_data, to_int


class Posts(DocList):
    def __init__(self):
        DocList.__init__(self, 'posts')
        self.status = 'public' # by default

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
        self.pager_name = 'posts'
        if hasattr(obj, '__iter__'):
            return obj.__iter__()
        return obj


    @cached_property
    def length(self):
        return len(self.list_obj)


    def set_status(self, status):
        if isinstance(status, (str, unicode)):
            status = status[:35]
            self.status = status
        return ''


    def get_recent(self, limit=8):
        # 可以获得最近的几篇文章
        limit = to_int(limit, 8)
        limit = min(100, limit)
        return get_data(type='post', limit=limit, sort='-date', with_page=False, path=self.under)

    def get_recent_posts(self, limit=8):
        return self.get_recent(limit)


    def get_by_status(self, status='public', limit=None):
        # 按照 status 获得对应的文章
        if not isinstance(status, (int, str, unicode, float)):
            return []
        status = smart_unicode(status)
        self.pager_name = pager_name = '%s_posts' % status
        return get_data(types='post', status=status, pager_name=pager_name, min_limit=self.min_per_page, limit=limit)


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
        self.pager_name = 'all_posts'
        return self._all


    @cached_property
    def _all(self):
        # 所有日志
        return get_data(types='post', pager_name='all_posts', min_limit=self.min_per_page)


    @cached_property
    def post(self):
        # 在 functions.namespace.shortcut 中，将 post 本身作为一个快捷调用，可以直接调用
        doc_in_g = getattr(g, 'doc', None)
        if doc_in_g and isinstance(doc_in_g, dict) and doc_in_g.get('type') == 'post':
            return doc_in_g

        # 得到当前 url 下对应的 post
        hide_post_prefix = get_value_from_data(g, 'site.configs.hide_post_prefix', default=False)
        if hide_post_prefix: # 不包含 /post/ 的 url
            url_path = self.request_path.lstrip('/')
        else: # 可能是/post/<url>的结构
            url_path = get_request_offset_path_without_prefix(offset=1)
        post_doc = get_data(type='post', url_path=url_path, return_one=True)

        if not post_doc and is_a_markdown_file(self.request_path): # 直接是markdown文件的路径
            post_doc = get_data(type='post', path=self.request_path, return_one=True)
            return post_doc # 避免写入g.doc todo why????

        if not post_doc and url_path and '/' in url_path: # sub path 的对应，offset 一次，让 markdown 本身作为 template 成为可能
            url_path = '/'.join(url_path.split('/')[:-1])
            post_doc = get_data(type='post', url_path=url_path, return_one=True)


        if post_doc: # 写入g.doc，作为上下文对象参数来处理
            g.doc = post_doc
        return post_doc


    @cached_property
    def list_obj(self):
        # 针对默认 的 url 规则，自动对应默认的 posts 的调用
        # 主要就是posts直接被 for 的逻辑调用了
        pager_name = 'posts'
        if self.keywords: # 关键词搜索放在最前面
            under = request.args.get('under') or self.under
            return get_data(type='post', keywords=request.args.get('s'), path=under,
                            limit=50, pager_name=pager_name, min_limit=self.min_per_page,
                            sort=self.sort or '-date', status=self.status)

        if self.request_path.startswith('/category/'): # 指定目录下的
            return get_data(type='post', path=get_request_offset_path_without_prefix(1), pager_name=pager_name, min_limit=self.min_per_page,
                            sort=self.sort, status=self.status)
        if self.request_path.startswith('/tags/') or self.request_path.startswith('/tag/'):
            _tags = get_request_offset_path_without_prefix(offset=1).strip('/')
            if _tags:
                _tags = [tag for tag in _tags.split('+') if tag]
                return get_data(type='post', tags=_tags, pager_name=pager_name, min_limit=self.min_per_page,
                                sort=self.sort, status=self.status)
        # at last
        path = self.under
        if not path and request.args.get('c'):
            # 相当于分类的路径传入
            path = request.args.get('c')
        _posts = get_data(type='post', path=path, pager_name=pager_name, min_limit=self.min_per_page, sort=self.sort, status=self.status)
        return _posts

    @cached_property
    def counts(self):
        self_list_obj = self.list_obj # 先行调用
        if self.pager:
            return self.pager.total_count
        else:
            return 0

    @cached_property
    def posts_count(self):
        return self.counts

    @cached_property
    def keywords(self):
        return request.args.get('s') or ''

    @cached_property
    def tags(self):
        _tags = get_request_offset_path_without_prefix(offset=1)
        if _tags == '/':
            return []
        else:
            _tags = [tag for tag in _tags.split('+') if tag]
            return _tags



@cache_result
def posts():
    return Posts()