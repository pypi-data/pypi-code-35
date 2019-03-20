from unittest import TestCase

import thewhitetools


class TestJoke(TestCase):
    def test_is_string(self):
        s = "hi"
        assert s == "hi"
