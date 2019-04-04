# -*- coding:utf-8 -*-

import six

__all__ = ['pick', 'defaults', 'deep_update']


def pick(d, keys, attr=False):
    if attr:
        result = {k: getattr(d, k) for k in keys if hasattr(d, k)}
    else:
        result = {k: d[k] for k in keys if k in d}
    return result


def defaults(d1, d2, inplace=True):
    result = d1 if inplace else d1.copy()
    for k, v in six.iteritems(d2):
        result.setdefault(k, v)
    return result


def deep_update(a, b):
    """deep version of dict.update()"""
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                deep_update(a[key], b[key])
            elif a[key] == b[key]:
                pass
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a
