# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Structure type."""

from .._plum import Plum
from ._sequencetype import SequenceType


class Sequence(list, Plum, metaclass=SequenceType):

    """Interpret memory bytes as a list of uniquely typed items.

    :param iterable iterable: items

    """

    # filled in by metaclass
    _types = ()
    _nbytes = 0

    @classmethod
    def __unpack__(cls, memory, dump, parent):
        self = list.__new__(cls)
        list.__init__(self)

        if dump:
            dump.cls = cls

            for i, item_cls in enumerate(cls._types):
                subdump = dump.add_level(access=f'[{i}]')
                list.append(self, item_cls.__unpack__(memory, subdump, self))
        else:
            for i, item_cls in enumerate(cls._types):
                list.append(self, item_cls.__unpack__(memory, None, self))

        return self

    @classmethod
    def __pack__(cls, items, dump):
        if not isinstance(items, cls):
            items = cls(items)

        if dump:
            dump.cls = cls

            for i, item in enumerate(items):
                yield from item.__pack__(item, dump.add_level(access=f'[{i}]'))
        else:
            for item in items:
                yield from item.__pack__(item, dump)

    def __str__(self):
        return f'[{", ".join([item.__baserepr__() for item in self])}]'

    __baserepr__ = __str__

    __repr__ = Plum.__repr__

    def __setitem__(self, index, item):
        cls = type(self)
        types = cls._types

        if isinstance(index, slice):
            items = list(item)
            if types:
                types = types[index]
                if len(items) != len(types):
                    raise ValueError(f'{cls.__name__!r} object does not support resizing')
                for i, (item, item_cls) in enumerate(items, types):
                    if type(item) is not item_cls:
                        items[i] = item_cls(item)
            else:
                for i, item in enumerate(items):
                    if not isinstance(item, Plum):
                        raise TypeError(f"slice item {i} must be a Plum subclass")
            item = items

        elif types:
            item_cls = types[index]
            if type(item) is not item_cls:
                item = item_cls(item)

        else:
            if not isinstance(item, Plum):
                raise TypeError(f"item must be a Plum subclass")

        list.__setitem__(self, index, item)

    def append(self, item):
        cls = type(self)
        types = cls._types

        if types:
            raise ValueError(f'{cls.__name__!r} object does not support resizing')

        if not isinstance(item, Plum):
            raise TypeError(f"item must be a Plum subclass")

        list.append(self, item)

    def clear(self):
        cls = type(self)
        types = cls._types

        if types:
            raise ValueError(f'{cls.__name__!r} object does not support resizing')

        list.clear(self)

    def extend(self, iterable):
        cls = type(self)
        types = cls._types

        if types:
            raise ValueError(f'{cls.__name__!r} object does not support resizing')

        for i, item in enumerate(iterable):
            if isinstance(item, Plum):
                list.append(self, item)
            else:
                raise TypeError(f"item {i} must be a Plum subclass")

    def insert(self, index, item):
        cls = type(self)
        types = cls._types

        if types:
            raise ValueError(f'{cls.__name__!r} object does not support resizing')

        if not isinstance(item, Plum):
            raise TypeError(f"item must be a Plum subclass")

        list.insert(self, index, item)

    def pop(self, index=-1):
        cls = type(self)
        types = cls._types

        if types:
            raise ValueError(f'{cls.__name__!r} object does not support resizing')

        return list.pop(self, index)

    def remove(self, value):
        cls = type(self)
        types = cls._types

        if types:
            raise ValueError(f'{cls.__name__!r} object does not support resizing')

        list.remove(self, value)
