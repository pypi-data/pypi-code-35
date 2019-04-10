# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer enum behavior when value not an enum member."""

from enum import IntEnum

from baseline import Baseline

from . import Int

from ..tests.conformance import BasicConformance


class Register(IntEnum):

    PC = 0
    SP = 1
    R0 = 2
    R1 = 3


class TestInvalidValue(BasicConformance):

    bindata = b'\x63\x00'

    class Register16(Int, nbytes=2, enum=Register):
        pass

    cls = Register16

    del Register16

    cls_nbytes = 2

    dump = Baseline("""
            +--------+--------+-------+--------+------------+
            | Offset | Access | Value | Memory | Type       |
            +--------+--------+-------+--------+------------+
            | 0      | x      | 99    | 63 00  | Register16 |
            +--------+--------+-------+--------+------------+
            """)

    value = 99

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+------------+
        | Offset | Access          | Value | Memory | Type       |
        +--------+-----------------+-------+--------+------------+
        | 0      | x               | 99    | 63 00  | Register16 |
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
