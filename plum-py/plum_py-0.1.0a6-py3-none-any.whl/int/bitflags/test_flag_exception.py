# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test flag bitfield construction exceptions."""

from enum import IntEnum, IntFlag

import pytest
from baseline import Baseline

from . import BitFlags
from ...tests.utils import wrap_message


class MyEnum(IntEnum):

    """Sample enumeration."""

    A = 1
    B = 2


class MyFlag(IntFlag):

    """Flag definition."""

    A = 1
    B = 2


class TestInit:

    """Test constructor."""

    def test_invalid_flag_class(self):
        """Test invalid flag class."""
        # pylint: disable=unused-variable
        with pytest.raises(TypeError) as trap:
            class MyBits(BitFlags, nbytes=2, flag=MyEnum):
                # pylint: disable=missing-docstring
                # pylint: disable=too-few-public-methods
                pass

        expected = Baseline("""
            invalid enum, expected IntFlag subclass or True
            """)

        assert wrap_message(trap.value) == expected

    def test_invalid_flag_anotation(self):
        """Test invalid flag flag parameter together with anotations."""
        # pylint: disable=unused-variable
        with pytest.raises(TypeError) as trap:
            class MyBits(BitFlags, nbytes=2, flag=MyFlag):
                # pylint: disable=missing-docstring
                # pylint: disable=too-few-public-methods
                invalid: int

        expected = Baseline("""
            subclass may not contain bitfield definitions (or any annotation) when
            'flag' argument specifies an integer flag enumeration
            """)

        assert wrap_message(trap.value) == expected
