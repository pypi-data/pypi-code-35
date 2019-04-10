# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Integer enumeration type."""

import enum

from ..._utils import getbytes
from .._int import Int
from ._enumtype import EnumType


class Enum(Int, enum.Enum, metaclass=EnumType):

    """Interpret memory bytes as an integer enumerated constants.

    :param x: value
    :type x: number or str
    :param int base: base of x when x is ``str``

    """

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        # pylint: disable=protected-access
        self._value_ = int(self)
        return self

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent):
        chunk, offset, limit = getbytes(memory, offset, cls._nbytes, limit, dump, cls)

        self = cls.from_bytes(chunk, cls._byteorder, signed=cls._signed)

        if dump:
            dump.value = self
            cls._add_flags_to_dump(self, dump)

        return self, offset, limit
