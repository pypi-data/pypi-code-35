import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from asyncscheduler import AsyncScheduler
import time
from threading import Event


class TestAsyncScheduler(unittest.TestCase):
    def test00_init(self):
        a = AsyncScheduler()
        self.assertIsNotNone(a)

    def test01_start_stop(self):
        a = AsyncScheduler()
        self.assertIsNotNone(a)
        self.assertFalse(a._stop.is_set())
        a.start()
        self.assertFalse(a._stop.is_set())
        time.sleep(0.1)
        a.stop()
        self.assertTrue(a._stop.is_set())

    def test02_add_event_a(self):
        event1 = Event()

        a = AsyncScheduler()
        a.enter(0.1, 1, event1.set)
        a.start()
        self.assertTrue(event1.wait(0.2))
        a.stop()

    def test02_add_event_b(self):
        event1 = Event()

        a = AsyncScheduler()
        a.start()
        a.enter(0.1, 1, event1.set)
        self.assertTrue(event1.wait(0.2))
        a.stop()

    def test03_add_eventabs_a(self):
        event1 = Event()

        a = AsyncScheduler()
        a.enterabs(time.time()+0.1, 1, event1.set)
        a.start()
        self.assertTrue(event1.wait(0.2))
        a.stop()

    def test03_add_eventabs_b(self):
        event1 = Event()

        a = AsyncScheduler()
        a.start()
        a.enterabs(time.time()+0.1, 1, event1.set)
        self.assertTrue(event1.wait(0.2))
        a.stop()

    def test04_remove_event_a(self):
        event1 = Event()

        a = AsyncScheduler()
        e = a.enter(0.1, 1, event1.set)
        a.cancel(e)
        a.start()
        self.assertFalse(event1.wait(0.11))
        a.stop()

    def test04_remove_event_b(self):
        event1 = Event()

        a = AsyncScheduler()
        e = a.enter(0.1, 1, event1.set)
        a.start()
        a.cancel(e)
        self.assertFalse(event1.wait(0.11))
        a.stop()

    def test05_clear_scheduler_a(self):
        event1 = Event()
        event2 = Event()

        a = AsyncScheduler()
        a.enter(0.05, 1, event1.set)
        a.enter(0.07, 1, event2.set)
        a.clear_scheduler()
        self.assertTrue(a.scheduler.empty())
        a.start()
        self.assertFalse(event1.wait(0.06))
        self.assertFalse(event1.wait(0.03))
        a.stop()

    def test05_clear_scheduler_b(self):
        event1 = Event()
        event2 = Event()

        a = AsyncScheduler()
        a.enter(0.05, 1, event1.set)
        a.enter(0.07, 1, event2.set)
        a.start()
        a.clear_scheduler()
        self.assertTrue(a.scheduler.empty())
        self.assertFalse(event1.wait(0.06))
        self.assertFalse(event1.wait(0.03))
        a.stop()

    def test06_stop_wait(self):
        event1 = Event()
        event2 = Event()

        a = AsyncScheduler()
        a.enter(0.1, 1, event1.set)
        a.enter(0.1, 1, event2.set)
        start_time = time.time()
        a.start()
        self.assertFalse(event1.is_set())
        self.assertFalse(event2.is_set())
        self.assertTrue(len(a.scheduler.queue), 2)
        a.stop()
        time_diff = time.time() - start_time
        self.assertEqual(len(a.scheduler.queue), 0)
        self.assertTrue(event1.is_set())
        self.assertTrue(event2.is_set())
        self.assertAlmostEqual(time_diff, 0.1, 2)

    def test07_stop_nowait(self):
        event1 = Event()
        event2 = Event()

        a = AsyncScheduler()
        a.enter(0.1, 1, event1.set)
        a.enter(0.1, 1, event2.set)
        start_time = time.time()
        a.start()
        self.assertFalse(event1.is_set())
        self.assertFalse(event2.is_set())
        self.assertTrue(len(a.scheduler.queue), 2)
        a.stop(wait=False)
        time_diff = time.time() - start_time
        self.assertEqual(len(a.scheduler.queue), 0)
        self.assertFalse(event1.is_set())
        self.assertFalse(event2.is_set())
        self.assertLess(time_diff, 0.05)

    def test08_enter_args(self):
        def wait(event, duration):
            time.sleep(duration)
            event.set()

        event1 = Event()

        a = AsyncScheduler()
        a.enter(0.5, 1, wait, args=(event1, 0.5,))
        start_time = time.time()
        a.start()
        self.assertTrue(event1.wait(1.5))
        time_diff = time.time() - start_time
        self.assertLess(time_diff, 1.2)
        a.stop()

    def test09_enter_kwargs(self):
        def wait(event, duration):
            time.sleep(duration)
            event.set()

        event1 = Event()

        a = AsyncScheduler()
        a.enter(0.5, 1, wait, kwargs={"event":event1, "duration":0.5})
        start_time = time.time()
        a.start()
        self.assertTrue(event1.wait(1.5))
        time_diff = time.time() - start_time
        self.assertLess(time_diff, 1.2)
        a.stop()

    def test10_enter_args_kwargs(self):
        def wait(event, duration):
            time.sleep(duration)
            event.set()

        event1 = Event()

        a = AsyncScheduler()
        a.enter(0.5, 1, wait, args=(event1,), kwargs={"duration":0.5})
        start_time = time.time()
        a.start()
        self.assertTrue(event1.wait(1.5))
        time_diff = time.time() - start_time
        self.assertLess(time_diff, 1.2)
        a.stop()

    def test11_priorities(self):
        def add_to_list(list, name):
            list.append(name)

        l = []

        a = AsyncScheduler()
        t = time.time() + 0.05
        a.enterabs(t, action=add_to_list, args=(l, "a"), priority=2)
        a.enterabs(t, action=add_to_list, args=(l, "b"), priority=0)
        a.enterabs(t, action=add_to_list, args=(l, "c"), priority=1)

        a.start()
        a.stop()

        self.assertEqual(len(l), 3)
        self.assertListEqual(l, ["b", "c", "a"])


if __name__ == '__main__':
    unittest.main()


