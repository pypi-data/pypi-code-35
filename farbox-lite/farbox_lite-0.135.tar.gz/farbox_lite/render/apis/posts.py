#coding: utf8
from __future__ import absolute_import
import os
import uuid
from farbox_lite.compiler.posts.posts import get_compiled_md_docs
from farbox_lite.utils import same_slash, smart_unicode, string_types

from .utils import cached, get_sub_docs_by_path, get_sub_docs_by_field, sort_docs_by_field

post_docs_cache = {}

cache_uuid = uuid.uuid4().hex
def get_cache_uuid():
    return cache_uuid

cache_wrapper = cached(cache_key_func=get_cache_uuid)


def get_post_docs(root):
    global cache_uuid
    root = same_slash(root)
    if not os.path.isdir(root):
        return []
    if root in post_docs_cache:
        posts = post_docs_cache.get(root)
        return posts
    posts = get_compiled_md_docs(root) or []
    post_docs_cache[root] = posts
    cache_uuid = uuid.uuid4().hex
    return posts


def update_post_docs(root):
    global cache_uuid
    root = same_slash(root)
    if not os.path.isdir(root):
        return []
    posts = get_compiled_md_docs(root) or []
    post_docs_cache[root] = posts
    cache_uuid = uuid.uuid4().hex
    return posts



@cache_wrapper
def get_posts_by_tag(root, tag, sort=None):
    if not tag:
        return []
    tag = smart_unicode(tag).strip()
    if not tag:
        return []
    raw_posts = get_post_docs(root)
    posts = []
    for post in raw_posts:
        tags = post.get('tags')
        if tags and isinstance(tags, (list, tuple)):
            if tag in tags:
                posts.append(post)
    posts = sort_docs_by_field(posts, field=sort)
    return posts



@cache_wrapper
def get_posts_by_keywords(root, keywords, sort=None):
    if isinstance(keywords, string_types):
        keywords = [keywords]
    keywords = [smart_unicode(keyword) for keyword in keywords]
    keywords = [keyword for keyword in keywords if keyword.strip()]
    raw_posts = get_post_docs(root)
    if not keywords:
        return raw_posts
    posts = []
    for post in raw_posts:
        raw_content = post.get('raw_content')
        if not raw_content:
            continue
        hit = True
        for keyword in keywords:
            if not keyword in raw_content:
                hit = False
                break
        if hit:
            posts.append(post)
    posts = sort_docs_by_field(posts, field=sort)
    return posts


@cache_wrapper
def get_posts_by_field(root, field, value, sort=None):
    raw_posts = get_post_docs(root)
    posts = get_sub_docs_by_field(raw_posts, field, value)
    posts = sort_docs_by_field(posts, field=sort)
    return posts



@cache_wrapper
def get_posts_by_path(root, parent_path, is_direct=False, sort=None):
    raw_posts = get_post_docs(root)
    posts = get_sub_docs_by_path(root, raw_posts, parent_path, is_direct=is_direct)
    posts = sort_docs_by_field(posts, field=sort)
    return posts


