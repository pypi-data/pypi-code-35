# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test int classes from little endian byte order module."""

from .native import UInt16


class TestInitializer:

    def test_no_value(self):
        assert UInt16() == 0

    def test_from_str_and_base(self):
        assert UInt16('102', base=16) == 0x102
