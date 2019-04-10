# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class Plum:

    """Packable/Unpacked Memory base class."""

    _nbytes = None

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent):
        raise NotImplementedError(f'{cls.__name__!r} does not support plum.unpack()')

    @classmethod
    def __pack__(cls, memory, offset, value, dump):
        raise NotImplementedError(f'{cls.__name__!r} does not support plum.pack()')

    def __baserepr__(self):
        raise NotImplementedError(f'{type(self).__name__!r} does not support repr()')

    def __repr__(self):
        return f'{type(self).__name__}({self.__baserepr__()})'
