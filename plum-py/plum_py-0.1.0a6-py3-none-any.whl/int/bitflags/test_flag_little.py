# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test little endian byte order flag bitfiled forms."""

from enum import IntFlag

from baseline import Baseline

from . import BitFlags

from ...tests.conformance import BasicConformance


class Register(IntFlag):

    """Flag definition."""

    SP = 1
    R0 = 2
    R1 = 16


class TestAssignedByteOrder(BasicConformance):

    """Test assignment of little endian during flag bitfiled class construction."""

    bindata = b'\x10\x00'

    class Bits16(BitFlags, nbytes=2, flag=Register, byteorder='little'):
        # pylint: disable=missing-docstring
        # pylint: disable=too-few-public-methods
        pass

    cls = Bits16

    del Bits16

    cls_nbytes = 2

    dump = Baseline("""
            +--------+--------+-------+--------+--------+
            | Offset | Access | Value | Memory | Type   |
            +--------+--------+-------+--------+--------+
            | 0      | x      | 16    | 10 00  | Bits16 |
            |  [0]   |   .sp  | False |        | bool   |
            |  [1]   |   .r0  | False |        | bool   |
            |  [4]   |   .r1  | True  |        | bool   |
            +--------+--------+-------+--------+--------+
            """)

    value = Register.R1

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+--------+
        | Offset | Access          | Value | Memory | Type   |
        +--------+-----------------+-------+--------+--------+
        | 0      | x               | 16    | 10 00  | Bits16 |
        |  [0]   |   .sp           | False |        | bool   |
        |  [1]   |   .r0           | False |        | bool   |
        |  [4]   |   .r1           | True  |        | bool   |
        | 2      | <excess memory> |       | 99     |        |
        +--------+-----------------+-------+--------+--------+

        1 unconsumed memory bytes (3 available, 2 consumed)
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+--------+
        | Offset | Access | Value                | Memory | Type   |
        +--------+--------+----------------------+--------+--------+
        | 0      | x      | <insufficient bytes> | 10     | Bits16 |
        +--------+--------+----------------------+--------+--------+

        InsufficientMemoryError: 1 too few memory bytes to unpack Bits16 (2
        needed, only 1 available), dump above shows interrupted progress
        """)

    def iter_instances(self):
        yield self.cls(self.value), 'instantiated from self.value'
        yield self.cls(16), 'instantiated from int'
