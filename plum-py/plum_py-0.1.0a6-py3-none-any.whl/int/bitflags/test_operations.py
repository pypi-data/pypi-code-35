# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Bitfield operations."""

import pytest
from baseline import Baseline

from . import BitFlags
from ...tests.utils import wrap_message


class Sample(BitFlags, nbytes=2, flag=True):

    """Test sample."""

    OPTION1 = 0x01
    OPTION2 = 0x02
    OPTION3 = 0x04


class TestOperations:

    """Oprations tests."""

    sample = Sample(2)

    def test_or(self):
        """Test logical or."""
        new_value = self.sample | Sample.OPTION3
        assert new_value == Sample.OPTION2 | Sample.OPTION3
        assert isinstance(new_value, Sample)

    def test_and(self):
        """Test logical and."""
        new_value = self.sample & Sample.OPTION3
        assert new_value == Sample.OPTION2 & Sample.OPTION3
        assert isinstance(new_value, Sample)

    def test_membership(self):
        """Test membership."""
        assert Sample.OPTION2 in self.sample
        assert Sample.OPTION1 not in self.sample

        with pytest.raises(TypeError) as trap:
            2 in self.sample  # pylint: disable=pointless-statement

        expected = Baseline("""
            Sample member must be used
            """)

        assert wrap_message(trap.value) == expected
