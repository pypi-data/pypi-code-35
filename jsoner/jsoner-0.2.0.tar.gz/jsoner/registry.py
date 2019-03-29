# -*- coding: utf-8 -*-

import pydoc
import typing as T
from collections import UserDict
from typing import Callable


class Registry(UserDict):
    """
    The :class:`Registry` allows simple key-value mapping. Each key is
    only allowed once in the registry.

    Usage::
        >>> from jsoner.registry import Registry
        >>> reg = Registry()

        >>> reg.add('foo', 42)
        >>> reg.get('foo')
        42

        >>> reg = Registry()
        >>> @reg.register('foo')
        ... def foo():
        ...     return 42

        >>> reg.get('foo')()
        42

    """

    @property
    def registry(self) -> dict:
        """
        Returns
        -------
        dict
            The registry dictionary.
        """
        return self.data

    def add(self, key: T.Any, value: T.Any) -> None:
        """
        Adds the key, value pair to the registry. Each key is only
        allowed once in the registry.

        :param key:
        :param value:
        :return:
        :raise KeyError: If the key is already in the registry.
        """
        if key in self.data:
            msg = 'Key `{}` is already in the registry!'.format(key)
            raise KeyError(msg)

        self.data[key] = value

    def register(self, key: T.Any) -> Callable:
        """
        :meth:`register` servers as a decorator to add functions to the
        registry.

        :param key:
        :return: Callable
        """

        def inner(func):
            self.add(key, func)
            return inner

        return inner

    def __contains__(self, item) -> bool:
        in_regestry = super().__contains__(item)
        if not in_regestry:
            try:
                self.__getitem__(item)
                in_regestry = True
            except KeyError:
                pass
        return in_regestry


class SubclassRegistry(Registry):
    """
    The :class:`SubclassRegistry` will not only map a single key-value pair,
    but will also retrieve a value if the key, or the type of the key
    is a Subclass of any of the keys.

    If the key, seems to be an object, which could potentially be in the
    registry but is not found at once, the :class:`SubclassRegistry` will
    search the mro of the object and check against its entries.

    Usage::
        >>> from jsoner.registry import SubclassRegistry
        >>> reg = SubclassRegistry()

        >>> reg.add(dict, 42)
        >>> reg.get(dict)
        42

        >>> class A:
        ...     pass
        >>> class B(A):
        ...     pass

        >>> reg.add(A, 'bar')
        >>> reg.get(B)
        'bar'
        >>> reg.get(B())
        'bar'

        The registration also works with strings

        >>> from datetime import datetime
        >>> reg.add('datetime.datetime', 'foo')
        >>> reg.get(datetime)
        'foo'

        >>> reg.get('dict')
        42

        Furthermore it can be used as decorator.

        >>> reg = SubclassRegistry()
        >>> @reg.register(A)
        ... def foo():
        ...     return 42
        >>> reg.get(A)()
        42
        >>> reg.get(B)()
        42

    """

    def __getitem__(self, key: T.Any) -> T.Any:
        """
        Returns the registered function for the given object or type
        :param key:
        :return:
        """
        msg = 'Key `{}` not found in registry.'.format(key)

        value = self.data.get(key)

        if value is not None:
            return value

        if isinstance(key, str):
            try:
                obj_type = import_object(key)
            except ImportError:
                raise KeyError(msg)

        # get the object type
        elif isinstance(key, type):
            obj_type = key
        else:
            obj_type = key.__class__

        try:
            return self.data[obj_type]
        except KeyError:
            pass

        try:
            mro = obj_type.mro()
        except AttributeError:
            raise KeyError(msg)

        # walk mro
        for cls in mro:
            for registered_cls, value in self.data.items():
                if isinstance(registered_cls, str):
                    try:
                        registered_cls = import_object(registered_cls)
                    except ImportError:
                        continue
                if cls is registered_cls:
                    return value
        else:
            raise KeyError(msg)


def import_object(path: str) -> T.Any:
    """
    Import the object or raise an :exc:`ImportError` if the object is not
    found.

    :param path: The path to the object.
    :return: The imported object.
    :raise ImportError:
    """
    t = pydoc.locate(path)
    if t is None:
        msg = 'Object `{}` could not be found'.format(path)
        raise ImportError(msg)
    return t


encoders = SubclassRegistry()
"""
:attr:`encoders` contains a mapping of types and encoding functions. An
encoding function takes an argument and returns a value which should be
json serializable. The function which is defined in :attr:`decoders`
must be able to recreate the object from the returned value.
"""

decoders = SubclassRegistry()
"""
:attr:`decoders` contains the inverse functions-type mapping for
:attr:`encoders`.
"""
