#coding: utf8
from __future__ import absolute_import
import os, datetime
from farbox_lite.compiler.posts.post import filepath_to_post_doc
from farbox_lite.compiler.utils import get_index_doc_filepath
from farbox_lite.utils import same_slash, get_relative_path


category_docs_cache = {}

def raw_get_category_doc(category_path, root=None):
    category_path = same_slash(category_path)
    index_doc_filepath = get_index_doc_filepath(category_path)
    relative_path = get_relative_path(category_path, root=root)
    path = relative_path.strip().lower()
    if index_doc_filepath and os.path.isfile(index_doc_filepath):
        category_doc = filepath_to_post_doc(index_doc_filepath, root=root)
    else:
        category_doc = {}
        category_doc['title'] = os.path.split(category_path)[-1]
    category_doc['type'] = 'folder'
    category_doc['path'] = path
    category_doc['filepath'] = category_path
    category_doc['url'] = '/category/%s' % path
    category_doc['date'] = datetime.datetime.fromtimestamp(os.path.getmtime(category_path))
    return category_doc




def get_category_doc(category_path, root=None):
    category_path = same_slash(category_path)
    if not root:
        root = os.path.dirname(category_path)
    if category_path in category_docs_cache:
        return category_docs_cache.get(category_path)
    else:
        category_doc = raw_get_category_doc(category_path, root=root)
        category_docs_cache[category_path] = category_doc
        return category_doc


def update_category_doc(category_path):
    category_doc = raw_get_category_doc(category_path)
    category_docs_cache[category_path] = category_doc


