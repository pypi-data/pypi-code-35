# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer enumeration classes from big endian byte order module."""

import pytest
from baseline import Baseline

from ...tests.conformance import BasicConformance

from .big import Enum8, Enum16, Enum32, Enum64


class Register16(Enum16):  # pylint: disable=too-many-ancestors

    """Tested class."""

    PC = 0
    SP = 1
    R0 = 2
    R1 = 3


class TestEnum16(BasicConformance):

    """Test unsigned big endian 16 bit integer enumeration."""

    bindata = b'\x00\x01'

    cls = Register16

    cls_nbytes = 2

    dump = Baseline("""
            +--------+--------+---------------+--------+------------+
            | Offset | Access | Value         | Memory | Type       |
            +--------+--------+---------------+--------+------------+
            | 0      | x      | Register16.SP | 00 01  | Register16 |
            +--------+--------+---------------+--------+------------+
            """)

    value = Register16.SP

    retval_repr = '<Register16.SP: 1>'

    unpack_excess = Baseline("""


        +--------+-----------------+---------------+--------+------------+
        | Offset | Access          | Value         | Memory | Type       |
        +--------+-----------------+---------------+--------+------------+
        | 0      | x               | Register16.SP | 00 01  | Register16 |
        | 2      | <excess memory> |               | 99     |            |
        +--------+-----------------+---------------+--------+------------+

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
        yield Register16.SP, "enumeration itself"


class TestRanges:

    """Test type ranges."""

    data = [
        (Enum8, 0, 0xff),
        (Enum16, 0, 0xffff),
        (Enum32, 0, 0xffffffff),
        (Enum64, 0, 0xffffffffffffffff),
    ]

    def test_just_outside_min(self):
        """Test just outside of type minimum."""
        for cls, min_, max_ in self.data:
            with pytest.raises(ValueError):
                cls("NewEnum", {"MIN": min_ - 1, "MAX": max_})

    def test_at_range(self):
        """Test minimum and maximum type values."""
        for cls, min_, max_ in self.data:
            new_cls = cls("NewEnum", {"MIN": min_, "MAX": max_})
            assert new_cls["MIN"] == min_
            assert new_cls["MAX"] == max_

    def test_just_outside_max(self):
        """Test just outside of type maximum."""
        for cls, min_, max_ in self.data:
            with pytest.raises(ValueError):
                cls("NewEnum", {"MIN": min_, "MAX": max_ + 1})
