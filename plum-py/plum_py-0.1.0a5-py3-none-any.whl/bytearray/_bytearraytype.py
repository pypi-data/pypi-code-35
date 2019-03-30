# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import codecs

from .._plumtype import PlumType


class ByteArrayType(PlumType):

    """ByteArray type metaclass.

    Create custom |ByteArray| subclass. For example:

        >>> from plum.bytearray import ByteArray
        >>> class ByteArray1(ByteArray, nbytes=4):
        ...     pass
        ...
        >>>

    :param int nbytes: size in number of bytes

    """

    def __new__(mcs, name, bases, namespace, nbytes=None):
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, nbytes=None):
        super().__init__(name, bases, namespace)

        if nbytes is None:
            nbytes = cls._nbytes
        else:
            assert nbytes > 0

        cls._nbytes = nbytes
