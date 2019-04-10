# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from io import BytesIO

import pytest
from baseline import Baseline

from plum import (
    PackError,
    pack_into,
)

from plum.int.little import UInt16, UInt8

from .tests.utils import wrap_message


class TestMultiple(object):

    """Test packing multiple items in one call."""

    pack_into = staticmethod(pack_into)

    def test_happy_path_items(self):
        memory = bytearray(4)
        assert self.pack_into(memory, 1, UInt8(1), UInt8(2)) is None
        assert memory == b'\x00\x01\x02\x00'

    def test_happy_path_kwitems(self):
        memory = bytearray(4)
        assert self.pack_into(memory, 1, m1=UInt8(1), m2=UInt8(2)) is None
        assert memory == b'\x00\x01\x02\x00'

    def test_happy_path_combo(self):
        memory = bytearray(4)
        assert self.pack_into(memory, 1, UInt8(1), m2=UInt8(2)) is None
        assert memory == b'\x00\x01\x02\x00'

    def test_untyped_item(self):
        memory = bytearray(4)
        with pytest.raises(PackError) as trap:
            self.pack_into(memory, 1, UInt8(1), UInt8(2), 3)

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
            self.pack_into(memory, 1, m1=UInt8(1), m2=UInt8(2), m3=3)

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
            self.pack_into(memory, 1, UInt8(1), m2=UInt8(2), m3=3)

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

    pack_into = staticmethod(pack_into)

    def test_middle(self):
        """Test insertion into the middle."""
        memory = bytearray(4)
        assert self.pack_into(memory, 1, UInt8(1), UInt8(2)) is None
        assert memory == b'\x00\x01\x02\x00'

    def test_extend(self):
        """Test adds onto the end."""
        memory = bytearray(2)
        assert self.pack_into(memory, 1, UInt8(1), UInt8(2)) is None
        assert memory == b'\x00\x01\x02'


class TestMemoryView(object):

    """Test packing into a writeable memoryview."""

    pack_into = staticmethod(pack_into)

    def test_middle(self):
        """Test insertion into the middle."""
        memory = bytearray(4)
        assert self.pack_into(memoryview(memory), 1, UInt8(1), UInt8(2)) is None
        assert memory == b'\x00\x01\x02\x00'

    def test_extend(self):
        """Test adds onto the end."""
        memory = bytearray(2)
        with pytest.raises(ValueError) as trap:
            self.pack_into(memoryview(memory), 1, UInt8(1), UInt8(2))

        expected = Baseline("""
            memoryview assignment: lvalue and rvalue have different structures
            """)

        assert wrap_message(trap.value) == expected


class TestBytesIO(object):

    """Test packing into a binary file."""

    pack_into = staticmethod(pack_into)

    def test_middle(self):
        """Test insertion into the middle."""
        memory = BytesIO(bytearray(4))
        assert self.pack_into(memory, 1, UInt8(1), UInt8(2)) is None
        memory.seek(0)
        assert memory.read() == b'\x00\x01\x02\x00'

    def test_extend(self):
        """Test adds onto the end."""
        memory = BytesIO(bytearray(2))
        assert self.pack_into(memory, 1, UInt8(1), UInt8(2)) is None
        memory.seek(0)
        assert memory.read() == b'\x00\x01\x02'
