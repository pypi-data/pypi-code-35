#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ptct` package."""

import pytest
import unittest

from ptct import ptct


@pytest.fixture
def error_fixture():
    assert 0


class TestPtct(unittest.TestCase):
    """Tests for `ptct` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_fahrenheit_to_rankine(self):
        assert int(ptct.convert(84.2, 'F', 'R')) == int(543.5)

    def test_celsius_to_kelvin(self):
        assert int(ptct.convert(-45.14, 'C', 'K')) == int(228.01)

    def test_kelvin_to_fahrenheit(self):
        assert int(ptct.convert(317.33, 'K', 'F')) == int(111.5)

    def test_rankine_to_celsius(self):
        assert int(ptct.convert(444.5, 'R', 'C')) == int(-26.2)

    def test_correct_response(self):
        assert ptct.check(ptct.convert(84.2, 'F', 'R'), 543.5) == 'correct'

    def test_incorrect_response(self):
        assert ptct.check(ptct.convert(84.2, 'F', 'R'), 550) == 'incorrect'

    def test_invalid_response(self):
        assert ptct.check(ptct.convert(6.5, 'F', 'R'), 'dog') == 'incorrect'

    def test_invalid_input(self):
        assert ptct.check(ptct.convert('dog', '', 'C'), 32) == 'invalid'
