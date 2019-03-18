#coding: utf8
from __future__ import absolute_import
import os
import uuid

from farbox_lite.compiler.files import get_compiled_file_docs
from farbox_lite.utils import same_slash, smart_unicode, get_relative_path
from .utils import cached, get_sub_docs_by_path, get_sub_docs_by_field, sort_docs_by_field

file_docs_cache = {}

cache_uuid = uuid.uuid4().hex
def get_cache_uuid():
    return cache_uuid

cache_wrapper = cached(cache_key_func=get_cache_uuid)


def get_file_docs(root):
    global cache_uuid
    root = same_slash(root)
    if not os.path.isdir(root):
        return []
    if root in file_docs_cache:
        docs = file_docs_cache.get(root)
        return docs
    docs = get_compiled_file_docs(root) or []
    file_docs_cache[root] = docs
    cache_uuid = uuid.uuid4().hex
    return docs


def update_file_docs(root):
    global cache_uuid
    root = same_slash(root)
    if not os.path.isdir(root):
        return []
    docs = get_compiled_file_docs(root) or []
    file_docs_cache[root] = docs
    cache_uuid = uuid.uuid4().hex
    return docs


@cache_wrapper
def get_file_docs_by_field(root, field, value, sort=None):
    raw_docs = get_file_docs(root)
    docs = get_sub_docs_by_field(raw_docs, field, value)
    docs = sort_docs_by_field(docs, field=sort)
    return docs


@cache_wrapper
def get_file_docs_by_path(root, parent_path, is_direct=False, sort=None):
    raw_file_docs = get_file_docs(root)
    file_docs = get_sub_docs_by_path(root, raw_file_docs, parent_path, is_direct=is_direct)
    file_docs = sort_docs_by_field(file_docs, field=sort)
    return file_docs


@cache_wrapper
def get_image_docs(root, sort=None):
    docs = get_file_docs_by_field(root, 'type', 'image')
    docs = sort_docs_by_field(docs, field=sort)
    return docs


@cache_wrapper
def get_image_docs_by_path(root, parent_path, is_direct=False, sort=None):
    raw_file_docs = get_file_docs(root)
    file_docs = get_image_docs(root, raw_file_docs, parent_path, is_direct=is_direct)
    file_docs = sort_docs_by_field(file_docs, field=sort)
    return file_docs
