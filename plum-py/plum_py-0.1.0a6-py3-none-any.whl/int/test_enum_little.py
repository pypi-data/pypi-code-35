# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test little endian byte order integer enum forms."""

from enum import IntEnum

from baseline import Baseline

from . import Int

from ..tests.conformance import BasicConformance


class Register(IntEnum):

    PC = 0
    SP = 1
    R0 = 2
    R1 = 3


class TestDefaultByteOrder(BasicConformance):

    """Test little endian is default for int enum class construction."""

    bindata = b'\x01\x00'

    class Register16(Int, nbytes=2, enum=Register):
        pass

    cls = Register16

    del Register16

    cls_nbytes = 2

    dump = Baseline("""
            +--------+--------+-------------+--------+------------+
            | Offset | Access | Value       | Memory | Type       |
            +--------+--------+-------------+--------+------------+
            | 0      | x      | Register.SP | 01 00  | Register16 |
            +--------+--------+-------------+--------+------------+
            """)

    value = Register.SP

    unpack_excess = Baseline("""


        +--------+-----------------+-------------+--------+------------+
        | Offset | Access          | Value       | Memory | Type       |
        +--------+-----------------+-------------+--------+------------+
        | 0      | x               | Register.SP | 01 00  | Register16 |
        | 2      | <excess memory> |             | 99     |            |
        +--------+-----------------+-------------+--------+------------+

        1 unconsumed memory bytes (3 available, 2 consumed)
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+------------+
        | Offset | Access | Value                | Memory | Type       |
        +--------+--------+----------------------+--------+------------+
        | 0      | x      | <insufficient bytes> | 01     | Register16 |
        +--------+--------+----------------------+--------+------------+

        InsufficientMemoryError: 1 too few memory bytes to unpack Register16
        (2 needed, only 1 available), dump above shows interrupted progress
        """)

    def iter_instances(self):
        yield self.cls(self.value), 'instantiated from self.value'
        yield self.cls('1', base=16), 'instantiated from str and base'
        yield self.cls(1), 'instantiated from int'


class TestAssignedByteOrder(TestDefaultByteOrder):

    """Test assignment of little endian during int enum class construction."""

    class Register16(Int, nbytes=2, enum=Register, byteorder='little'):
        pass

    cls = Register16

    del Register16
