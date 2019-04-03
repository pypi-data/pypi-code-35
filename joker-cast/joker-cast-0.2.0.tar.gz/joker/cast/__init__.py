#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import six

__version__ = '0.2.0'


def regular_cast(original, *attempts):
    """
    >>> regular_cast('12.3', int, float)
    12.3
    >>> regular_cast('12.3a', int, float)
    '12.3a'
    >>> regular_cast('12.3a', int, float, 0)
    0
    """
    for atmpt in attempts:
        if not callable(atmpt):
            return atmpt
        try:
            return atmpt(original)
        except (TypeError, ValueError):
            pass
    return original


def regular_lookup(dictlike, *keys):
    for key in keys:
        try:
            return dictlike[key]
        except LookupError:
            pass


def regular_attr_lookup(dictlike, *keys):
    for key in keys:
        try:
            return getattr(dictlike, key)
        except AttributeError:
            pass


def cache_lookup(dictlike, key, default, *args, **kwargs):
    try:
        return dictlike[key]
    except LookupError:
        pass
    if callable(default):
        value = default(*args, **kwargs)
    else:
        value = default
    dictlike[key] = value
    return value


def smart_cast(value, default):
    """
    Cast to the same type as `default`;
    if fail, return default
    :param value:
    :param default:
    :return:
    """
    func = type(default)
    try:
        return func(value)
    except (TypeError, ValueError):
        return default


def numerify(s):
    return regular_cast(s, int, float)


def want_bytes(s, **kwargs):
    """
    :param s: 
    :param kwargs: key word arguments passed to str.encode(..)
    :return: 
    """
    if not isinstance(s, six.binary_type):
        s = s.encode(**kwargs)
    return s


def want_unicode(s, **kwargs):
    """
    :param s: 
    :param kwargs: key word arguments passed to bytes.decode(..)
    :return: 
    """
    if not isinstance(s, six.text_type):
        return s.decode(**kwargs)
    return s


def want_str(s, **kwargs):
    """
    :param s:
    :param kwargs: key word arguments passed to s.decode(..)
    :return:
    """
    if not isinstance(s, str):
        return s.decode(**kwargs)
    return s


def namedtuple_to_dict(nt):
    from collections import OrderedDict
    fields = getattr(nt, '_fields')
    return OrderedDict(zip(fields, nt))


def represent(obj, params):
    """
    :param obj:
    :param params: a dict or list
    """
    c = obj.__class__.__name__
    if isinstance(params, dict):
        parts = ('{}={}'.format(k, repr(v)) for k, v in params.items())
    else:
        parts = ('{}={}'.format(k, repr(getattr(obj, k))) for k in params)
    s = ', '.join(parts)
    return '<{}({}) at {}>'.format(c, s, hex(id(obj)))
