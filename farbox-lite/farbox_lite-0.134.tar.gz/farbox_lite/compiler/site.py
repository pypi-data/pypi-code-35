#coding: utf8
from __future__ import absolute_import
import os
from farbox_lite.compiler.posts.post import filepath_to_post_doc
from farbox_lite.compiler.utils import get_index_doc_filepath
from farbox_lite.compiler.templates import get_template_resources
from farbox_lite.utils import same_slash


site_docs_cache = {}


def get_site_doc_by_filepath_directly(site_path):
    # 没有 index.md .etc 时, 直接构建的
    if not os.path.isdir(site_path):
        return {}
    folder_name = os.path.split(site_path)[-1]
    site_doc = dict(
        title = folder_name,
        domains = [folder_name.strip().lower()],
        filepath = site_path
    )
    return site_doc



def raw_get_site_doc(site_path):
    site_path = same_slash(site_path)
    if not os.path.isdir(site_path):
        return {}
    index_doc_filepath = get_index_doc_filepath(site_path)
    if not index_doc_filepath:
        site_doc = get_site_doc_by_filepath_directly(site_path)
    else:
        site_doc = filepath_to_post_doc(index_doc_filepath)
    site_doc['type'] = 'site'
    site_doc['filepath'] = site_path
    site_doc['configs'] = site_doc.get('metadata') or {}
    site_doc['template_resources'] = get_template_resources(site_path)
    return site_doc



def get_site_doc(site_path):
    site_path = same_slash(site_path)
    if site_path in site_docs_cache:
        return site_docs_cache.get(site_path)
    else:
        site_doc = raw_get_site_doc(site_path)
        site_docs_cache[site_path] = site_doc
        return site_doc


def update_site_doc(site_path):
    site_doc = raw_get_site_doc(site_path)
    site_docs_cache[site_path] = site_doc


