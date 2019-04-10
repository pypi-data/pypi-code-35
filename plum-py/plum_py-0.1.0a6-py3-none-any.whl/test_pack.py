# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
from baseline import Baseline

from plum import (
    PackError,
    pack,
)

from plum.int.little import UInt16, UInt8

from .tests.utils import wrap_message


class TestMultiple(object):

    """Test packing multiple items in one call."""

    pack = staticmethod(pack)

    def test_happy_path_items(self):
        assert self.pack(UInt8(0), UInt16(0x0102)) == b'\x00\x02\x01'

    def test_happy_path_kwitems(self):
        assert self.pack(m1=UInt8(0), m2=UInt16(0x0102)) == b'\x00\x02\x01'

    def test_happy_path_combo(self):
        assert self.pack(UInt8(0), m2=UInt16(0x0102)) == b'\x00\x02\x01'

    def test_untyped_item(self):
        with pytest.raises(PackError) as trap:
            self.pack(UInt8(0), UInt16(0x0102), 0)

        expected = Baseline("""


            +--------+--------+-------+--------+--------+
            | Offset | Access | Value | Memory | Type   |
            +--------+--------+-------+--------+--------+
            | 0      | [0]    | 0     | 00     | UInt8  |
            | 1      | [1]    | 258   | 02 01  | UInt16 |
            |        | [2]    |       |        |        |
            +--------+--------+-------+--------+--------+

            PackError: unexpected TypeError exception occurred during pack
            operation, dump above shows interrupted progress, original exception
            traceback appears above this exception's traceback
            """)

        assert wrap_message(trap.value) == expected

    def test_untyped_kwitem(self):
        with pytest.raises(PackError) as trap:
            self.pack(m1=UInt8(0), m2=UInt16(0x0102), m3=0)

        expected = Baseline("""


            +--------+--------+-------+--------+--------+
            | Offset | Access | Value | Memory | Type   |
            +--------+--------+-------+--------+--------+
            | 0      | m1     | 0     | 00     | UInt8  |
            | 1      | m2     | 258   | 02 01  | UInt16 |
            |        | m3     |       |        |        |
            +--------+--------+-------+--------+--------+

            PackError: unexpected TypeError exception occurred during pack
            operation, dump above shows interrupted progress, original exception
            traceback appears above this exception's traceback
            """)

        assert wrap_message(trap.value) == expected

    def test_untyped_combo(self):
        with pytest.raises(PackError) as trap:
            self.pack(UInt8(0), m2=UInt16(0x0102), m3=0)

        expected = Baseline("""


            +--------+--------+-------+--------+--------+
            | Offset | Access | Value | Memory | Type   |
            +--------+--------+-------+--------+--------+
            | 0      | [0]    | 0     | 00     | UInt8  |
            | 1      | m2     | 258   | 02 01  | UInt16 |
            |        | m3     |       |        |        |
            +--------+--------+-------+--------+--------+

            PackError: unexpected TypeError exception occurred during pack
            operation, dump above shows interrupted progress, original exception
            traceback appears above this exception's traceback
            """)

        assert wrap_message(trap.value) == expected
