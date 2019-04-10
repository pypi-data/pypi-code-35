# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test big endian byte order integer enum forms."""

from enum import IntEnum

from baseline import Baseline

from . import Int

from ..tests.conformance import BasicConformance


class Register(IntEnum):

    PC = 0
    SP = 1
    R0 = 2
    R1 = 3


class TestAssignedByteOrder(BasicConformance):

    """Test assignment of big endian during int enum class construction."""

    bindata = b'\x00\x01'

    class Register16(Int, nbytes=2, enum=Register, byteorder='big'):
        pass

    cls = Register16

    del Register16

    cls_nbytes = 2

    dump = Baseline("""
            +--------+--------+-------------+--------+------------+
            | Offset | Access | Value       | Memory | Type       |
            +--------+--------+-------------+--------+------------+
            | 0      | x      | Register.SP | 00 01  | Register16 |
            +--------+--------+-------------+--------+------------+
            """)

    value = Register.SP

    unpack_excess = Baseline("""


        +--------+-----------------+-------------+--------+------------+
        | Offset | Access          | Value       | Memory | Type       |
        +--------+-----------------+-------------+--------+------------+
        | 0      | x               | Register.SP | 00 01  | Register16 |
        | 2      | <excess memory> |             | 99     |            |
        +--------+-----------------+-------------+--------+------------+

        1 unconsumed memory bytes (3 available, 2 consumed)
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
        yield self.cls('1', base=16), 'instantiated from str and base'
        yield self.cls(1), 'instantiated from int'
