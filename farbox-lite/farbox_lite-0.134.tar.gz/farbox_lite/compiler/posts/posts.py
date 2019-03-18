#coding: utf8
from __future__ import absolute_import
import os
import operator
from farbox_markdown.util import is_a_markdown_file
from farbox_lite.compiler.utils import get_file_list
from farbox_lite.compiler.posts.post import filepath_to_post_doc


# 此处不处理缓存，在 API 的逻辑中, 有 update 的逻辑, 因为有 cache_uuid 的逻辑


def is_a_post_markdown_file(filepath):
    filename = os.path.split(filepath)[-1]
    if filename.lower().strip() in ['index.md', 'index.txt', 'index.mk', 'index.markdown']:
        # index as category
        return False
    if '/template/' in filepath:
        return False
    if not os.path.exists(filepath):
        return False
    elif os.path.isdir(filepath):
        return True
    else:
        return is_a_markdown_file(filepath)



def get_compiled_md_docs(root):
    md_docs = []
    md_filepaths = get_file_list(root, split=False, filter_func=is_a_post_markdown_file)
    for filepath in md_filepaths:
        doc = filepath_to_post_doc(filepath, root=root)
        if doc:
            md_docs.append(doc)
    md_docs = sorted(md_docs, key=operator.itemgetter('date'), reverse=True)
    return md_docs







