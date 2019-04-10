# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test unpack_from_and_getdump() utility function."""

from io import BytesIO

import pytest
from baseline import Baseline

from . import InsufficientMemoryError, unpack_from_and_getdump
from .int.little import UInt16
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


class TestUnpackBytesIO:

    """Test memory parameter as "io.BytesIO" type."""

    def test_happypath_nonzero_offset(self):
        """Verify unpack successful for nonzero offset."""
        x, dump = unpack_from_and_getdump(UInt16, BytesIO(b'\x99\x02\x01\x99'), offset=1)
        assert x == 0x0102
        assert dump == DUMP

    def test_happypath_default_offset(self):
        """Verify unpack successful for for default offset."""
        memory = BytesIO(b'\x99\x02\x01\x99')
        memory.seek(1)  # verify default of 0 overrides this
        x, dump = unpack_from_and_getdump(UInt16, memory)
        assert x == 0x0102
        assert dump == DUMP

    def test_insufficient(self):
        """Verify exception when too few memory bytes present."""
        with pytest.raises(InsufficientMemoryError) as trap:
            unpack_from_and_getdump(UInt16, BytesIO(b'\x99\x01'), offset=1)

        assert wrap_message(trap.value) == INSUFFICIENT_MESSAGE
