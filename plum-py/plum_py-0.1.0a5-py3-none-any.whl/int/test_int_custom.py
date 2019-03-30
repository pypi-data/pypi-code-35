# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test default Int and variants using subclass keyword args."""

from baseline import Baseline

from . import Int

from .. import pack, unpack
from ..tests.conformance import BasicConformance


class TestDefault(BasicConformance):

    """Test Int class defaults to unsigned, little endian, 32 bit."""

    bindata = b'\x02\x01\x00\x00'

    cls = Int

    cls_nbytes = 4

    dump = Baseline("""
            +--------+--------+-------+-------------+------+
            | Offset | Access | Value | Memory      | Type |
            +--------+--------+-------+-------------+------+
            | 0      | x      | 258   | 02 01 00 00 | Int  |
            +--------+--------+-------+-------------+------+
            """)

    pack = staticmethod(pack)

    value = 0x102

    unpack = staticmethod(unpack)

    unpack_cls = int

    unpack_excess = Baseline("""


        +--------+-----------------+-------+-------------+------+
        | Offset | Access          | Value | Memory      | Type |
        +--------+-----------------+-------+-------------+------+
        | 0      | x               | 258   | 02 01 00 00 | Int  |
        | 4      | <excess memory> |       | 99          |      |
        +--------+-----------------+-------+-------------+------+

        1 unconsumed memory bytes
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+----------+------+
        | Offset | Access | Value                | Memory   | Type |
        +--------+--------+----------------------+----------+------+
        | 0      | x      | <insufficient bytes> | 02 01 00 | Int  |
        +--------+--------+----------------------+----------+------+

        InsufficientMemoryError: 1 too few memory bytes to unpack Int (4
        needed, only 3 available), dump above shows interrupted progress
        """)
