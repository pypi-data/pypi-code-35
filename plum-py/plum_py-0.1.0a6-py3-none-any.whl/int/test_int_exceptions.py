# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer construction exceptions."""

import enum
import pytest

from baseline import Baseline

from plum import pack
from .little import UInt64
from plum import PackError

from ..tests.utils import wrap_message


class TestInit:

    """Test constructor."""

    def test_not_int_val(self):
        """Test not integer values."""
        # pylint: disable=unused-variable
        with pytest.raises(PackError) as trap:
            pack(UInt64, "str")

        expected = Baseline("""


            +--------+--------+-------+--------+--------+
            | Offset | Access | Value | Memory | Type   |
            +--------+--------+-------+--------+--------+
            |        | [0]    |       |        | UInt64 |
            +--------+--------+-------+--------+--------+

            PackError: unexpected TypeError exception occurred during pack
            operation, dump above shows interrupted progress, original exception
            traceback appears above this exception's traceback
            """)

        assert wrap_message(trap.value) == expected


