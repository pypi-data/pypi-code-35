# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test flag bitfield behavior when members are defined in namespace of class."""

from baseline import Baseline

from . import BitFlags

from ...tests.conformance import BasicConformance


class Sample(BitFlags, nbytes=2, flag=True):
    # pylint: disable=too-few-public-methods

    """Test sample."""

    CENTER = 0x01
    LEFT = 0x02
    RIGHT = 0x04

    def custom(self):
        pass


class TestNamespaceFlag(BasicConformance):

    """Test namespace flag bitfield definition."""

    bindata = b'\x05\x00'

    cls = Sample

    cls_nbytes = 2

    dump = Baseline("""
            +--------+-----------+-------+--------+--------+
            | Offset | Access    | Value | Memory | Type   |
            +--------+-----------+-------+--------+--------+
            | 0      | x         | 5     | 05 00  | Sample |
            |  [0]   |   .center | True  |        | bool   |
            |  [1]   |   .left   | False |        | bool   |
            |  [2]   |   .right  | True  |        | bool   |
            +--------+-----------+-------+--------+--------+
            """)

    value = Sample.CENTER | Sample.RIGHT

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+--------+
        | Offset | Access          | Value | Memory | Type   |
        +--------+-----------------+-------+--------+--------+
        | 0      | x               | 5     | 05 00  | Sample |
        |  [0]   |   .center       | True  |        | bool   |
        |  [1]   |   .left         | False |        | bool   |
        |  [2]   |   .right        | True  |        | bool   |
        | 2      | <excess memory> |       | 99     |        |
        +--------+-----------------+-------+--------+--------+

        1 unconsumed memory bytes (3 available, 2 consumed)
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+--------+
        | Offset | Access | Value                | Memory | Type   |
        +--------+--------+----------------------+--------+--------+
        | 0      | x      | <insufficient bytes> | 05     | Sample |
        +--------+--------+----------------------+--------+--------+

        InsufficientMemoryError: 1 too few memory bytes to unpack Sample (2
        needed, only 1 available), dump above shows interrupted progress
        """)
