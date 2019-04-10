# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer flag classes from big endian byte order module."""

import pytest
from baseline import Baseline

from ...tests.conformance import BasicConformance

from .big import Flag8, Flag16, Flag32, Flag64


class Register16(Flag16):

    """Tested class."""

    SP = 1
    R0 = 2
    R1 = 16


class TestFlag16(BasicConformance):

    """Test big endian 16 bit integer flag."""

    bindata = b'\x00\x01'

    cls = Register16

    cls_nbytes = 2

    dump = Baseline("""
            +--------+--------+-------+--------+------------+
            | Offset | Access | Value | Memory | Type       |
            +--------+--------+-------+--------+------------+
            | 0      | x      | 1     | 00 01  | Register16 |
            |  [0]   |   .sp  | True  |        | bool       |
            |  [1]   |   .r0  | False |        | bool       |
            |  [4]   |   .r1  | False |        | bool       |
            +--------+--------+-------+--------+------------+
            """)

    value = Register16.SP

    retval_repr = '<Register16.SP: 1>'

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+------------+
        | Offset | Access          | Value | Memory | Type       |
        +--------+-----------------+-------+--------+------------+
        | 0      | x               | 1     | 00 01  | Register16 |
        |  [0]   |   .sp           | True  |        | bool       |
        |  [1]   |   .r0           | False |        | bool       |
        |  [4]   |   .r1           | False |        | bool       |
        | 2      | <excess memory> |       | 99     |            |
        +--------+-----------------+-------+--------+------------+

        1 unconsumed memory bytes
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+------------+
        | Offset | Access | Value                | Memory | Type       |
        +--------+--------+----------------------+--------+------------+
        | 0      | x      | <insufficient bytes> | 00     | Register16 |
        +--------+--------+----------------------+--------+------------+

        InsufficientMemoryError: 1 too few memory bytes to unpack Register16
        (2 needed, only 1 available), dump above shows interrupted progress
        """)

    def iter_instances(self):
        yield self.cls(self.value), 'instantiated from self.value'
        yield self.cls(1), 'instantiated from int'
        yield Register16.SP, "flag itself"


class TestRanges:

    """Test type ranges."""

    data = [
        (Flag8, 0, 0x80),
        (Flag16, 0, 0x8000),
        (Flag32, 0, 0x80000000),
        (Flag64, 0, 0x8000000000000000),
    ]

    def test_just_outside_min(self):
        """Test just outside of type minimum."""
        for cls, min_, max_ in self.data:
            with pytest.raises(ValueError):
                cls("NewFlag", {"MIN": min_ - 1, "MAX": max_})

    def test_at_range(self):
        """Test minimum and maximum possible flag value."""
        for cls, min_, max_ in self.data:
            new_cls = cls("NewFlag", {"MIN": min_, "MAX": max_})
            assert new_cls["MIN"] == min_
            assert new_cls["MAX"] == max_

    def test_just_outside_max(self):
        """Test just outside of type maximum."""
        for cls, min_, max_ in self.data:
            with pytest.raises(ValueError):
                cls("NewFlag", {"MIN": min_, "MAX": max_ << 1})
