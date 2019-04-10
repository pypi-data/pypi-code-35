# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test flag bitfield behavior when value not an flag member combination."""

from enum import IntFlag

from baseline import Baseline

from . import BitFlags

from ...tests.conformance import BasicConformance


class Register(IntFlag):

    """Flag definition."""

    SP = 1
    R0 = 2
    R1 = 8


class TestInvalidValue(BasicConformance):

    """Test value that is not a flag member combination."""

    bindata = b'\x63\x00'

    class Register16(BitFlags, nbytes=2, flag=Register):
        # pylint: disable=missing-docstring
        # pylint: disable=too-few-public-methods
        pass

    cls = Register16

    del Register16

    cls_nbytes = 2

    dump = Baseline("""
            +--------+--------+-------+--------+------------+
            | Offset | Access | Value | Memory | Type       |
            +--------+--------+-------+--------+------------+
            | 0      | x      | 99    | 63 00  | Register16 |
            |  [0]   |   .sp  | True  |        | bool       |
            |  [1]   |   .r0  | True  |        | bool       |
            |  [3]   |   .r1  | False |        | bool       |
            +--------+--------+-------+--------+------------+
            """)

    value = Register(99)

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+------------+
        | Offset | Access          | Value | Memory | Type       |
        +--------+-----------------+-------+--------+------------+
        | 0      | x               | 99    | 63 00  | Register16 |
        |  [0]   |   .sp           | True  |        | bool       |
        |  [1]   |   .r0           | True  |        | bool       |
        |  [3]   |   .r1           | False |        | bool       |
        | 2      | <excess memory> |       | 99     |            |
        +--------+-----------------+-------+--------+------------+

        1 unconsumed memory bytes (3 available, 2 consumed)
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+------------+
        | Offset | Access | Value                | Memory | Type       |
        +--------+--------+----------------------+--------+------------+
        | 0      | x      | <insufficient bytes> | 63     | Register16 |
        +--------+--------+----------------------+--------+------------+

        InsufficientMemoryError: 1 too few memory bytes to unpack Register16
        (2 needed, only 1 available), dump above shows interrupted progress
        """)
