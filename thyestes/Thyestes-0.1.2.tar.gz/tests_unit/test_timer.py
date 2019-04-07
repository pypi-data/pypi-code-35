import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.myconfigtools import read_config
from pelops.logging.mylogger import create_logger
import threading
import time
from thyestes.timer import Timer


class TestTimer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tests_unit/config.yaml"
        cls.main_config = read_config(cls.filename)
        cls.logger = create_logger(cls.main_config["logger"], "TestTimer")
        cls.logger.info("start ==============================================")

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("end ================================================")

    def setUp(self):
        self.logger.info("----------------------------------------------------")

    def tearDown(self):
        pass

    def test_0init(self):
        self.logger.info("")
        def temp():
            self.assertTrue(False)
        stop_signal = threading.Event()
        stop_signal.clear()
        timer = Timer(temp, stop_signal, self.logger)
        self.assertIsNotNone(timer)
        self.assertTrue(timer.is_stopped.is_set())

    def test_1set_timer(self):
        self.logger.info("test_1set_timer")
        global counter
        counter = 0
        event = threading.Event()
        event.clear()
        stop_signal = threading.Event()
        stop_signal.clear()
        seconds = 1

        def timer_event():
            global counter
            counter += 1
            event.set()

        timer = Timer(timer_event, stop_signal, self.logger)
        self.assertIsNotNone(timer)
        self.assertEqual(counter, 0)
        start = time.time()
        timer.set_timer(seconds)
        self.assertEqual(counter, 0)
        self.assertFalse(timer.is_stopped.is_set())
        time.sleep(seconds/2)
        self.assertEqual(counter, 0)
        self.assertFalse(timer.is_stopped.is_set())
        event.wait(seconds)
        self.assertTrue(event.is_set())
        timer.is_stopped.wait(seconds)
        self.assertTrue(timer.is_stopped.is_set())
        self.assertEqual(counter, 1)
        diff = time.time()-start
        self.assertGreaterEqual(diff, seconds)
        self.assertLess(diff, seconds+1)

    def test_2set_timer_three_times_sequentially(self):
        self.logger.info("test_2set_timer_three_times_sequentially")
        global counter
        counter = 0
        event = threading.Event()
        event.clear()
        stop_signal = threading.Event()
        stop_signal.clear()
        seconds = 0.5

        def timer_event():
            global counter
            counter += 1
            event.set()

        def test(test_timer, c):
            global counter
            self.assertEqual(counter, c-1)
            start = time.time()
            test_timer.set_timer(seconds)
            self.assertEqual(counter, c-1)
            self.assertFalse(test_timer.is_stopped.is_set())
            time.sleep(seconds/2)
            self.assertEqual(counter, c-1)
            self.assertFalse(test_timer.is_stopped.is_set())
            event.wait(seconds)
            self.assertTrue(event.is_set())
            event.clear()
            test_timer.is_stopped.wait(seconds)
            self.assertTrue(test_timer.is_stopped.is_set())
            self.assertEqual(counter, c)
            diff = time.time()-start
            self.assertGreaterEqual(diff, seconds)
            self.assertLess(diff, seconds + 1)

        timer = Timer(timer_event, stop_signal, self.logger)
        self.assertIsNotNone(timer)
        test(timer, 1)
        test(timer, 2)
        test(timer, 3)

    def test_3set_timer_three_times_overlapping(self):
        self.logger.info("test_3set_timer_three_times_overlapping")
        global counter
        counter = 0
        event = threading.Event()
        event.clear()
        stop_signal = threading.Event()
        stop_signal.clear()
        seconds = 1.5
        overlapwait = seconds/3

        def timer_event():
            global counter
            counter += 1
            event.set()

        timer = Timer(timer_event, stop_signal, self.logger)
        self.assertIsNotNone(timer)
        self.assertEqual(counter, 0)
        start = time.time()
        for i in range(3):
            timer.set_timer(seconds)
            self.assertEqual(counter, 0)
            self.assertFalse(timer.is_stopped.is_set())
            time.sleep(overlapwait)

        event.wait(seconds)
        self.assertTrue(event.is_set())
        event.clear()
        timer.is_stopped.wait(seconds)
        self.assertTrue(timer.is_stopped.is_set())
        self.assertEqual(counter, 1)
        diff = time.time() - start
        self.assertGreaterEqual(diff, seconds+overlapwait*2)
        self.assertLess(diff, seconds+overlapwait*2+1)

    def test_4stop_signal(self):
        self.logger.info("test_4stop_signal")
        global counter
        counter = 0
        event = threading.Event()
        event.clear()
        stop_signal = threading.Event()
        stop_signal.clear()
        seconds = 1

        def timer_event():
            global counter
            counter += 1
            event.set()

        timer = Timer(timer_event, stop_signal, self.logger)
        self.assertIsNotNone(timer)
        self.assertEqual(counter, 0)
        start = time.time()
        timer.set_timer(seconds)
        self.assertEqual(counter, 0)
        self.assertFalse(timer.is_stopped.is_set())
        time.sleep(seconds/2)
        self.assertEqual(counter, 0)
        self.assertFalse(timer.is_stopped.is_set())
        stop_signal.set()
        timer.is_stopped.wait(seconds)
        self.assertTrue(timer.is_stopped.is_set())
        self.assertEqual(counter, 0)
        event.wait(seconds)
        self.assertFalse(event.is_set())


if __name__ == '__main__':
    unittest.main()
