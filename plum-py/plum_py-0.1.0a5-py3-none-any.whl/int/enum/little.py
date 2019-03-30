# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Little endian integer enumeration types."""

from ._enum import Enum


class Enum8(Enum, nbytes=1, byteorder='little', signed=False):

    """Unsigned little endian 8 bit integer enumeration."""


class Enum16(Enum, nbytes=2, byteorder='little', signed=False):

    """Unsigned little endian 16 bit integer enumeration."""


class Enum32(Enum, nbytes=4, byteorder='little', signed=False):

    """Unsigned little endian 32 bit integer enumeration."""


class Enum64(Enum, nbytes=8, byteorder='little', signed=False):

    """Unsigned little endian 64 bit integer enumeration."""
