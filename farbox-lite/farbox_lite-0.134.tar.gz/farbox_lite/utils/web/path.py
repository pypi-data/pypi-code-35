#coding: utf8
from __future__ import absolute_import
import re, urllib
from flask import request, g
from .url import get_url_without_prefix

def to_folder_path(path): # 左前是没有/的
    if type(path) in [list, tuple]:  # list to path (str)
        path = '/'.join(path)
    return path.strip('/') + '/'


def is_same_path(p1, p2):
    p1 = p1 or ''
    p2 = p2 or ''
    return p1.strip('/').lower() == p2.strip('/').lower()


def split_path(path):
    # 将一个path转为以/分割的parts，如果有包含~~的，则以~~为第一个split
    path = urllib.unquote(path)
    path = re.sub(r'/page/\d+/?$', '/', path) # 去掉/page/1这样的后缀

    if '~~' in path:
        # /blog/post/~this/is/post/path
        head, tail = path.split('~~', 1)
        parts = [head.strip('/')] + tail.split('/')
    else:
        parts = path.split('/')

    return filter(lambda x: x, parts)


def get_offset_path(path, offset=1):
    # /a/b/c/d 如果 offset=1, 则获得 b/c/d, 如果是2，则是 c/d
    if not offset or not isinstance(offset, int):
        return path
    else:
        raw_path = path
        path = path.lstrip('/')
        parts = split_path(path)
        path = '/'.join(parts[offset:])
        if raw_path.endswith('/'):
            path += '/'
        return path


def get_request_offset_path(offset=1, path=None):
    # 得到偏移几个单位的url，头没有  /
    if path is None:
        path = get_path()
    path = get_offset_path(path, offset)
    return path.lstrip('/')



def get_path():
    # 去掉/page/<int> 这样分页信息后的path, 并且不以/开头
    path_got = getattr(g, 'url_path', None)
    if path_got:
        return path_got
    # path = request.path.lower()
    path = request.path # 保留大小写，想获取 tags 的时候，需要区分大小写敏感的
    page_finder = re.compile(r'(.*?)/page/(\d+)/?$')
    page_result = page_finder.search(path)
    if page_result:
        path, page = page_result.groups()
        g.page = int(page) #存在g里面，这样后面供页面使用的函数，可以取这个值
    path = path.lstrip('/')
    g.url_path = path
    return path



def get_request_path():
    path = get_path()
    return '/%s' % path.lstrip('/')


def get_request_path_without_prefix():
    path = get_request_path()
    return get_url_without_prefix(path)


def get_request_offset_path_without_prefix(offset=1):
    path = get_request_path_without_prefix()
    return get_request_offset_path(offset, path=path)



def get_default_root_by_site_route():
    current_site_route = getattr(g, 'current_site_route', None)
    if current_site_route and isinstance(current_site_route, dict):
        default_root = current_site_route.get('route_root') or ''
        if default_root:
            return default_root
    return None