#coding: utf8
from __future__ import absolute_import
from collections import OrderedDict
from farbox_lite.utils import get_md5, smart_str, get_relative_path
from farbox_lite.utils.functional import curry
import copy

class LimitedSizeDict(OrderedDict):
    def __init__(self, *args, **kwds):
        self.size_limit = None # default，实际上不会有 limited 的效果
        fields = ['size_limit', 'limit', 'size', 'max', 'max_size']
        for field in fields:
            field_value = kwds.pop(field, None) # 避免这些字段成为字段的初始对象
            if field_value:
                self.size_limit = field_value
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value, *args, **kwargs):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=True)


class cached(object):
    """
    @cached(get_cache_key_func)
    def xxx(xxxxx):
        xxxxxxx
    """
    def __init__(self, cache_key_func):
        self.cached_function_responses = LimitedSizeDict(size=1000)
        self.cache_key_func = cache_key_func


    def __call__(self, func):
        prefix_cache_key = self.cache_key_func()
        def _func(*func_args, **func_kwargs):
            base_cache_key = '%s-%s' % (prefix_cache_key, id(func))
            if func_args or func_kwargs:
                # 可能第一个变量传入的是 self 这种实例对象
                func_args_s_list = [] # 形成缓存key用的一个list
                for func_arg in func_args:
                    if not isinstance(func_arg, (str, unicode, dict, tuple, list, bool, int, float)):
                        func_args_s_list.append(smart_str(id(func_arg)))
                    else:
                        if isinstance(func_arg, dict) and func_arg.get('id'):
                            func_args_s_list.append(func_arg.get('id'))
                        else:
                            func_args_s_list.append(func_arg)
                if func_kwargs:
                    func_kwargs = copy.copy(func_kwargs)
                    for k, v in func_kwargs.items():
                        if v and isinstance(v, dict) and v.get('id'):
                            func_kwargs[k] = v.get('id')
                var_key = '-'.join(func_args_s_list) + smart_str(func_kwargs)
                var_md5 = get_md5(var_key)
                cache_key = '%s-%s' % (base_cache_key, var_md5)
            else:
                cache_key = base_cache_key

            if cache_key in self.cached_function_responses:
                cached_data = self.cached_function_responses[cache_key]
                return cached_data
            else:

                result = func(*func_args, **func_kwargs)
                self.cached_function_responses[cache_key] = result
                return result
        return _func



def get_sub_docs_by_path(root, raw_docs, parent_path, is_direct=False):
    if parent_path.startswith('/'):
        parent_relative_path = get_relative_path(parent_path, root=root).lower()
    else:
        parent_relative_path = parent_path.strip().strip('/').lower()
    parent_slash_number = parent_relative_path.count('/')
    docs = []
    for doc in raw_docs:
        doc_path = doc.get('path')
        if not doc_path:
            continue
        doc_slash_number = doc_path.count('/')
        if not doc_path.startswith('%s/'%parent_relative_path):
            continue
        if is_direct:
            if doc_slash_number != parent_slash_number+1:
                continue
        docs.append(doc)
    return docs


def get_sub_docs_by_field(raw_docs, field, value):
    docs = []
    for doc in raw_docs:
        if not isinstance(doc, dict):
            continue
        if doc.get(field) == value:
            docs.append(doc)
    return docs



def sort_key_func(field, doc):
    return doc.get(field)


def sort_docs_by_field(raw_docs, field=None):
    if not field:
        return raw_docs
    field = field.strip()
    if field.startswith('-'):
        reverse = True
    else:
        reverse = False
    field = field.strip('-').strip()
    sorted_docs = sorted(raw_docs, key=curry(sort_key_func, field), reverse=reverse)
    return sorted_docs

