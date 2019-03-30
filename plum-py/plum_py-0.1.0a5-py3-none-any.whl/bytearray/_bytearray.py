# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .._plum import Plum
from .._utils import getbytes
from ._bytearraytype import ByteArrayType


class ByteArray(bytearray, Plum, metaclass=ByteArrayType):

    """Interpret memory bytes as a byte array.

    .. code-block:: none

        ByteArray(iterable_of_ints) -> bytes array
        ByteArray(string, encoding[, errors]) -> bytes array
        ByteArray(bytes_or_buffer) -> mutable copy of bytes_or_buffer
        ByteArray(int) -> bytes array of size given by the parameter initialized with null bytes
        ByteArray() -> empty bytes array

    """

    # filled in by metaclass
    _nbytes = None

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent):
        chunk, offset, limit = getbytes(memory, offset, cls._nbytes, limit, dump, cls)

        if dump:
            dump.memory = b''
            for i in range(0, len(chunk), 16):
                subchunk = chunk[i:i + 16]
                subdump = dump.add_level(access=f'[{i}:{i + len(subchunk)}]')
                subdump.value = str(list(subchunk))
                subdump.memory = subchunk

        return bytearray(chunk), offset, limit

    @classmethod
    def __pack__(cls, value, dump):

        try:
            dump.cls = cls
        except AttributeError:
            pass  # must be None

        if not isinstance(value, bytes):
            value = bytes(value)

        nbytes = cls._nbytes
        if nbytes is not None and len(value) != nbytes:
            raise ValueError(
                f'expected length to be {nbytes} but instead found {len(value)}')

        if dump:
            for i in range(0, len(value), 16):
                chunk = value[i:i + 16]
                subdump = dump.add_level(access=f'[{i}:{i + len(chunk)}]')
                subdump.value = str(list(chunk))
                subdump.memory = chunk

        yield value

    def __baserepr__(self):
        return bytearray.__repr__(self).split('(', 1)[1][:-1]

    __repr__ = Plum.__repr__
