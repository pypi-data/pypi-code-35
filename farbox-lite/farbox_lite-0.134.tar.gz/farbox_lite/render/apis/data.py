#coding: utf8
from __future__ import absolute_import
import re
from flask import g

from farbox_lite.utils import LazyDict, smart_unicode, string_types
from farbox_lite.utils.lazy import to_int, get_value_from_data
from farbox_lite.utils.web.pagination import Paginator
from farbox_lite.utils.web.cache_for_function import cache_result

from .site import get_site_from_request
from .all_docs import has_doc as _has_doc, get_next_doc, get_all_docs_by_field, get_all_docs_by_types, get_doc_by_path, get_all_sub_docs_by_path
from .posts import get_posts_by_field, get_posts_by_tag, get_post_docs, get_posts_by_keywords


MAX_PER_PAGE = 1000


def auto_pg(query, limit, page=None, pager_name=None, with_page=True):
    """
    如果函数是获取列表式的，那么第一个函数可以使用g.pg来获得分页信息。
    """
    if isinstance(query, (dict, int, basestring)): # 本身就是具体的数据了，则不做额外的处理了
        return query

    limit = to_int(limit, 10, max_value=MAX_PER_PAGE) #不能超过 1000

    if not with_page and not page:
        page = 1
    else:
        page = page or getattr(g, 'page', 1)

    paginator = Paginator(query, per_page=limit, page=page)

    if with_page: # 启用分页
        if not hasattr(g, 'paginators'):
            g.paginators = []
        if not hasattr(g, 'paginators_dict'):
            g.paginators_dict = {}
        g.paginators.append(paginator)
        if pager_name:
            g.paginators_dict[pager_name] = paginator

    return paginator.list_object


def get_paginator(index_or_name=0):
    paginators  = list(getattr(g, 'paginators', []))
    paginators_dict = getattr(g, 'paginators_dict', {})
    if paginators and isinstance(index_or_name, int):
        try:
            return paginators[index_or_name]
        except:
            return paginators[0]
    elif paginators_dict and isinstance(index_or_name, (str, unicode)):
        # 必然有paginators
        return paginators_dict.get(index_or_name, paginators[0])
    else:
        return LazyDict()



@cache_result
def get_data(types=None, path=None, url_path=None, limit=None, page=None, with_page=True, keywords=None, pager_name=None, min_limit=0, return_one=False, **kwargs):
    # get site first
    site = kwargs.get('site') or get_site_from_request()

    pager_name = kwargs.get('paginator_name') or pager_name # 两个参数名皆可

    if path and not isinstance(path, (str, unicode)): # 这个类型不支持
        path = None

    if url_path: # 如果使用了url_path，则只会返回一个数据对象，非list
        url_path = smart_unicode(url_path).strip('/')
        return_one = True

    if return_one:
        with_page = False
        limit = 1

    if page is None:
        if not with_page:
            page = 1
        else:
            page = getattr(g, 'page', 1)
    page = to_int(page, 1)

    if not url_path and isinstance(url_path, (str, unicode)): # 指定了url_path，但是空的，返回None
        return None

     # 没有站点时候的数据返回
    if not site:
        if return_one:
            return None
        elif 'return_count' in kwargs:
            return 0
        else:
            return []

    # got root first
    root = site['filepath']

    if not limit:
        limit = kwargs.pop('per_page', None)


    path = path or ''

    if path:
        path = path.lower().lstrip('/')

    # 处理 types，转为 list 类型
    types = types or kwargs.get('type') or 'post'
    if isinstance(types, (str, unicode)):
        types = [doc_type for doc_type in re.split(r' |,|\+', types)]
    elif isinstance(types, (list, tuple)):
        types = [doc_type for doc_type in types if isinstance(doc_type, (str, unicode))]
    else:
        return []

    if len(types)==1 and types[0]=='post':
        is_post_type = True
    else:
        is_post_type = False


    if limit:
        limit = to_int(limit) or 12

    if limit and limit > MAX_PER_PAGE:
        limit = MAX_PER_PAGE


    if not limit: # 设定一个默认输出值
        tmp_per_page = getattr(g, 'tmp_per_page', None)
        if tmp_per_page and isinstance(tmp_per_page, int):
            limit = tmp_per_page
        elif is_post_type:
            limit =  to_int(get_value_from_data(site, 'configs.posts_per_page'), 3)
        else:
            limit = 12

    if min_limit and limit < min_limit:
        limit = min_limit

    if url_path:
        # 根据 url_path 直接返回一个 doc 对象
        matched_posts = get_posts_by_field(root=root, field='url_path', value=url_path)
        if matched_posts:
            return matched_posts[0]
        else:
            return None

    sort = kwargs.get('sort') or None
    tag = kwargs.get('tag')
    tags = kwargs.get('tags')
    if not tag and tags:
        if isinstance(tags, string_types):
            tag = tags
        elif isinstance(tags, (list, tuple)):
            tag = tags[0]
    if keywords:
        docs = get_posts_by_keywords(root=root, keywords=keywords, sort=sort)
    elif tag and isinstance(tag, string_types): # for post only
        docs = get_posts_by_tag(root=root, tag=tag, sort=sort)
    elif len(types) > 1:
        docs = get_all_docs_by_types(root=root, types=types, sort=sort)
    elif len(types) == 1 and types[0]!='all':
        doc_type = types[0]
        docs = get_all_docs_by_field(root=root, field='type', value=doc_type, sort=sort,)
    else:
        docs = get_post_docs(root=root)

    if path:
        is_directly_under = kwargs.get('is_directly_under', False)
        docs = get_all_sub_docs_by_path(root=root, raw_docs=docs, parent_path=path, is_direct=is_directly_under)

    if return_one: # 不返回 list
        if docs:
            return docs[0]
        else:
            return

    if not docs:
        data = []
    else:
        data = auto_pg(docs, limit, page, pager_name, with_page=with_page)

    return data



def get_doc(path=None, match=False, site=None, **kwargs):
    if not site:
        site = get_site_from_request()
    if not site:
        return None
    url_path = kwargs.get('url')
    if url_path:
        doc = get_data(url_path=url_path, site=site)
        return doc
    path = smart_unicode(path)
    root = site['filepath']
    doc = get_doc_by_path(path=path, root=root)
    doc_type_by_user = kwargs.get('type')
    if doc and doc_type_by_user and doc_type_by_user != doc.get('type'):
        # 用户指定了类型，但是类型不匹配，返回 None
        return

    return doc


@cache_result
def has_doc(path, site=None):
    # 一个 doc 是否存在
    if not site:
        site = get_site_from_request()
    if not site:
        return False
    root = site['filepath']
    return _has_doc(root=root, path=path)



@cache_result
def get_connected_one(doc=None, same_folder=None, position='>'):
    doc = doc or getattr(g, 'doc', None)
    if not doc:
        return None
    site = get_site_from_request()
    if not site:
        return None

    root = site['filepath']
    if 'date' not in doc:
        return None
    if same_folder is None and doc.get('type') != 'post': # same_folder未指定，并且是post类型的，则全站
        same_folder = True

    if position == '>': # next_one
        return get_next_doc(current_doc=doc, root=root, sort='-date', same_folder=same_folder)
    else: # pre
        return get_next_doc(current_doc=doc, root=root, sort='date', same_folder=same_folder)

