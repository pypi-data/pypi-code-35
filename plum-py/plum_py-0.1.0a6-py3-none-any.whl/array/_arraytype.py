# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from functools import reduce
from operator import mul

from .._utils import calcsize, SizeError
from .._plum import Plum
from .._plumtype import PlumType

GREEDY_DIMS = (None,)


class ArrayInitError(Exception):
    pass


class ArrayType(PlumType):

    """Array type metaclass.

    Create custom |Array| subclass. For example:

        >>> from plum.array import Array
        >>> from plum.int.little import UInt16
        >>> class MyArray(Array, item_cls=UInt16, dims=(10,)):
        ...     pass
        ...
        >>>

    :param PlumType item_cls: array item type
    :param dims: array dimension
    :type dims: tuple of int or None

    """

    def __new__(mcs, name, bases, namespace, item_cls=None, dims=None):
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, item_cls=None, dims=None):
        super().__init__(name, bases, namespace)

        if item_cls is None:
            item_cls = cls._item_cls

        assert issubclass(item_cls, Plum)

        if dims is None:
            dims = cls._dims

        dims = tuple(None if d is None else int(d) for d in dims)
        if None in dims:
            nbytes = None
        else:
            assert all(d > 0 for d in dims)

            try:
                nbytes = calcsize(item_cls)
            except SizeError:
                nbytes = None
            else:
                nbytes *= reduce(mul, dims)

        cls._dims = dims
        cls._item_cls = item_cls
        cls._nbytes = nbytes

    def _make_instance(cls, iterable, dims=None, idims=0, index=''):
        if dims is None:
            dims = list(cls._dims)
            clsname = cls.__name__
        else:
            clsname = 'Array'

        this_dim = dims[idims]

        if idims < len(dims) - 1:
            item_cls = cls
            if iterable is None:
                if this_dim is None:
                    iterable = []
                else:
                    iterable = [None] * this_dim
        else:
            item_cls = cls._item_cls
            if iterable is None:
                if this_dim is None:
                    iterable = []
                else:
                    iterable = [item_cls() for _ in range(this_dim)]

        self = list.__new__(cls, iterable)
        list.__init__(self, iterable)

        if this_dim is None:
            dims[idims] = len(self)
        elif len(self) != this_dim:
            invalid_dimension = (
                f'expected length of item{index} to be {this_dim} '
                f'but instead found {len(self)}')
            raise ArrayInitError(invalid_dimension)

        try:
            equivalent = item_cls.__equivalent__
        except AttributeError:
            equivalent = item_cls

        for i, item in enumerate(self):
            if not isinstance(item, equivalent):
                try:
                    if item_cls is cls:
                        item = item_cls._make_instance(item, dims, idims + 1, index + f'[{i}]')
                    else:
                        item = item_cls(item)
                    list.__setitem__(self, i, item)
                except ArrayInitError:
                    # allow lowest level one to propagate
                    raise
                except Exception as exc:
                    raise ArrayInitError(
                        f"unexpected {type(exc).__name__!r} "
                        f"exception occurred during array initialization, "
                        f"item{index}[{i}] did not successfully convert to a "
                        f"{item_cls.__name__!r}, original exception "
                        f"traceback appears above this exception's traceback"
                    ).with_traceback(exc.__traceback__)

        self._dims = tuple(dims[idims:])
        self._clsname = clsname

        return self

    def __call__(cls, iterable=None):
        return cls._make_instance(iterable)
