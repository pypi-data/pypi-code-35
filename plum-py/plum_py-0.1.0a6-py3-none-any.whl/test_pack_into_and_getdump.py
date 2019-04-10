# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from io import BytesIO

import pytest
from baseline import Baseline

from plum import (
    PackError,
    pack_into_and_getdump,
)

from plum.int.little import UInt16, UInt8

from .tests.utils import wrap_message


EXPECT_LIST = Baseline("""
    +--------+--------+-------+--------+-------+
    | Offset | Access | Value | Memory | Type  |
    +--------+--------+-------+--------+-------+
    | 0      | [0]    | 1     | 01     | UInt8 |
    | 1      | [1]    | 2     | 02     | UInt8 |
    +--------+--------+-------+--------+-------+
    """)


EXPECT_DICT = Baseline("""
    +--------+--------+-------+--------+-------+
    | Offset | Access | Value | Memory | Type  |
    +--------+--------+-------+--------+-------+
    | 0      | m1     | 1     | 01     | UInt8 |
    | 1      | m2     | 2     | 02     | UInt8 |
    +--------+--------+-------+--------+-------+
    """)


EXPECT_MIX = Baseline("""
    +--------+--------+-------+--------+-------+
    | Offset | Access | Value | Memory | Type  |
    +--------+--------+-------+--------+-------+
    | 0      | [0]    | 1     | 01     | UInt8 |
    | 1      | m2     | 2     | 02     | UInt8 |
    +--------+--------+-------+--------+-------+
    """)


class TestMultiple(object):

    """Test packing multiple items in one call."""

    def test_happy_path_items(self):
        memory = bytearray(4)
        assert pack_into_and_getdump(memory, 1, UInt8(1), UInt8(2)) == EXPECT_LIST
        assert memory == b'\x00\x01\x02\x00'

    def test_happy_path_kwitems(self):
        memory = bytearray(4)
        assert pack_into_and_getdump(memory, 1, m1=UInt8(1), m2=UInt8(2)) == EXPECT_DICT
        assert memory == b'\x00\x01\x02\x00'

    def test_happy_path_combo(self):
        memory = bytearray(4)
        assert pack_into_and_getdump(memory, 1, UInt8(1), m2=UInt8(2)) == EXPECT_MIX
        assert memory == b'\x00\x01\x02\x00'

    def test_untyped_item(self):
        memory = bytearray(4)
        with pytest.raises(PackError) as trap:
            pack_into_and_getdump(memory, 1, UInt8(1), UInt8(2), 3)

        expected = Baseline("""


            +--------+--------+-------+--------+-------+
            | Offset | Access | Value | Memory | Type  |
            +--------+--------+-------+--------+-------+
            | 0      | [0]    | 1     | 01     | UInt8 |
            | 1      | [1]    | 2     | 02     | UInt8 |
            |        | [2]    |       |        |       |
            +--------+--------+-------+--------+-------+

            PackError: unexpected TypeError exception occurred during pack
            operation, dump above shows interrupted progress, original exception
            traceback appears above this exception's traceback
            """)

        assert wrap_message(trap.value) == expected

    def test_untyped_kwitem(self):
        memory = bytearray(4)
        with pytest.raises(PackError) as trap:
            pack_into_and_getdump(memory, 1, m1=UInt8(1), m2=UInt8(2), m3=3)

        expected = Baseline("""


            +--------+--------+-------+--------+-------+
            | Offset | Access | Value | Memory | Type  |
            +--------+--------+-------+--------+-------+
            | 0      | m1     | 1     | 01     | UInt8 |
            | 1      | m2     | 2     | 02     | UInt8 |
            |        | m3     |       |        |       |
            +--------+--------+-------+--------+-------+

            PackError: unexpected TypeError exception occurred during pack
            operation, dump above shows interrupted progress, original exception
            traceback appears above this exception's traceback
            """)

        assert wrap_message(trap.value) == expected

    def test_untyped_combo(self):
        memory = bytearray(4)
        with pytest.raises(PackError) as trap:
            pack_into_and_getdump(memory, 1, UInt8(1), m2=UInt8(2), m3=3)

        expected = Baseline("""


            +--------+--------+-------+--------+-------+
            | Offset | Access | Value | Memory | Type  |
            +--------+--------+-------+--------+-------+
            | 0      | [0]    | 1     | 01     | UInt8 |
            | 1      | m2     | 2     | 02     | UInt8 |
            |        | m3     |       |        |       |
            +--------+--------+-------+--------+-------+

            PackError: unexpected TypeError exception occurred during pack
            operation, dump above shows interrupted progress, original exception
            traceback appears above this exception's traceback
            """)

        assert wrap_message(trap.value) == expected



class TestByteArray(object):

    """Test packing into a bytearray."""

    def test_middle(self):
        """Test insertion into the middle."""
        memory = bytearray(4)
        assert pack_into_and_getdump(memory, 1, UInt8(1), UInt8(2)) == EXPECT_LIST
        assert memory == b'\x00\x01\x02\x00'

    def test_extend(self):
        """Test adds onto the end."""
        memory = bytearray(2)
        assert pack_into_and_getdump(memory, 1, UInt8(1), UInt8(2)) == EXPECT_LIST
        assert memory == b'\x00\x01\x02'


class TestMemoryView(object):

    """Test packing into a writeable memoryview."""

    def test_middle(self):
        """Test insertion into the middle."""
        memory = bytearray(4)
        assert pack_into_and_getdump(memoryview(memory), 1, UInt8(1), UInt8(2)) == EXPECT_LIST
        assert memory == b'\x00\x01\x02\x00'

    def test_extend(self):
        """Test adds onto the end."""
        memory = bytearray(2)
        with pytest.raises(ValueError) as trap:
            pack_into_and_getdump(memoryview(memory), 1, UInt8(1), UInt8(2))

        expected = Baseline("""
            memoryview assignment: lvalue and rvalue have different structures
            """)

        assert wrap_message(trap.value) == expected


class TestBytesIO(object):

    """Test packing into a binary file."""

    def test_middle(self):
        """Test insertion into the middle."""
        memory = BytesIO(bytearray(4))
        assert pack_into_and_getdump(memory, 1, UInt8(1), UInt8(2)) == EXPECT_LIST
        memory.seek(0)
        assert memory.read() == b'\x00\x01\x02\x00'

    def test_extend(self):
        """Test adds onto the end."""
        memory = BytesIO(bytearray(2))
        assert pack_into_and_getdump(memory, 1, UInt8(1), UInt8(2)) == EXPECT_LIST
        memory.seek(0)
        assert memory.read() == b'\x00\x01\x02'
