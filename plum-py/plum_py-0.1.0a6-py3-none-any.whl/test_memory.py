# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
from baseline import Baseline

from . import InsufficientMemoryError, Memory
from .int.little import UInt8, UInt16
from .tests.utils import wrap_message


class TestAvailableProperty:

    memcls = Memory

    attr_readonly_msg = Baseline("""
            can't set attribute
            """)

    def test_write(self):
        m = self.memcls(b'123')
        with pytest.raises(AttributeError) as trap:
            m.available = 0

        assert str(trap.value) == self.attr_readonly_msg

    def test_at_init(self):
        m = self.memcls(b'123')
        assert m.available == 3


class TestConsumedProperty:

    memcls = Memory

    attr_readonly_msg = Baseline("""
        can't set attribute
        """)

    def test_at_init(self):
        m = self.memcls(b'123')
        assert m.consumed == 0


class TestLimitContextManager:

    memcls = Memory

    def test_available(self):
        m = self.memcls(bytes(100))
        assert m.available == 100
        with m.limit(20):
            assert m.available == 20
        assert m.available == 100

    def test_consume(self):
        m = self.memcls(bytes(100))
        with m.limit(10):
            assert m.consume_bytes(10) == bytes(10)
            with pytest.raises(InsufficientMemoryError):
                m.consume_bytes(1)
            assert m.available == 0
        assert m.available == 90


class TestBufferProperty:

    memcls = Memory

    attr_readonly_msg = Baseline("""
        can't set attribute
        """)

    def test_write(self):
        m = self.memcls(b'123')
        with pytest.raises(AttributeError) as trap:
            m.buffer = 0

        assert str(trap.value) == self.attr_readonly_msg

    def test_type(self):
        m = self.memcls(b'123')
        assert type(m.buffer) == memoryview

    def test_content(self):
        m = self.memcls(b'123')
        assert bytes(m.buffer) == b'123'


class TestUnpack:

    memcls = Memory

    def test_simple(self):
        m = self.memcls(b'\x01\x02\x03')
        assert m.consumed == 0

        x = m.unpack(UInt8)

        assert x == 1
        assert type(x) is UInt8
        assert m.consumed == 1

        y = m.unpack(UInt8)
        assert y == 2
        assert type(y) is UInt8
        assert m.consumed == 2

    def test_exception(self):
        m = self.memcls(b'\x01')

        with pytest.raises(InsufficientMemoryError) as trap:
            m.unpack(UInt16)

        expected_message = Baseline("""


            +--------+--------+----------------------+--------+--------+
            | Offset | Access | Value                | Memory | Type   |
            +--------+--------+----------------------+--------+--------+
            | 0      | x      | <insufficient bytes> | 01     | UInt16 |
            +--------+--------+----------------------+--------+--------+

            InsufficientMemoryError: 1 too few memory bytes to unpack UInt16 (2
            needed, only 1 available), dump above shows interrupted progress
            """)

        assert wrap_message(trap.value) == expected_message
