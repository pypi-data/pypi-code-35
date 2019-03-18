#coding: utf8
from __future__ import absolute_import
import os
import datetime
from farbox_lite.compiler.utils import get_file_list
from farbox_lite.utils import get_relative_path
from farbox_lite.utils.mime import guess_type
import ujson as json

from .utils import is_real, is_a_hidden_path, get_sort_and_name_from_filepath

from .category import get_category_doc

# 此处不处理缓存，在 API 的逻辑中, 有 update 的逻辑, 因为有 cache_uuid 的逻辑


def filepath_to_file_doc(filepath, root=None):
    if not os.path.exists(filepath):
        return {}
    if not root:
        root = os.path.dirname(filepath)

    if os.path.isdir(filepath):
        # folder 直接进行添加处理的逻辑
        category_doc = get_category_doc(filepath, root=root)
        return category_doc

    relative_path = get_relative_path(filepath, root=root).strip().lower()
    slash_number = relative_path.count('/')
    mime_type = guess_type(filepath, 'application/octet-stream')
    file_type = 'file'
    if mime_type.startswith('image/'):
        file_type = 'image'

    sort, name = get_sort_and_name_from_filepath(filepath)
    just_name = os.path.splitext(name)[0]
    title = name
    if file_type == 'image':
        title = just_name

    date = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))


    data = {}
    if relative_path.endswith('.json'):
        with open(filepath, 'rb') as f:
            raw_content = f.read()
        try:
            data = json.loads(raw_content)
        except:
            pass

    doc = dict(
        title = title,
        path = relative_path,
        filepath = filepath, # 记录完整的路径，后续 send_file 用的
        type = file_type,
        date = date,
        sort = sort,
        slash_number = slash_number,
        position = sort,

        data = data,
        id = filepath,
    )

    return doc


# todo 要不要把 category 也处理了, 放在 list 中?


def should_treat_as_a_file(filepath):
    l_filepath = filepath.lower()
    if '/template/' in l_filepath:
        return False
    if not os.path.isfile(filepath):
        return False
    if not is_real(filepath):
        return False
    if is_a_hidden_path(filepath):
        return False
    # at last
    return True



def get_compiled_file_docs(root):
    file_docs = []
    filepaths = get_file_list(root, split=False, filter_func=should_treat_as_a_file)
    for filepath in filepaths:
        doc = filepath_to_file_doc(filepath)
        if not doc:
            continue
        else:
            file_docs.append(doc)
    return file_docs





