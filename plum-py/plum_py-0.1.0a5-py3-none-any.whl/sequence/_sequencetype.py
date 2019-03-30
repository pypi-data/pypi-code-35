# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Sequence type metaclass."""

from .._plum import Plum
from .._plumtype import PlumType


class SequenceType(PlumType):

    """Sequence type metaclass.

    Create custom |Sequence| subclass. For example:

        >>> from plum.sequence import Sequence
        >>> from plum.int.little import UInt16, UInt8
        >>> class MySequence(Sequence, types=[UInt8, UInt16]):
        ...     pass
        ...
        >>>

    :param types: item types
    :type types: list of PlumType

    """

    def __new__(mcs, name, bases, namespace, types=None):
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, types=None):
        super().__init__(name, bases, namespace)

        if types is None:
            types = cls._types

        types = tuple(types)
        assert all(issubclass(t, Plum) for t in types)

        nbytes = 0

        for i, item_cls in enumerate(types):
            try:
                n = item_cls._nbytes
            except AttributeError:
                raise TypeError(f"sequence member {i} must be a Plum subclass")
            if n < 0:
                nbytes = -1
                break
            nbytes += n

        cls._types = types
        cls._nbytes = nbytes

    def __call__(cls, iterable=()):
        types = cls._types
        ntypes = len(types)

        if ntypes:
            self = list.__new__(cls, iterable)
            list.__init__(self, iterable)
            if len(self) != ntypes:
                invalid_length = (
                    f'{cls.__name__} accepts an iterable of length '
                    f'{len(cls._types)} but iterable of length {len(args)} given')
                raise ValueError(invalid_length)
            for i, (item, cls) in enumerate(zip(self, types)):
                if type(item) is not cls:
                    self[i] = cls(item)
        else:
            self = list.__new__(cls, iterable)
            list.__init__(self, iterable)
            for i, item in enumerate(self):
                if not isinstance(item, Plum):
                    raise TypeError(f'item {i} is not a packable type ')

        return self
