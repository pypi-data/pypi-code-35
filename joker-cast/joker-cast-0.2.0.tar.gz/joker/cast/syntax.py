#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

"""Syntax sugar"""


def noop(*_, **__):
    pass


def default_func(*pargs, **_):
    """
    As a placeholder function, it works like lambda x: x.
    As a method of a class, it returns cls or self.
    :param pargs: positional arguments
    :param _: keyword arguments, ignored
    :return: 1st positional arguments
    """
    return pargs[0]


def adaptive_call(entry):
    """
    >>> import sys
    >>> entry = [print, ['a', 'b'], {'file': sys.stderr}]
    >>> adaptive_call(entry)

    :param entry: an iterable or a callable
    :return:
    """
    pargs = []
    kwargs = dict()
    if callable(entry):
        return entry()

    items = list(entry)
    if not items:
        return items
    if not callable(items[0]):
        raise TypeError('first item of entry must be a callable')

    for x in items[1:]:
        if isinstance(x, (list, tuple)):
            pargs.extend(x)
        elif isinstance(x, dict):
            kwargs.update(x)
        else:
            raise TypeError('params must be a tuple, list or dict')
    return items[0](*pargs, **kwargs)


def format_class_path(obj):
    if isinstance(obj, type):
        klass = obj
    else:
        klass = type(obj)
    m = getattr(klass, '__module__', None)
    q = getattr(klass, '__qualname__', None)
    n = getattr(klass, '__name__', None)
    name = q or n or ''
    if m:
        return '{}.{}'.format(m, name)
    return name


def format_function_path(func):
    import inspect
    from joker.cast import regular_attr_lookup

    if not inspect.ismethod(func):
        mod = getattr(func, '__module__', None)
        qualname = regular_attr_lookup(func, '__qualname__', '__name__')
        qualname = qualname or '<func>'
        if mod is None:
            return qualname
        else:
            return '{}.{}'.format(mod, qualname)
    klass_path = format_class_path(func.__self__)
    return '{}.{}'.format(klass_path, func.__name__)


def printerr(*args, **kwargs):
    import sys
    kwargs.setdefault('file', sys.stderr)
    pargs = []
    for a in args:
        if isinstance(a, BaseException):
            cn = a.__class__.__name__
            a = '{}: {}'.format(cn, a)
        pargs.append(a)
    print(*pargs, **kwargs)


def instanciate(cls):
    return cls()


def instanciate_with_foolproof(cls):
    """
    The return class can be called again without error
    """
    if '__call__' not in cls.__dict__:
        cls.__call__ = lambda x: x
    return cls()


class ConstantCallable(object):
    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)


_always_true = ConstantCallable(True)
_always_false = ConstantCallable(False)


class Void(object):
    """
    Act as 0, False, '', [] 
    """
    __bool__ = _always_false
    __nonzero__ = _always_false
    __add__ = default_func
    __sub__ = default_func
    __radd__ = default_func
    __rsub__ = default_func
    __round__ = default_func
    __truediv__ = default_func
    __floordiv__ = default_func
    __rtruediv__ = default_func
    __rfloordiv__ = default_func
    __rmul__ = default_func
    __gt__ = _always_false
    __ge__ = _always_false
    __lt__ = _always_false
    __le__ = _always_false
    __len__ = ConstantCallable(0)

    def __init__(self, symbol='-'):
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self.symbol))

    def __eq__(self, other):
        if isinstance(other, Void):
            return True
        return False


class Universe(object):
    __contains__ = _always_true
    __iter__ = ConstantCallable(tuple())


class Mu(object):
    __slots__ = ['value']

    # mutable value
    def __init__(self, value):
        self.value = value

    def __call__(self, value):
        self.value = value
        return self
