# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test little endian byte order integer enum forms."""

from baseline import Baseline
import pytest

from ..tests.conformance import BasicConformance
from .. tests.utils import wrap_message
from . import Nil
from plum import PackError

class TestNil(BasicConformance):

    """Test Nil class construction."""

    bindata = b''

    cls = Nil

    cls_nbytes = 0

    retval_str = "Nil()"
    retval_repr = "Nil()"

    dump = Baseline("""
            +--------+--------+-------+--------+------+
            | Offset | Access | Value | Memory | Type |
            +--------+--------+-------+--------+------+
            |        | x      | nil   |        | Nil  |
            +--------+--------+-------+--------+------+
            """)

    value = None

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+------+
        | Offset | Access          | Value | Memory | Type |
        +--------+-----------------+-------+--------+------+
        |        | x               | nil   |        | Nil  |
        | 0      | <excess memory> |       | 99     |      |
        +--------+-----------------+-------+--------+------+

        1 unconsumed memory bytes
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


class TestNilClass:

    def test_subclass(self):
        """Test subclass."""
        # pylint: disable=unused-variable
        with pytest.raises(TypeError) as trap:
            class MyNil(Nil): pass

        expected = Baseline("""
            type 'Nil' is not an acceptable base type
            """)

        assert wrap_message(trap.value) == expected

    def test_init_not_nil(self):
        """Test test init not nil."""
        # pylint: disable=unused-variable
        with pytest.raises(TypeError) as trap:
            Nil(1)

        expected = Baseline("""
            Nil() argument must be a 'nil' or 'None'
            """)

        assert wrap_message(trap.value) == expected


class TestNilinstance:

    def test_not_equal(self):
        sample = Nil()
        assert sample != 1
