# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test int classes from little endian byte order module."""

import pytest
from baseline import Baseline

from .. import pack, unpack
from ..tests.conformance import BasicConformance

from .little import SInt8, SInt16, SInt32, SInt64
from .little import UInt8, UInt16, UInt32, UInt64


class TestU8(BasicConformance):

    bindata = b'\x00'

    cls = UInt8

    cls_nbytes = 1

    dump = Baseline("""
            +--------+--------+-------+--------+-------+
            | Offset | Access | Value | Memory | Type  |
            +--------+--------+-------+--------+-------+
            | 0      | x      | 0     | 00     | UInt8 |
            +--------+--------+-------+--------+-------+
            """)

    pack = staticmethod(pack)

    value = 0

    unpack = staticmethod(unpack)

    unpack_cls = int

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+-------+
        | Offset | Access          | Value | Memory | Type  |
        +--------+-----------------+-------+--------+-------+
        | 0      | x               | 0     | 00     | UInt8 |
        | 1      | <excess memory> |       | 99     |       |
        +--------+-----------------+-------+--------+-------+

        1 unconsumed memory bytes
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+-------+
        | Offset | Access | Value                | Memory | Type  |
        +--------+--------+----------------------+--------+-------+
        |        | x      | <insufficient bytes> |        | UInt8 |
        +--------+--------+----------------------+--------+-------+

        InsufficientMemoryError: 1 too few memory bytes to unpack UInt8 (1
        needed, only 0 available), dump above shows interrupted progress
        """)


class TestS32L(BasicConformance):

    bindata = b'\x00\xfc\xff\xff'

    cls = SInt32

    cls_nbytes = 4

    dump = Baseline("""
            +--------+--------+-------+-------------+--------+
            | Offset | Access | Value | Memory      | Type   |
            +--------+--------+-------+-------------+--------+
            | 0      | x      | -1024 | 00 fc ff ff | SInt32 |
            +--------+--------+-------+-------------+--------+
            """)

    pack = staticmethod(pack)

    value = -1024

    unpack = staticmethod(unpack)

    unpack_cls = int

    unpack_excess = Baseline("""


        +--------+-----------------+-------+-------------+--------+
        | Offset | Access          | Value | Memory      | Type   |
        +--------+-----------------+-------+-------------+--------+
        | 0      | x               | -1024 | 00 fc ff ff | SInt32 |
        | 4      | <excess memory> |       | 99          |        |
        +--------+-----------------+-------+-------------+--------+

        1 unconsumed memory bytes
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+----------+--------+
        | Offset | Access | Value                | Memory   | Type   |
        +--------+--------+----------------------+----------+--------+
        | 0      | x      | <insufficient bytes> | 00 fc ff | SInt32 |
        +--------+--------+----------------------+----------+--------+

        InsufficientMemoryError: 1 too few memory bytes to unpack SInt32 (4
        needed, only 3 available), dump above shows interrupted progress
        """)


class TestRanges:

    data = [
        (UInt8, 0, 0xff),
        (UInt16, 0, 0xffff),
        (UInt32, 0, 0xffffffff),
        (UInt64, 0, 0xffffffffffffffff),
        (SInt8, -0x80, 0x7f),
        (SInt16, -0x8000, 0x7fff),
        (SInt32, -0x80000000, 0x7fffffff),
        (SInt64, -0x8000000000000000, 0x7fffffffffffffff),
    ]

    def test_just_outside_min(self):
        for cls, min_, _ in self.data:
            with pytest.raises(ValueError):
                cls(min_ - 1)

    def test_at_min(self):
        for cls, min_, _ in self.data:
            assert cls(min_) == min_

    def test_at_max(self):
        for cls, _, max_ in self.data:
            assert cls(max_) == max_

    def test_just_outside_max(self):
        for cls, _, max_ in self.data:
            with pytest.raises(ValueError):
                cls(max_ + 1)
