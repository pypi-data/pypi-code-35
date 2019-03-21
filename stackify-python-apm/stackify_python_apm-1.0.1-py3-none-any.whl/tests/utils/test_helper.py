from unittest import TestCase

from stackifyapm.utils.helper import get_current_time_in_millis
from stackifyapm.utils.helper import get_current_time_in_string


class TestGetCurrentTimeInMillis(TestCase):

    def test_should_be_float(self):
        time = get_current_time_in_millis()

        assert isinstance(time, float)

    def test_should_contain_at_least_13_characters(self):
        time = str(get_current_time_in_millis())

        assert len(time) >= 13

    def test_should_contain_decemal_point(self):
        time = str(get_current_time_in_millis())

        assert time.count('.') == 1


class TestGetCurrentTimeInString(TestCase):

    def test_should_be_string(self):
        time = get_current_time_in_string()

        assert isinstance(time, str)

    def test_should_be_13_characters(self):
        time = get_current_time_in_string()

        assert len(time) == 13

    def test_should_not_contain_decemal_point(self):
        time = get_current_time_in_string()

        assert time.count('.') == 0
