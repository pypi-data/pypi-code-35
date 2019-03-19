import time
import unittest

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_pump.process_data_pump import ProcessDataPump
from rover_position_rjg.data.data_pump.rate_limited_data_provider import RateLimitedDataProvider

frequency = 100


class TestDataProvider(RateLimitedDataProvider[int]):
    def __init__(self):
        super().__init__(frequency)
        self.closed = False
        self.start = time.clock()
        self.value = 0

    def get(self) -> Data[int]:
        self.value = self.value + 1
        return Data(self.value, time.time() - self.start)

    def close(self):
        self.closed = True


class ProcessDataPumpTest(unittest.TestCase):
    def setUp(self):
        self.frequency = frequency
        self.shortWait = (1 / self.frequency) * 5
        self.longWait = 5
        self.data_pump = ProcessDataPump(TestDataProvider, 1/self.frequency, 'TESTER')

    def tearDown(self):
        self.data_pump.halt()

    def test_name(self):
        self.assertEqual('TESTER', self.data_pump.name)

    def test_poll_times_out_when_data_not_available(self):
        data_ready = self.data_pump.poll(self.shortWait)

        self.assertFalse(data_ready)

    def test_poll_returns_true_if_data_is_ready(self):
        self.data_pump.run()
        data_ready = self.data_pump.poll(self.longWait)

        self.assertTrue(data_ready)

    def test_recv_returns_data_when_data_is_available(self):
        self.data_pump.run()
        self.data_pump.poll(self.longWait)

        data = self.data_pump.recv()

        self.assertIsNotNone(data)
        self.assertEqual(1, data.value)

    def test_can_recv_multiple_items(self):
        self.data_pump.run()

        for i in range(1, 5):
            if self.data_pump.poll(self.longWait):
                data = self.data_pump.recv()
                self.assertIsNotNone(data)
                self.assertEqual(i, data.value)
            else:
                self.fail("Expected more data")

    def test_skips_initial_samples(self):
        other_pump = ProcessDataPump(TestDataProvider, 1 / self.frequency, 'OTHER', initial_samples_to_reject=3)
        data: Data[int] = None
        try:
            other_pump.run()
            if other_pump.poll(self.longWait):
                data = other_pump.recv()
        finally:
            other_pump.halt()
        self.assertIsNotNone(data)
        self.assertEqual(4, data.value)

    def test_remaining_data_is_available_after_halt(self):
        self.data_pump.run()
        self.data_pump.poll(self.longWait)

        self.data_pump.halt()

        data = self.data_pump.recv()
        self.assertIsNotNone(data)
        self.assertEqual(1, data.value)

    def test_halt_stops_the_flow_of_data(self):
        self.data_pump.run()
        self.data_pump.poll(self.longWait)
        self.data_pump.halt()
        self.data_pump.recv()

        data_ready = self.data_pump.poll(self.shortWait)

        self.assertFalse(data_ready)

    def test_can_restart_pump(self):
        self.data_pump.run()
        self.data_pump.poll(self.longWait)
        self.data_pump.halt()
        self.data_pump.recv()

        self.data_pump.run()
        data_ready = self.data_pump.poll(self.longWait)

        self.assertTrue(data_ready)

    def test_can_pause_the_pump(self):
        self.data_pump.run()
        self.data_pump.poll(self.longWait)

        self.data_pump.pause()
        self.data_pump.recv()

        data_ready = self.data_pump.poll(self.shortWait)
        self.assertFalse(data_ready)

    def test_can_resume_pumping(self):
        self.data_pump.run()
        self.data_pump.poll(self.longWait)
        self.data_pump.pause()
        self.data_pump.recv()

        self.data_pump.resume()

        data_ready = self.data_pump.poll(self.shortWait)
        self.assertTrue(data_ready)

    def test_skips_samples_after_resume(self):
        other_pump = ProcessDataPump(TestDataProvider, 1 / self.frequency, 'OTHER', initial_samples_to_reject=0, samples_to_reject_on_resume=2)
        data: Data[int] = None
        try:
            other_pump.run()
            other_pump.pause()
            other_pump.resume()
            if other_pump.poll(self.longWait):
                data = other_pump.recv()
        finally:
            other_pump.halt()
        self.assertIsNotNone(data)
        self.assertEqual(3, data.value)

    def test_fileno(self):
        self.assertEqual(self.data_pump.receive_pipe.fileno(), self.data_pump.fileno())
