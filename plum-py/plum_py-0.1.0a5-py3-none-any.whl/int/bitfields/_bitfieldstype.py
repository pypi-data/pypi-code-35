# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""BitFields type metaclass."""

from enum import IntEnum

from ..._plumtype import PlumType
from ._bitfield import BitField


class BitFieldsType(PlumType):

    """BitFields type metaclass.

    Create custom |BitFields| subclass. For example:

        >>> from plum.int.bitfields import BitFields, bitfield
        >>> class MyBits(BitFields, nbytes=1, byteorder='big', fill=0, ignore=0x80):
        ...     nibble: int = bitfield(pos=0, size=4)
        ...     threebits: int = bitfield(pos=4, size=3)
        ...
        >>>

    :param int nbytes: number of memory bytes
    :param str byteorder: ``'big'`` or ``'little'``
    :param int fill: default value (integer basis before applying bit field values)
    :param int ignore: mask applied during comparison to ignore bit fields

    """

    def __new__(mcs, name, bases, namespace, nbytes=None, byteorder=None,
                fill=None, ignore=None):
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, nbytes=None, byteorder=None,
                 fill=None, ignore=None):
        super().__init__(name, bases, namespace)

        if byteorder is None:
            byteorder = cls._byteorder

        assert byteorder in {'big', 'little'}

        if fill is None:
            fill = cls._fill

        if ignore is None:
            ignore = cls._ignore

        fields = dict()
        for name, typ in getattr(cls, '__annotations__', {}).items():
            field = getattr(cls, name, None)
            assert isinstance(field, BitField)
            assert isinstance(typ, BitFieldsType) or issubclass(
                typ, (int, IntEnum))
            field.type = typ
            fields[name] = field

        if nbytes is None:
            numbits = max(field.pos + field.size for field in fields.values())
            nbytes = 1
            while numbits > (nbytes * 8):
                nbytes *= 2

        max_ = (1 << (nbytes * 8)) - 1

        for field in fields.values():
            if field.ignore:
                ignore |= field.mask << field.pos
            elif isinstance(field.type, BitFieldsType):
                ignore |= field.type._ignore << field.pos

        cls._byteorder = byteorder
        cls._compare_mask = (max_ ^ ignore) & max_
        cls._fields = fields
        cls._fill = fill
        cls._ignore = ignore
        cls._max = max_
        cls._nbytes = nbytes
