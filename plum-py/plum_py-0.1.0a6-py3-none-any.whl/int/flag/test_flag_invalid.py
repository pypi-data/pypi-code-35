# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer flag behavior when value is not a member combination."""

from baseline import Baseline

from ...tests.conformance import BasicConformance

from . import Flag


class Register(Flag, nbytes=2):

    """Tested class."""

    SP = 1
    R0 = 2
    R1 = 8


class TestInvalidValue(BasicConformance):

    """Test value is not a member combination."""

    bindata = b'\x63\x00'

    cls = Register

    cls_nbytes = 2

    dump = Baseline("""
            +--------+--------+-------+--------+----------+
            | Offset | Access | Value | Memory | Type     |
            +--------+--------+-------+--------+----------+
            | 0      | x      | 99    | 63 00  | Register |
            |  [0]   |   .sp  | True  |        | bool     |
            |  [1]   |   .r0  | True  |        | bool     |
            |  [3]   |   .r1  | False |        | bool     |
            +--------+--------+-------+--------+----------+
            """)

    value = Register(99)

    retval_repr = "<Register.64|32|R0|SP: 99>"

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+----------+
        | Offset | Access          | Value | Memory | Type     |
        +--------+-----------------+-------+--------+----------+
        | 0      | x               | 99    | 63 00  | Register |
        |  [0]   |   .sp           | True  |        | bool     |
        |  [1]   |   .r0           | True  |        | bool     |
        |  [3]   |   .r1           | False |        | bool     |
        | 2      | <excess memory> |       | 99     |          |
        +--------+-----------------+-------+--------+----------+

        1 unconsumed memory bytes
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+----------+
        | Offset | Access | Value                | Memory | Type     |
        +--------+--------+----------------------+--------+----------+
        | 0      | x      | <insufficient bytes> | 63     | Register |
        +--------+--------+----------------------+--------+----------+

        InsufficientMemoryError: 1 too few memory bytes to unpack Register (2
        needed, only 1 available), dump above shows interrupted progress
        """)
