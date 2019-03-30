# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Interpret memory bytes as a floating point number."""

from struct import Struct

from .._plum import Plum
from .._utils import getbytes
from ._floattype import FloatType


class Float(float, Plum, metaclass=FloatType):

    """Interpret memory bytes as a floating point number.

    :param x: value
    :type x: number or str

    """

    _byteorder = 'little'
    _nbytes = 4
    _pack = Struct('<f').pack
    _unpack = Struct('<f').unpack

    __equivalent__ = float

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent):
        chunk, offset, limit = getbytes(memory, offset, cls._nbytes, limit, dump, cls)

        self = cls._unpack(chunk)[0]

        if dump:
            dump.value = self

        return self, offset, limit

    @classmethod
    def __pack__(cls, value, dump):
        try:
            dump.cls = cls
        except AttributeError:
            pass  # must be None

        bytes_ = cls._pack(value)

        if dump:
            dump.value = value
            dump.memory = bytes_

        yield bytes_

    __baserepr__ = float.__repr__

    __repr__ = Plum.__repr__
