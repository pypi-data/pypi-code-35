# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""BitFields type."""

from ..._plum import Plum
from ..._utils import getbytes
from ._bitfieldstype import BitFieldsType


class BitFields(Plum, metaclass=BitFieldsType, nbytes=4, byteorder='little', fill=0, ignore=0):

    """Interpret memory bytes as an unsigned integer with bit fields."""

    # filled in by metaclass
    _byteorder = 'little'
    _compare_mask = 0xffffffff
    _fields = dict()
    _fill = 0
    _ignore = 0
    _max = 0xffffffff
    _nbytes = 4

    def __init__(self, *args, **kwargs):
        cls = type(self)

        if args:
            if len(args) > 1:
                raise TypeError(
                    f'{cls.__name__} expected at most 1 arguments, got {len(args)}')

            try:
                self._value = int(args[0])
            except TypeError:
                self._value = cls._fill
                try:
                    values = dict(args[0])
                except TypeError:
                    raise TypeError(
                        f'{args[0]!r} object is not an int or bit field dict')
                if kwargs:
                    values.update(kwargs)
                    kwargs = values
                else:
                    kwargs = values
            else:
                if (self._value < 0) or (self._value > cls._max):
                    raise ValueError(
                        f'{cls.__name__} requires 0 <= number <= {cls._max}')
        else:
            self._value = cls._fill

        if kwargs:
            fields = cls._fields

            extras = set(kwargs) - set(fields)

            if extras:
                s = 's' if len(extras) > 1 else ''
                message = (
                    f'{cls.__name__}() '
                    f'got {len(extras)} unexpected bit field{s}: ')
                message += ', '.join(repr(e) for e in sorted(extras))
                raise TypeError(message)

            values = [kwargs.get(n, f.default) for n, f in fields.items()]
            missing = [n for n, v in zip(fields, values) if v is None]

            if missing:
                s = 's' if len(missing) > 1 else ''
                message = (
                    f'{cls.__name__}() '
                    f'missing {len(missing)} required bit field{s}: ')
                message += ', '.join(repr(m) for m in sorted(missing))
                raise TypeError(message)

            for field, value in zip(fields.values(), values):
                field.__set__(self, value)

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent):
        chunk, offset, limit = getbytes(memory, offset, cls._nbytes, limit, dump, cls)

        value = int.from_bytes(chunk, cls._byteorder, signed=False)

        self = cls.__new__(cls, value)
        cls.__init__(self, value)

        if dump:
            dump.value = self._value
            cls._add_bitfields_to_dump(self, dump)

        return self, offset, limit

    @classmethod
    def __pack__(cls, memory, offset, value, dump):
        try:
            ivalue = int(value)
        except TypeError:
            value = cls(value)
            ivalue = value._value

        nbytes = cls._nbytes

        chunk = ivalue.to_bytes(nbytes, cls._byteorder, signed=False)

        end = offset + nbytes
        memory[offset:end] = chunk

        if dump:
            dump.value = str(ivalue)
            dump.memory = chunk
            dump.cls = cls
            cls._add_bitfields_to_dump(value, dump)

        return end

    @classmethod
    def _add_bitfields_to_dump(cls, value, dump, bitoffset=0):
        if not isinstance(value, cls):
            value = cls(value)
        for name, field in cls._fields.items():
            if issubclass(field.type, BitFields):
                row = dump.add_level(
                    access='.' + name)
                row.cls = field.type
                field.type._add_bitfields_to_dump(
                    getattr(cls, name).__get__(value, cls), row, bitoffset + field.pos)
            else:
                row = dump.add_level(
                    access='.' + name,
                    bits=(bitoffset + field.pos, field.size))
                row.value = str(getattr(cls, name).__get__(value, cls))
                row.cls = field.type

    def __str__(self):
        # str( ) around getattr formats enumerations correctly (otherwise shows
        # as int)
        return f"{{{', '.join(f'{n!r}={str(getattr(self, n))}' for n in self._fields)}}}"

    def __baserepr__(self):
        return f"{{{', '.join(f'{n!r}={getattr(self, n)!r}' for n in self._fields)}}}"

    @classmethod
    def _normalize_for_compare(cls, value, other):
        if type(other) is cls:
            other = other._value & cls._compare_mask
            value = value & cls._compare_mask
        else:
            try:
                other = int(other)
            except TypeError:
                other = int(cls(other)) & cls._compare_mask
                value = value & cls._compare_mask
        return value, other

    def __lt__(self, other):
        value, other = self._normalize_for_compare(self._value, other)
        return int.__lt__(value, other)

    def __le__(self, other):
        value, other = self._normalize_for_compare(self._value, other)
        return int.__le__(value, other)

    def __eq__(self, other):
        value, other = self._normalize_for_compare(self._value, other)
        return int.__eq__(value, other)

    def __ne__(self, other):
        value, other = self._normalize_for_compare(self._value, other)
        return int.__ne__(value, other)

    def __gt__(self, other):
        value, other = self._normalize_for_compare(self._value, other)
        return int.__gt__(value, other)

    def __ge__(self, other):
        value, other = self._normalize_for_compare(self._value, other)
        return int.__ge__(value, other)

    def __hash__(self):
        return int.__hash__(self._value & type(self)._compare_mask)

    def __bool__(self):
        return int.__bool__(self._value & type(self)._compare_mask)

    def __add__(self, other):
        return int.__add__(self._value, other)

    def __sub__(self, other):
        return int.__sub__(self._value, other)

    def __mul__(self, other):
        return int.__mul__(self._value, other)

    def __truediv__(self, other):
        return int.__truediv__(self._value, other)

    def __floordiv__(self, other):
        return int.__floordiv__(self._value, other)

    def __mod__(self, other):
        return int.__mod__(self._value, other)

    def __divmod__(self, other):
        return int.__divmod__(self._value, other)

    def __pow__(self, other, *args):
        return int.__pow__(self._value, other, *args)

    def __lshift__(self, other):
        return int.__lshift__(self._value, other)

    def __rshift__(self, other):
        return int.__rshift__(self._value, other)

    def __and__(self, other):
        return int.__and__(self._value, other)

    def __xor__(self, other):
        return int.__xor__(self._value, other)

    def __or__(self, other):
        return int.__or__(self._value, other)

    def __radd__(self, other):
        return int.__radd__(self._value, other)

    def __rsub__(self, other):
        return int.__rsub__(self._value, other)

    def __rmul__(self, other):
        return int.__rmul__(self._value, other)

    def __rtruediv__(self, other):
        return int.__rtruediv__(self._value, other)

    def __rfloordiv__(self, other):
        return int.__rfloordiv__(self._value, other)

    def __rmod__(self, other):
        return int.__rmod__(self._value, other)

    def __rdivmod__(self, other):
        return int.__rdivmod__(self._value, other)

    def __rpow__(self, other, *args):
        return int.__rpow__(self._value, other, *args)

    def __rlshift__(self, other):
        return int.__rlshift__(self._value, other)

    def __rrshift__(self, other):
        return int.__rrshift__(self._value, other)

    def __rand__(self, other):
        return int.__rand__(self._value, other)

    def __rxor__(self, other):
        return int.__rxor__(self._value, other)

    def __ror__(self, other):
        return int.__ror__(self._value, other)

    def __iadd__(self, other):
        self._value += other

    def __isub__(self, other):
        self._value -= other

    def __imul__(self, other):
        self._value *= other

    def __itruediv__(self, other):
        self._value /= other

    def __ifloordiv__(self, other):
        self._value //= other

    def __imod__(self, other):
        self._value %= other

    def __ilshift__(self, other):
        self._value <<= other

    def __irshift__(self, other):
        self._value >>= other

    def __iand__(self, other):
        self._value &= other

    def __ixor__(self, other):
        self._value ^= other

    def __ior__(self, other):
        self._value |= other

    def __neg__(self):
        return (~self._value) & type(self)._max

    def __pos__(self):
        return self._value

    def __abs__(self):
        return self._value

    def __invert__(self):
        return (~self._value) & type(self)._max

    def __int__(self):
        return self._value

    def __float__(self):
        return int.__float__(self._value)

    def __index__(self):
        return int.__index__(self._value)

    def __round__(self, *args):
        return int.__round__(self._value, *args)
