# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Little endian integer flag types."""

from . import Flag


class Flag8(Flag, nbytes=1, byteorder='little'):

    """Little endian 8 bit integer flags."""


class Flag16(Flag, nbytes=2, byteorder='little'):

    """Little endian 16 bit integer flags."""


class Flag32(Flag, nbytes=4, byteorder='little'):

    """Little endian 32 bit integer flags."""


class Flag64(Flag, nbytes=8, byteorder='little'):

    """Little endian 64 bit integer flags."""
