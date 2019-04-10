# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test unpack_and_getdump() utility function."""

from io import BytesIO

import pytest
from baseline import Baseline

from . import InsufficientMemoryError, ExcessMemoryError, unpack_and_getdump
from .int.little import UInt8, UInt16
from .tests.utils import wrap_message

DUMP = Baseline("""
+--------+--------+-------+--------+--------+
| Offset | Access | Value | Memory | Type   |
+--------+--------+-------+--------+--------+
| 0      | x      | 258   | 02 01  | UInt16 |
+--------+--------+-------+--------+--------+
""")


INSUFFICIENT_MESSAGE = Baseline("""


    +--------+--------+----------------------+--------+--------+
    | Offset | Access | Value                | Memory | Type   |
    +--------+--------+----------------------+--------+--------+
    | 0      | x      | <insufficient bytes> | 01     | UInt16 |
    +--------+--------+----------------------+--------+--------+

    InsufficientMemoryError: 1 too few memory bytes to unpack UInt16 (2
    needed, only 1 available), dump above shows interrupted progress
    """)


EXCESS_MESSAGE = Baseline("""


    +--------+-----------------+-------+--------+--------+
    | Offset | Access          | Value | Memory | Type   |
    +--------+-----------------+-------+--------+--------+
    | 0      | x               | 258   | 02 01  | UInt16 |
    | 2      | <excess memory> |       | 00     |        |
    +--------+-----------------+-------+--------+--------+

    1 unconsumed memory bytes
    """)


class TestUnpackBytes:

    """Test memory parameter as "bytes" type."""

    def test_happypath(self):
        """Verify unpack successful."""
        x, dump = unpack_and_getdump(UInt16, b'\x02\x01')
        assert x == 0x0102
        assert dump == DUMP

    def test_insufficient(self):
        """Verify exception when too few memory bytes present."""
        with pytest.raises(InsufficientMemoryError) as trap:
            unpack_and_getdump(UInt16, b'\x01')

        assert wrap_message(trap.value) == INSUFFICIENT_MESSAGE

    def test_excess(self):
        """Verify exception when too many memory bytes present."""
        with pytest.raises(ExcessMemoryError) as trap:
            unpack_and_getdump(UInt16, b'\x02\x01\x00')

        assert wrap_message(trap.value) == EXCESS_MESSAGE


class TestUnpackByteArray:

    """Test memory parameter as "bytearray" type."""

    def test_happypath(self):
        """Verify unpack successful."""
        x, dump = unpack_and_getdump(UInt16, bytearray([2, 1]))
        assert x == 0x0102
        assert dump == DUMP

    def test_insufficient(self):
        """Verify exception when too few memory bytes present."""
        with pytest.raises(InsufficientMemoryError) as trap:
            unpack_and_getdump(UInt16, bytearray([1]))

        assert wrap_message(trap.value) == INSUFFICIENT_MESSAGE

    def test_excess(self):
        """Verify exception when too many memory bytes present."""
        with pytest.raises(ExcessMemoryError) as trap:
            unpack_and_getdump(UInt16, bytearray([2, 1, 0]))

        assert wrap_message(trap.value) == EXCESS_MESSAGE
