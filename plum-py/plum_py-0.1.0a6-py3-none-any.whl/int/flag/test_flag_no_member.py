# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test flag type behavior with no members."""

from baseline import Baseline

from ...tests.conformance import BasicConformance

from .little import Flag16


class TestNoMember(BasicConformance):

    """Test flag type behavior with no members."""

    bindata = b'\x11\x00'

    cls = Flag16

    cls_nbytes = 2

    dump = Baseline("""
            +--------+--------+-------+--------+--------+
            | Offset | Access | Value | Memory | Type   |
            +--------+--------+-------+--------+--------+
            | 0      | x      | 17    | 11 00  | Flag16 |
            +--------+--------+-------+--------+--------+
            """)

    value = 17

    retval_str = 'Flag16.16|1'

    retval_repr = '<Flag16.16|1: 17>'

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+--------+
        | Offset | Access          | Value | Memory | Type   |
        +--------+-----------------+-------+--------+--------+
        | 0      | x               | 17    | 11 00  | Flag16 |
        | 2      | <excess memory> |       | 99     |        |
        +--------+-----------------+-------+--------+--------+

        1 unconsumed memory bytes
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+--------+
        | Offset | Access | Value                | Memory | Type   |
        +--------+--------+----------------------+--------+--------+
        | 0      | x      | <insufficient bytes> | 11     | Flag16 |
        +--------+--------+----------------------+--------+--------+

        InsufficientMemoryError: 1 too few memory bytes to unpack Flag16 (2
        needed, only 1 available), dump above shows interrupted progress
        """)
