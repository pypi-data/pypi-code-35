#coding: utf8
from __future__ import absolute_import
import os
import re
from farbox_lite.utils import same_slash, smart_unicode



def get_index_doc_filepath(folder_path):
    md_index_filenames = ['index.md', 'index.txt', 'index.mk', 'index.markdown']
    for filename in md_index_filenames:
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            return filepath
    return None # at last



def is_real(path):
    # 主要是判断是否真实的文档，还是软链，或者软链下的目录内
    path = same_slash(path)
    if not os.path.exists(path):
        return False
    parts = path.split('/')
    for i in range(len(parts)):
        if i:
            _path = '/'.join(parts[:-i])
        else:
            _path = path
        if os.path.islink(_path):
            return False
    return True


def is_a_hidden_path(path):
    path = same_slash(path)
    if re.search('(^|/)(\.|~$)', path):
        return True
    elif re.search(r'~\.[^.]+$', path):
        return True
    elif path.endswith('~'):
        return True
    else:
        return False


def is_a_empty_folder(folder_path, include_empty_sub_folder=True):
    if not os.path.isdir(folder_path):
        return False
    for sub_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, sub_name)
        if not is_a_hidden_path(file_path) and os.path.exists(file_path):
            if os.path.isdir(file_path) and is_a_empty_folder(file_path) and include_empty_sub_folder:
                # 如果包含的目录也是空目录，不处理， continue
                continue
            return False
    # at last
    return True



def get_file_list(root_path, split=False, filter_func=None, parent_filter_func=None):
    root_path = same_slash(root_path)
    file_paths = []
    just_files = []
    just_folders = []
    if not os.path.isdir(root_path): # 根目录不存在，不处理
        pass
    else:
        for parent, folders, files in os.walk(root_path):
            if is_a_hidden_path(parent):
                continue
            elif not is_real(parent): # link类型的不处理
                continue

            if parent_filter_func:
                if not parent_filter_func(parent): # parent 不需要处理的, 直接 ignore
                    continue

            for filename in files:
                file_path = os.path.join(parent, filename)
                if not is_a_hidden_path(file_path) and is_real(file_path):
                    #relative_path = file_path.replace(root_path, '').strip('/')
                    file_paths.append(file_path)
                    just_files.append(file_path)

            for filename in folders:
                file_path = os.path.join(parent, filename)
                if not is_a_hidden_path(file_path) and is_real(file_path):
                    #relative_path = file_path.replace(root_path, '').strip('/')
                    file_paths.append(file_path)
                    just_folders.append(file_path)
    if filter_func:
        file_paths = [path for path in file_paths if filter_func(path)]
        just_folders = [path for path in just_folders if filter_func(path)]

    if not split:
        return file_paths
    else:
        return just_folders, just_files


def get_sort_and_name_from_filepath(filepath):
    filename = os.path.split(filepath)[-1]
    if os.path.isdir(filepath):
        name = filename
    else:
        name = os.path.splitext(filename)[0]
    name = name.strip()
    sort = -1
    if re.match(r'\d+ ', name) or re.match(r'\d+\.\d+ ', name):
        sort, name = name.split(' ', 1)
        sort = sort.strip()
        if '.' in sort:
            try: sort = float(sort)
            except: pass
        else:
            try: sort = int(sort)
            except: pass
    return sort, name



