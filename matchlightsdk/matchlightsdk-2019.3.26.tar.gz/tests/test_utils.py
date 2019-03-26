"""Unit tests the utils module of Matchlight SDK."""
import pytest

import matchlight


@pytest.mark.parametrize('test_input,expected', [
    (None, '*****'),
    ('', '*****'),
    ('a', 'a****'),
    ('foobar', 'f****'),
    ('terbiumlabs', 't****'),
])
def test_blind_name(test_input, expected):
    """Verify test cases for blind_name."""
    assert matchlight.utils.blind_name(test_input) == expected


@pytest.mark.parametrize('test_input,expected', [
    (None, '*****'),
    ('', '*****'),
    ('a@terbiumlabs.com', 'a****@terbiumlabs.com'),
    ('ab@terbiumlabs.com', 'a****@terbiumlabs.com'),
    ('abc@terbiumlabs.com', 'a****@terbiumlabs.com'),
    ('abcd@terbiumlabs.com', 'ab****@terbiumlabs.com'),
    ('abcde@terbiumlabs.com', 'ab****@terbiumlabs.com'),
    ('abcdef@terbiumlabs.com', 'abc****@terbiumlabs.com'),
    ('abcdefg@terbiumlabs.com', 'abc****@terbiumlabs.com'),
    ('abcdefgh@terbiumlabs.com', 'abc****@terbiumlabs.com'),
])
def test_blind_email(test_input, expected):
    """Verify test cases for blind_email."""
    assert matchlight.utils.blind_email(test_input) == expected
