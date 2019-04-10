# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Big endian integer enumeration types."""

from . import Enum


class Enum8(Enum, nbytes=1, byteorder='big', signed=False):

    """Unsigned big endian 8 bit integer enumeration."""


class Enum16(Enum, nbytes=2, byteorder='big', signed=False):

    """Unsigned big endian 16 bit integer enumeration."""


class Enum32(Enum, nbytes=4, byteorder='big', signed=False):

    """Unsigned big endian 32 bit integer enumeration."""


class Enum64(Enum, nbytes=8, byteorder='big', signed=False):

    """Unsigned big endian 64 bit integer enumeration."""
