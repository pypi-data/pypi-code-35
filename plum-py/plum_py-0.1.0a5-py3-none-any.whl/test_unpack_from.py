# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test unpack_from() utility function."""

from io import BytesIO

import pytest
from baseline import Baseline

from . import InsufficientMemoryError, unpack_from
from .int.little import UInt16
from .tests.utils import wrap_message


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

    unpack_from = staticmethod(unpack_from)

    def test_happypath_nonzero_offset(self):
        """Verify unpack successful for nonzero offset."""
        x = self.unpack_from(UInt16, BytesIO(b'\x99\x02\x01\x99'), offset=1)
        assert x == 0x0102

    def test_happypath_default_offset(self):
        """Verify unpack successful for default offset."""
        memory = BytesIO(b'\x99\x02\x01\x99')
        memory.seek(1)
        x = self.unpack_from(UInt16, memory)
        assert x == 0x0102

    def test_insufficient(self):
        """Verify exception when too few memory bytes present."""
        with pytest.raises(InsufficientMemoryError) as trap:
            self.unpack_from(UInt16, BytesIO(b'\x99\x01'), offset=1)

        assert wrap_message(trap.value) == INSUFFICIENT_MESSAGE
