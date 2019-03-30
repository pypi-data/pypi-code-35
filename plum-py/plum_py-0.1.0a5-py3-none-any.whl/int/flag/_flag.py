# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Integer flag type."""

import enum

from ..._utils import getbytes
from .._int import Int
from ._flagtype import FlagType


class Flag(Int, enum.Flag, metaclass=FlagType):
    # pylint: disable=too-many-ancestors

    """Interpret memory bytes as an integer with bit flags.

    :param x: value
    :type x: number or str
    :param int base: base of x when x is ``str``

    """

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        # pylint: disable=protected-access
        self._value_ = int(self)
        return self

    def __getattr__(self, name):
        try:
            member = type(self)[name.upper()]
        except KeyError:
            object.__getattribute__(self, name)
        # pylint: disable=protected-access
        return bool(self._value_ & member._value_)

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent):
        chunk, offset, limit = getbytes(memory, offset, cls._nbytes, limit, dump, cls)

        self = cls.from_bytes(chunk, cls._byteorder, signed=cls._signed)

        if dump:
            dump.value = self
            cls._add_flags_to_dump(self, dump)

        return self, offset, limit

    @classmethod
    def _add_flags_to_dump(cls, value, dump):
        dump.value = int(value)

        for member in cls:
            row = dump.add_level(
                access='.' + member.name.lower(),
                bits=(int(member.bit_length() - 1), 1))
            row.value = str(bool(dump.value & member))
            row.cls = bool

    # pylint: disable=protected-access
    _missing_ = classmethod(enum.IntFlag._missing_.__func__)
    _create_pseudo_member_ = classmethod(
        enum.IntFlag._create_pseudo_member_.__func__)

    __or__ = enum.IntFlag.__or__
    __and__ = enum.IntFlag.__and__
    __xor__ = enum.IntFlag.__xor__

    __ror__ = enum.IntFlag.__ror__
    __rand__ = enum.IntFlag.__rand__
    __rxor__ = enum.IntFlag.__rxor__

    def __invert__(self):
        result = self.__class__(~self._value_ & self._max)
        return result
