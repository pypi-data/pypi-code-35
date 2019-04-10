# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""BitFlags type."""

from ..bitfields._bitfields import BitsBase
from ._bitflagstype import BitFlagsType


class BitFlags(BitsBase, metaclass=BitFlagsType, nbytes=4, byteorder='little', fill=0, ignore=0):

    """Interpret memory bytes as an unsigned integer with bit flags.

    :param value: integer value or flag values
    :type value: int or any iterable accepted by :class:`dict`
    :param dict kwargs: flag values

    """
    # filled in by metaclass
    _flag_cls = None

    @property
    def value(self):
        """Get flags value.

        :returns: flags value
        :rtype: enum

        """
        # pylint: disable=not-callable
        return self._flag_cls(int(self))

    @property
    def name(self):
        """Get flags name.

        :returns: flags name
        :rtype: str

        """
        return str(self).split('.')[-1]

    def __baserepr__(self):
        # pylint: disable=not-callable
        flag_instance = self.value
        return repr(flag_instance)

    def __str__(self):
        # pylint: disable=not-callable
        flag_instance = self.value
        return str(flag_instance)

    def __and__(self, other):
        new_value = super().__and__(other)
        return type(self)(new_value)

    def __or__(self, other):
        new_value = super().__or__(other)
        return type(self)(new_value)

    __rand__ = __and__
    __ror__ = __or__

    def __invert__(self):
        new_value = super().__invert__()
        return type(self)(new_value)

    def __contains__(self, other):
        if not isinstance(other, self._flag_cls):
            raise TypeError(f'{self._flag_cls.__name__} member must be used')
        return self._value & int(other) == int(other)
