# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Bit field definition."""

from enum import IntEnum


class BitField:

    __slots__ = [
        '_make_type',
        '_type',
        'mask',
        'signbit',
        'default',
        'ignore',
        'name',
        'pos',
        'size',
    ]

    def __init__(self, pos, size, default, signed, ignore):

        pos = int(pos)
        size = int(size)
        signed = bool(signed)

        assert pos >= 0

        if signed:
            assert size > 1
            signbit = 1 << (size - 1)
        else:
            assert size > 0
            signbit = 0

        self.mask = (1 << size) - 1
        self.signbit = signbit

        self.default = default
        self.ignore = ignore
        self.name = None  # assigned via __set_name__ protocol
        self.pos = pos
        self.size = size
        # assigned during BitFields class construction (by
        # BitFieldsType.__new__)
        self._type = None
        # assigned during BitFields class construction (by
        # BitFieldsType.__new__)
        self._make_type = None

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, cls):
        self._type = cls

        if issubclass(cls, IntEnum):
            self._make_type = self._make_enum
        elif issubclass(cls, int):
            self._make_type = self._make_int
        else:
            self._make_type = self._make_bits

    @property
    def signed(self):
        return bool(self.signbit)

    def __repr__(self):
        return ('BitField('
                f'name={self.name!r},'
                f'type={self._type!r},'
                f'pos={self.pos!r},'
                f'size={self.size!r},'
                f'default={self.default!r},'
                f'signed={self.signed!r}'
                ')')

    def __set_name__(self, owner, name):
        assert self.name is None, 'bitfield definition already in use'
        self.name = name

    def __get__(self, obj, type=None):
        if obj is None:
            return self

        value = (int(obj) >> self.pos) & self.mask
        if self.signbit & value:
            # its a signed number and its negative
            value = -((1 << self.size) - value)

        return self._make_type(obj, value)

    def _make_bits(self, obj, value):
        item = self._type(value)
        try:
            bitoffset, store = obj._bitoffset_store
        except AttributeError:
            bitoffset, store = self.pos, obj
        else:
            bitoffset += self.pos
        item._bitoffset_store = bitoffset, store
        return item

    def _make_int(self, obj, value):
        return self._type(value)

    def _make_enum(self, obj, value):
        try:
            item = self.type(value)
        except ValueError:
            if issubclass(self._type, IntEnum):
                item = value
            else:
                raise
        return item

    def __set__(self, obj, value):
        mask = self.mask
        size = self.size
        pos = self.pos

        try:
            value = int(value)
        except TypeError:
            value = self._type(value)

        if value & ~mask:
            if self.signbit:
                minvalue = -(1 << (size - 1))
                maxvalue = -(1 + minvalue)
            else:
                minvalue = 0
                maxvalue = (1 << size) - 1
            raise ValueError(
                f'bitfield {self.name!r} requires {minvalue} <= number <= {maxvalue}')

        try:
            bitoffset, obj = obj._bitoffset_store
        except AttributeError:
            pass
        else:
            pos += bitoffset

        obj._value = (obj._value & ~(mask << pos)) | ((value & mask) << pos)


# TODO: look at dataclass implementation as to why this should be a function
#       rather than just leaving user instantiate class directly
#       (has something to do with IDE introspection/hints)
def bitfield(*, pos, size, default=None, signed=False, ignore=False):
    """Create bit field definition.

    :param int pos: bit offset of least significant bit
    :param int size: size in bits
    :param int default: initial value when unspecified
    :param bool signed: interpret as signed integer
    :param bool ignore: do not include field in comparisons
    :returns: bit field definition
    :rtype: BitField

    """
    return BitField(pos, size, default, signed, ignore)
