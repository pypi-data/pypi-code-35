# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import Optional


ATTR_NAME = '__cologler.attributes__'


class AttributeMetaClass(type):
    def __init__(self, name, bases, *args, **kwargs):
        allow_multiple = kwargs.pop('allow_multiple', None)
        if allow_multiple is not False:
            attr_bases = [b for b in bases if isinstance(b, AttributeMetaClass)]
            for base in attr_bases:
                if not base._allow_multiple:
                    if allow_multiple is None:
                        allow_multiple = False
                        break
                    else:
                        raise ValueError(f'attribute {self} cannot allow multiple (inherit from {base})')
        if allow_multiple is None:
            allow_multiple = True
        self._allow_multiple = allow_multiple

        super().__init__(name, bases, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        def attr_appender(obj):
            attrs_list = vars(obj).get(ATTR_NAME, None)
            if attrs_list is None:
                attrs_list = []
                setattr(obj, ATTR_NAME, attrs_list)
            if not self._allow_multiple:
                for attr_cls, factory in attrs_list:
                    if attr_cls == self:
                        raise SyntaxError(f'attribute {self} did not allow multiple')
            attrs_list.append(
                # (cls, factory)
                (self, lambda: type.__call__(self, *args, **kwargs))
            )
            return obj
        return attr_appender


class Attribute(metaclass=AttributeMetaClass):

    def __init_subclass__(cls, *args, **kwargs):
        # so we can add `allow_multiple` kwargs.
        pass

    @classmethod
    def _iter_attr_factorys(cls, obj, attr_type=None, *, inherit=False):
        if inherit and isinstance(obj, type):
            for subcls in obj.__mro__:
                yield from cls._iter_attr_factorys(subcls, attr_type, inherit=False)
        else:
            for attr_cls, factory in vars(obj).get(ATTR_NAME, ()):
                if attr_type is None or issubclass(attr_cls, attr_type):
                    yield factory

    @classmethod
    def _iter_attrs(cls, obj, attr_type=None, *, inherit=False):
        for factory in cls._iter_attr_factorys(obj, attr_type, inherit=inherit):
            yield factory()

    @classmethod
    def get_attrs(cls, obj, attr_type=None, *, inherit=False):
        '''
        gets the all attrs from `obj` which match `attr_type`.
        '''
        return tuple(cls._iter_attrs(obj, attr_type, inherit=inherit))

    @classmethod
    def get_attr(cls, obj, attr_type, *, inherit=False):
        '''
        gets the first attr from `obj` which match `attr_type`.
        '''
        if attr_type is None:
            raise ValueError
        for attr in cls._iter_attrs(obj, attr_type, inherit=inherit):
            return attr
        return None

    @classmethod
    def has_attr(cls, obj, attr_type, *, inherit=False):
        '''
        check whether the `obj` has some attr.
        '''
        for factory in cls._iter_attr_factorys(obj, attr_type, inherit=inherit):
            return True
        return False
