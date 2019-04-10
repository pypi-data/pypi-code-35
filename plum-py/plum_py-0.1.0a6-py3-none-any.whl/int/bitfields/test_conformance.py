# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from baseline import Baseline

from ...tests.conformance import BasicConformance
from .test_features import MyBits, MyEnum


class Sample:

    """Conformance configuration."""

    bindata = b'\x00\x12'

    cls = MyBits

    cls_nbytes = 2

    dump = Baseline("""
        +---------+--------+----------+--------+--------+
        | Offset  | Access | Value    | Memory | Type   |
        +---------+--------+----------+--------+--------+
        | 0       | x      | 4608     | 00 12  | MyBits |
        |  [0:7]  |   .f1  | 0        |        | int    |
        |  [8:11] |   .f2  | MyEnum.B |        | MyEnum |
        |  [12]   |   .f3  | True     |        | bool   |
        +---------+--------+----------+--------+--------+
        """)

    retval_str = Baseline("""
        {'f1'=0, 'f2'=MyEnum.B, 'f3'=True}
        """)

    retval_repr = Baseline("""
        MyBits({'f1'=0, 'f2'=<MyEnum.B: 2>, 'f3'=True})
        """)

    value = {'f1': 0, 'f2': MyEnum.B, 'f3': True}

    unpack_excess = Baseline("""


        +---------+-----------------+----------+--------+--------+
        | Offset  | Access          | Value    | Memory | Type   |
        +---------+-----------------+----------+--------+--------+
        | 0       | x               | 4608     | 00 12  | MyBits |
        |  [0:7]  |   .f1           | 0        |        | int    |
        |  [8:11] |   .f2           | MyEnum.B |        | MyEnum |
        |  [12]   |   .f3           | True     |        | bool   |
        | 2       | <excess memory> |          | 99     |        |
        +---------+-----------------+----------+--------+--------+

        1 unconsumed memory bytes
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+--------+
        | Offset | Access | Value                | Memory | Type   |
        +--------+--------+----------------------+--------+--------+
        | 0      | x      | <insufficient bytes> | 00     | MyBits |
        +--------+--------+----------------------+--------+--------+

        InsufficientMemoryError: 1 too few memory bytes to unpack MyBits (2
        needed, only 1 available), dump above shows interrupted progress
        """)


class TestBasicConformance(Sample, BasicConformance):

    """Test basic API conformance and utility usage."""

    # inherit test cases
