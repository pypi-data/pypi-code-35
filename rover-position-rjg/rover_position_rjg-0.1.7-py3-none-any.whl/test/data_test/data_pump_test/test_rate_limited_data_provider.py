import unittest

from rover_position_rjg.data.data_pump.rate_limited_data_provider import *


class TestDataProvider(RateLimitedDataProvider[int]):
    def __init__(self):
        super().__init__(10)
        self.start = time.time()
        self.value = 0

    def get(self) -> Data[int]:
        self.value = self.value + 1
        return Data(self.value, time.time() - self.start)

    def close(self):
        pass


class TestRateLimitedDataProvider(unittest.TestCase):
    def setUp(self):
        self.frequency = 10
        self.veryShortWait = (1 / self.frequency) / 5
        self.shortWait = (1 / self.frequency) * 5
        self.longWait = 5
        self.provider = TestDataProvider()

    def test_poll_returns_true_immediately(self):
        data_ready = self.provider.poll(0)
        # Assert
        self.assertTrue(data_ready)

    def test_poll_times_out_when_data_not_available(self):
        self.provider.poll(0)  # Clear the initial ready value
        data_ready = self.provider.poll(self.veryShortWait)
        # Assert
        self.assertFalse(data_ready)

    def test_poll_returns_true_if_data_is_ready(self):
        self.provider.poll(0)  # Clear the initial ready value
        data_ready = self.provider.poll(self.shortWait)
        # Assert
        self.assertTrue(data_ready)

    def test_poll_returns_false_if_called_twice_in_quick_succession(self):
        self.provider.poll(0)
        data_ready = self.provider.poll(0)
        # Assert
        self.assertFalse(data_ready)

    def test_poll_returns_true_both_time_if_called_with_waits(self):
        self.provider.poll(0)  # Clear the initial ready value
        data_ready = self.provider.poll(self.shortWait)
        self.assertTrue(data_ready)  # Make sure we hit it once
        data_ready = self.provider.poll(self.shortWait)
        # Assert
        self.assertTrue(data_ready)

    def test_poll_will_eventually_return_true(self):
        self.provider.poll(0)  # Clear the initial ready value
        data_ready = False
        iterations = 0
        while not data_ready and iterations < 20:
            data_ready = self.provider.poll(self.veryShortWait)
            iterations += 1
        self.assertTrue(iterations > 1)
        self.assertTrue(iterations < 15)
