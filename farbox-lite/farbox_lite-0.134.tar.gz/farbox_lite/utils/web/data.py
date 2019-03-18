#coding: utf8
from __future__ import absolute_import
import ujson as json
from farbox_lite.utils import smart_str


def json_dumps(obj, indent=None):
    # 主要是 mongodb 上的一些 obj
    if isinstance(obj, dict) and '_id' in obj:
        obj['_id'] = smart_str(obj['_id'])
    return json.dumps(obj, indent=indent)


def json_loads(raw_content):
    # 主要是 mongodb 上的一些 obj
    return json.loads(raw_content)




def make_tree(docs, kept_fields=None):
    if not docs:
        return docs

    #('title', 'position', '_images_count', 'images_count', 'posts_count', '_posts_count', 'real_path')
    if kept_fields and isinstance(kept_fields, (list, tuple)): # 为避免产生的 tree 包含太多数据，如果指定了 kept_fields
        kept_fields = set(list(kept_fields) + ['slash_number', 'path'])
        _docs = []
        for doc in docs:
            doc = {field:doc.get(field) for field in kept_fields}
            _docs.append(doc)
        docs = _docs

    leveled_docs = {}
    for doc in docs:
        slash_number = doc.get('slash_number') # 肯定是整数
        if slash_number is None:
            continue
        leveled_docs.setdefault(slash_number, []).append(doc)

    levels = leveled_docs.keys()
    if not levels:
        return docs

    min_level = min(levels)
    max_level = max(levels)

    level1_docs = leveled_docs.pop(min_level) # 先得到第一级的
    if min_level == max_level: # 没有多层结构
        return level1_docs

    parent_level_docs = level1_docs
    for level in range(min_level+1, max_level+1): # 得到后续的 level
        current_level_docs = leveled_docs.pop(level, [])
        if not current_level_docs:
            break
        parent_match_dict = {doc['path']:doc for doc in parent_level_docs}
        for doc in current_level_docs:
            parent_path = doc['path'].rsplit('/', 1)[0]
            parent_doc = parent_match_dict.get(parent_path)
            if parent_doc and isinstance(parent_doc, dict):
                children = parent_doc.setdefault('children', [])
                if doc not in children:
                    children.append(doc)
                #parent_doc.setdefault('children', []).append(doc)
        parent_level_docs = current_level_docs
    return level1_docs
