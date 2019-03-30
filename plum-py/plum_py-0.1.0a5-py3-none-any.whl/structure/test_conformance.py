# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from baseline import Baseline

from ..int.little import UInt16, UInt8
from ..structure import Structure
from ..tests.conformance import BasicConformance


class Custom(Structure):

    m1: UInt8
    m2: UInt16 = 0x9988


class Sample:

    """Conformance configuration."""

    bindata = b'\x01\x02\x00'

    cls = Custom

    cls_nbytes = 3

    dump = Baseline("""
    +--------+--------+-------+--------+--------+
    | Offset | Access | Value | Memory | Type   |
    +--------+--------+-------+--------+--------+
    |        | x      |       |        | Custom |
    | 0      |   .m1  | 1     | 01     | UInt8  |
    | 1      |   .m2  | 2     | 02 00  | UInt16 |
    +--------+--------+-------+--------+--------+
    """)

    retval_str = Baseline("""
        {'m1': 1, 'm2': 2}
        """)

    retval_repr = Baseline("""
        Custom({'m1': 1, 'm2': 2})
        """)

    value = {'m1': 1, 'm2': 2}

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+--------+
        | Offset | Access          | Value | Memory | Type   |
        +--------+-----------------+-------+--------+--------+
        |        | x               |       |        | Custom |
        | 0      |   .m1           | 1     | 01     | UInt8  |
        | 1      |   .m2           | 2     | 02 00  | UInt16 |
        | 3      | <excess memory> |       | 99     |        |
        +--------+-----------------+-------+--------+--------+

        1 unconsumed memory bytes
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+--------+
        | Offset | Access | Value                | Memory | Type   |
        +--------+--------+----------------------+--------+--------+
        |        | x      |                      |        | Custom |
        | 0      |   .m1  | 1                    | 01     | UInt8  |
        | 1      |   .m2  | <insufficient bytes> | 02     | UInt16 |
        +--------+--------+----------------------+--------+--------+

        InsufficientMemoryError: 1 too few memory bytes to unpack UInt16 (2
        needed, only 1 available), dump above shows interrupted progress
        """)


class TestBasicConformance(Sample, BasicConformance):

    """Test basic API conformance and utility usage."""

    # inherit test cases
