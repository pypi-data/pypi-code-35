# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from io import BytesIO

import pytest
from baseline import Baseline

from . import ExcessMemoryError, exhaust, unpack_from
from .int.little import UInt8, UInt16
from .tests.utils import wrap_message


class TestBytes:

    expected_message = Baseline("""
        1 unconsumed memory bytes
        """)

    @property
    def memory(self):
        return bytes([1, 2])

    def test_happypath_bytes(self):
        with exhaust(self.memory) as memory:
            assert unpack_from(UInt8, memory) == 1
            assert memory.tell() == 1
            assert unpack_from(UInt8, memory) == 2
            assert memory.tell() == 2

    def test_excess_bytes(self):
        with pytest.raises(ExcessMemoryError) as trap:
            with exhaust(self.memory) as memory:
                assert unpack_from(UInt8, memory) == 1
                assert memory.tell() == 1

        assert wrap_message(trap.value) == self.expected_message


class TestByteArray(TestBytes):

    @property
    def memory(self):
        return bytearray([1, 2])


class TestBytesIO(TestBytes):

    @property
    def memory(self):
        return BytesIO(bytes([1, 2]))

