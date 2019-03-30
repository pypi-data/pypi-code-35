# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test little endian byte order integer enum forms."""

from baseline import Baseline

from ..tests.conformance import BasicConformance

from .little import Float32


class TestFloat(BasicConformance):

    """Test Float class construction."""

    bindata = b'\x00\x00\x20\x40'

    cls = Float32

    cls_nbytes = 4

    dump = Baseline("""
            +--------+--------+-------+-------------+---------+
            | Offset | Access | Value | Memory      | Type    |
            +--------+--------+-------+-------------+---------+
            | 0      | x      | 2.5   | 00 00 20 40 | Float32 |
            +--------+--------+-------+-------------+---------+
            """)

    value = 2.5

    unpack_cls = float

    unpack_excess = Baseline("""


        +--------+-----------------+-------+-------------+---------+
        | Offset | Access          | Value | Memory      | Type    |
        +--------+-----------------+-------+-------------+---------+
        | 0      | x               | 2.5   | 00 00 20 40 | Float32 |
        | 4      | <excess memory> |       | 99          |         |
        +--------+-----------------+-------+-------------+---------+

        1 unconsumed memory bytes
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+----------+---------+
        | Offset | Access | Value                | Memory   | Type    |
        +--------+--------+----------------------+----------+---------+
        | 0      | x      | <insufficient bytes> | 00 00 20 | Float32 |
        +--------+--------+----------------------+----------+---------+

        InsufficientMemoryError: 1 too few memory bytes to unpack Float32 (4
        needed, only 3 available), dump above shows interrupted progress
        """)

    def iter_instances(self):
        yield self.cls(self.value), 'instantiated from self.value'

