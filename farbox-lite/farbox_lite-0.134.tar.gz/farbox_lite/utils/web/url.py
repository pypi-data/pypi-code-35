# coding: utf8
from __future__ import absolute_import
from flask import g
import re, os
from farbox_lite.utils.functional import  curry
from farbox_lite.utils.mime import guess_type


def get_url_with_prefix(url, force=False, prefix=None):
    # 转换 url (url_path), 自动补全前缀
    # force 的话，就会强制处理, 即使不以 / 开头的，都会尝试转换
    if not isinstance(url, (str, unicode)):
        return url
    if not url.startswith('/') and not force:
        # 仅仅处理当前网站的URL，以避免混淆
        return url
    if prefix is None:
        prefix = getattr(g, 'prefix', '')
    if prefix and isinstance(prefix, (str,unicode)):
        raw_url = url
        prefix = prefix.strip().strip('/')
        url = url.lstrip('/')
        if url.lower().startswith(prefix+'/') or url.lower() == prefix:
            # 本身已经是前缀补足了
            # 所以，有一个问题，在 /prefix 下，不能存在 一个/prefix/prefix 的意图，这不会转换
            return raw_url
        if url:
            new_url = '/%s/%s' % (prefix, url)
        else: # 相当原始的首页 /
            new_url = '/%s' % prefix
        return new_url
    else:
        return url


def get_url_without_prefix(url, prefix=None):
    # url 去除 prefix 后， 一般以 '/' 开头
    if not isinstance(url, (str, unicode)):
        return url # ignore
    url_startswith_dash = url.startswith('/')
    raw_url = url
    if prefix is None:
        prefix = getattr(g, 'prefix', '')
    if prefix and isinstance(prefix, (str,unicode)):
        url = url.lstrip('/')
        prefix = prefix.strip().strip('/')
        if url.startswith(prefix+'/') or url == prefix:
            first_char = '/' if url_startswith_dash else ''
            url =  first_char + url.replace(prefix, '', 1).lstrip('/')
            # 确保模拟 request.path 类似的逻辑，一般可以保证 / 开头的
            return url
    return raw_url



# 只处理 / 开头的url, 视为 site 内部的 url
site_a_dom_re_compiler = re.compile(r'(<a[^<]+href=[\'"])(/.*?)([\'"][^<]*>.*?</a>)', flags=re.S|re.I)


def auto_prefix_a_re_obj_replacer(re_obj, prefix_url, ignore_file_url=True, ignore_keywords=('nav__item',)):
    part1 = re_obj.group(1)
    current_url = re_obj.group(2)
    part3 = re_obj.group(3)
    raw_a_html = re_obj.group()
    if '#' in current_url: # 有 # 存在的，则不进行转义、自动补全
        return raw_a_html
    for ignore_keyword in ignore_keywords:
        # 有些关键词，会自动不进行补全，比如作为自动生成的 nav
        if ignore_keyword in raw_a_html:
            return raw_a_html
    if ignore_file_url and current_url:
        # 直接的文件输出地址，不做补全，避免画蛇添足, 但也只是大概的估算
        file_type = guess_type(current_url)
        # link_in_site 是非常特殊的字符，如果存在，则认为这个也是要处理
        if 'link_in_site' not in raw_a_html:
            if file_type.startswith('image/') or file_type.startswith('text/') or file_type.startswith('application/'):
                return raw_a_html
    new_url = get_url_with_prefix(current_url, prefix=prefix_url)
    return '%s%s%s' % (part1, new_url, part3)



def auto_complete_prefix_url_for_html(html, prefix_url=None, ignore_file_url=True):
    if not isinstance(prefix_url, (str, unicode)):
        return html
    prefix_url = prefix_url.strip().strip('/')
    if not prefix_url:
        return html
    new_html = site_a_dom_re_compiler.sub(curry(auto_prefix_a_re_obj_replacer, prefix_url=prefix_url, ignore_file_url=ignore_file_url), html)
    return new_html
