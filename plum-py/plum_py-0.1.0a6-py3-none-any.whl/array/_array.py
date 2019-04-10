# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .._plum import Plum
from .._utils import getbytes
from ..int.little import UInt8
from ._arraytype import ArrayType, GREEDY_DIMS


class Array(list, Plum, metaclass=ArrayType):

    """Interpret memory bytes as a list of uniformly typed items.

    :param iterable iterable: items

    """

    # filled in by metaclass
    _dims = GREEDY_DIMS
    _item_cls = UInt8
    _nbytes = None

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent, dims=None, outer_level=True):

        if dims is None:
            dims = cls._dims

        if dump and outer_level:
            dump.cls = cls

        self = list()

        if dims == GREEDY_DIMS:
            chunk, offset, limit = getbytes(memory, offset, cls._nbytes, limit, dump, cls)

            _offset = 0
            _limit = None
            _len_chunk = len(chunk)

            i = 0
            item_cls = cls._item_cls
            if dump:
                dump.memory = b''
                while _offset < _len_chunk:
                    subdump = dump.add_level(access=f'[{i}]')
                    item, _offset, _limit = item_cls.__unpack__(chunk, _offset, _limit, subdump, self)
                    self.append(item)
                    i += 1
            else:
                while _offset < _len_chunk:
                    item, _offset, _limit = item_cls.__unpack__(chunk, _offset, _limit, None, self)
                    self.append(item)
                    i += 1
        elif None in dims:
            raise RuntimeError('unpack does not support multidimensional greedy arrays')
        else:
            itemdims = dims[1:]
            if dump:
                if itemdims:
                    for i in range(dims[0]):
                        subdump = dump.add_level(access=f'[{i}]')
                        item, offset, limit = cls.__unpack__(
                            memory, offset, limit, subdump, self, itemdims, False)
                        self.append(item)
                else:
                    item_cls = cls._item_cls
                    for i in range(dims[0]):
                        subdump = dump.add_level(access=f'[{i}]')
                        item, offset, limit = item_cls.__unpack__(
                            memory, offset, limit, subdump, self)
                        self.append(item)
            else:
                if itemdims:
                    for i in range(dims[0]):
                        item, offset, limit = cls.__unpack__(
                            memory, offset, limit, None, self, itemdims, False)
                        self.append(item)
                else:
                    item_cls = cls._item_cls
                    for i in range(dims[0]):
                        item, offset, limit = item_cls.__unpack__(
                            memory, offset, limit, None, self)
                        self.append(item)

        return self, offset, limit

    @classmethod
    def __pack__(cls, memory, offset, items, dump, dims=None, outer_level=True):
        if not isinstance(items, cls):
            items = cls(items)

        if dims is None:
            dims = items._dims

        itemdims = dims[1:]

        if dump:
            if outer_level:
                dump.cls = cls

            if itemdims:
                for i, item in enumerate(items):
                    offset = item.__pack__(memory, offset, item, dump.add_level(access=f'[{i}]'), itemdims, False)
            else:
                item_cls = cls._item_cls
                for i, item in enumerate(items):
                    offset = item_cls.__pack__(memory, offset, item, dump.add_level(access=f'[{i}]'))
        else:
            if itemdims:
                for item in items:
                    offset = item.__pack__(memory, offset, item, None, itemdims, False)
            else:
                item_cls = cls._item_cls
                for item in items:
                    offset = item_cls.__pack__(memory, offset, item, None)

        return offset

    def __str__(self):
        lst = []
        for item in self:
            try:
                r = item.__baserepr__
            except AttributeError:
                r = item.__repr__

            lst.append(r())

        return f"[{', '.join(lst)}]"


    __baserepr__ = __str__

    def __repr__(self):
        return f'{self._clsname}({self.__baserepr__()})'

    def __setitem__(self, index, item):
        # FUTURE: add mechanism to keep track of index for arrays
        cls = type(self)

        if isinstance(index, slice):
            items = list(item)
            replace_count = len(self[index])
            if len(items) != replace_count:
                raise ValueError(f'{cls.__name__!r} object does not support resizing')
            for i, item in zip(range(len(self))[index], items):
                self[i] = item
        else:
            item_dims = self._dims[1:]
            if item_dims:
                if (type(item) is not cls) or (item._dims != item_dims):
                    item = cls._make_instance(item, item_dims)
            else:
                if type(item) is not cls._item_cls:
                    item = cls._item_cls(item)

            list.__setitem__(self, index, item)

    def append(self, item):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')

    def clear(self):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')

    def extend(self, iterable):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')

    def insert(self, index, item):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')

    def pop(self, index=-1):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')

    def remove(self, value):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')
