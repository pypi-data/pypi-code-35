#coding: utf8
from __future__ import absolute_import
from .files import get_file_docs, get_cache_uuid as get_files_cache_uuid
from .posts import get_post_docs, get_cache_uuid as get_posts_cache_uuid
from .utils import sort_docs_by_field, cached, get_sub_docs_by_field, get_sub_docs_by_path
import os
from farbox_lite.compiler.files import filepath_to_file_doc


def get_cache_uuid():
    cache_uuid = '%s-%s' % (get_files_cache_uuid(), get_posts_cache_uuid())
    return cache_uuid

cache_wrapper = cached(cache_key_func=get_cache_uuid)


@cache_wrapper
def get_all_docs(root):
    post_docs = get_post_docs(root)
    docs = post_docs + get_file_docs(root)
    category_docs = []
    category_filepaths = set()
    posts_count_db = {}
    for doc in post_docs:
        filepath = doc.get('filepath')
        if filepath:
            category_filepath = os.path.dirname(filepath)
            category_filepaths.add(category_filepath)
            posts_count_db[category_filepath] = posts_count_db.get(category_filepath, 0)+1
    for category_filepath in category_filepaths:
        if category_filepath == root:
            continue
        category_doc = filepath_to_file_doc(category_filepath, root=root)
        if category_doc:
            category_docs.append(category_doc)
            category_doc['posts_count'] = posts_count_db.get(category_filepath, 0)
    docs += category_docs
    docs = sort_docs_by_field(docs, field='-date')
    return docs


@cache_wrapper
def get_docs_map(root):
    docs_map  = {}
    docs = get_all_docs(root)
    for doc in docs:
        path = doc.get('path')
        if not path:
            continue
        docs_map[path] = doc
    return docs_map


@cache_wrapper
def get_all_docs_by_field(root, field, value, sort=None):
    all_docs = get_all_docs(root)
    docs = get_sub_docs_by_field(all_docs, field, value)
    docs = sort_docs_by_field(docs, field=sort)
    return docs


@cache_wrapper
def get_all_docs_by_types(root, types, sort=None):
    all_docs = get_all_docs(root)
    docs = []
    for doc_type in types:
        type_docs = get_sub_docs_by_field(all_docs, 'type', doc_type)
        if type_docs:
            docs += type_docs
    docs = sort_docs_by_field(docs, field=sort)
    return docs


def get_doc_by_path(path, root):
    relative_path = path.strip('/').strip().lower()
    docs_map = get_docs_map(root)
    doc = docs_map.get(relative_path)
    return doc



def has_doc(path, root):
    root = root.rstrip('/')
    relative_path = path.strip('/').strip()
    full_path = os.path.join(root, relative_path)
    if os.path.exists(full_path):
        return True
    else:
        return False

@cache_wrapper
def get_all_sub_docs_by_path(root, raw_docs, parent_path, is_direct=False):
    # 相当于 get_sub_docs_by_path 带 cache 的逻辑
    all_sub_docs = get_sub_docs_by_path(root, raw_docs, parent_path, is_direct=is_direct)
    return all_sub_docs


@cache_wrapper
def get_next_doc(current_doc, root, sort='-date', same_folder=False):
    if not current_doc or not isinstance(current_doc, dict):
        return None
    current_doc_filepath = current_doc.get('filepath')
    if not current_doc_filepath:
        return None
    doc_type = current_doc.get('type')
    if not doc_type:
        return None
    docs = get_all_docs_by_field(root, field='type', value=doc_type, sort=sort)
    if same_folder: # 位于当前同一个目录之内
        parent_path = os.path.dirname(current_doc_filepath)
        docs = get_sub_docs_by_path(root, docs, parent_path=parent_path, is_direct=True)
    hit_next = False
    for doc in docs:
        if doc.get('filepath') and doc.get('filepath') == current_doc.get('filepath'):
            hit_next = True
            continue
        if hit_next:
            return doc



