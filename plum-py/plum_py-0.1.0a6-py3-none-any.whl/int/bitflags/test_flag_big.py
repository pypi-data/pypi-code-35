# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test big endian byte order flag bitfiled forms."""

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

    """Test assignment of big endian during flag bitfiled class construction."""

    bindata = b'\x00\x01'

    class Bits16(BitFlags, nbytes=2, flag=Register, byteorder='big'):
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
            | 0      | x      | 1     | 00 01  | Bits16 |
            |  [0]   |   .sp  | True  |        | bool   |
            |  [1]   |   .r0  | False |        | bool   |
            |  [4]   |   .r1  | False |        | bool   |
            +--------+--------+-------+--------+--------+
            """)

    value = Register.SP

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+--------+
        | Offset | Access          | Value | Memory | Type   |
        +--------+-----------------+-------+--------+--------+
        | 0      | x               | 1     | 00 01  | Bits16 |
        |  [0]   |   .sp           | True  |        | bool   |
        |  [1]   |   .r0           | False |        | bool   |
        |  [4]   |   .r1           | False |        | bool   |
        | 2      | <excess memory> |       | 99     |        |
        +--------+-----------------+-------+--------+--------+

        1 unconsumed memory bytes (3 available, 2 consumed)
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+--------+
        | Offset | Access | Value                | Memory | Type   |
        +--------+--------+----------------------+--------+--------+
        | 0      | x      | <insufficient bytes> | 00     | Bits16 |
        +--------+--------+----------------------+--------+--------+

        InsufficientMemoryError: 1 too few memory bytes to unpack Bits16 (2
        needed, only 1 available), dump above shows interrupted progress
        """)

    def iter_instances(self):
        yield self.cls(self.value), 'instantiated from self.value'
        yield self.cls(1), 'instantiated from int'
