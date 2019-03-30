# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Float type metaclass."""

from struct import Struct

from .._plumtype import PlumType


FORMAT_CODES = {2: 'e', 4: 'f', 8: 'd'}
ENDIAN_CODES = {'big': '>', 'little': '<'}


class FloatType(PlumType):

    """Float type metaclass.

    Create custom |Float| subclass. For example:

        >>> from plum.float import Float
        >>> class Float32(Float, nbytes=4, byteorder='big'):
        ...     pass
        ...
        >>>

    :param int nbytes: number of memory bytes
    :param str byteorder: ``'big'`` or ``'little'``

    """

    def __new__(mcs, name, bases, namespace, nbytes=None, byteorder=None):
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, nbytes=None, byteorder=None):
        super().__init__(name, bases, namespace)

        if nbytes is None:
            nbytes = cls._nbytes

        nbytes = int(nbytes)

        assert nbytes in [2, 4, 8]

        if byteorder is None:
            byteorder = cls._byteorder

        assert byteorder in {'big', 'little'}

        struct = Struct(ENDIAN_CODES[byteorder] + FORMAT_CODES[nbytes])

        cls._byteorder = byteorder
        cls._nbytes = nbytes
        cls._pack = struct.pack
        cls._unpack = struct.unpack
