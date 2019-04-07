import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from pelops.logging.mylogger import create_logger
import threading
import time
from thyestes.spawntimer import SpawnTimer


class TestSpawnTimer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tests_unit/config.yaml"
        cls.main_config = read_config(cls.filename)
        cls.logger = create_logger(cls.main_config["logger"], "TestSpawnTimer")
        cls.mqttclient = MyMQTTClient(cls.main_config["mqtt"], cls.logger, True)
        cls.mqttclient.connect()

        cls.logger.info("start ==============================================")

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("end ================================================")
        cls.mqttclient.disconnect()

    def setUp(self):
        self.logger.info("----------------------------------------------------")
        self.config = {
            "name": "test",
            "topic-sub": "/test/1/event",
            "topic-command": "start",
            "topic-pub": "/test/1/timer",
            "timer-message": "timer",
            "timer-value": 1
        }

    def tearDown(self):
        self.mqttclient.unsubscribe_all()

    def test_0init(self):
        self.logger.info("test_0init")
        st = SpawnTimer(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(st)
        self.assertEqual(st._timer_value, float(self.config["timer-value"]))
        self.assertEqual(st._topic_sub, self.config["topic-sub"])
        self.assertEqual(st._topic_command, self.config["topic-command"])
        self.assertEqual(st._topic_pub, self.config["topic-pub"])
        self.assertEqual(st._timer_message, self.config["timer-message"])
        self.assertEqual(len(st._timer_list), 0)

    def test_1start_stop(self):
        self.logger.info("test_1start_stop")
        st = SpawnTimer(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(st)
        self.assertTrue(st._stop_timer.is_set())
        self.assertEqual(len(st._timer_list), 0)
        st.start()
        self.assertEqual(len(st._timer_list), 0)
        st.stop()
        self.assertTrue(st._stop_timer.is_set())
        self.assertEqual(len(st._timer_list), 0)

    def test_2set_timer_once_happy(self):
        self.logger.info("test_2set_timer_once_happy")
        global counter
        counter = 0
        event = threading.Event()
        event.clear()

        def mqtt_handler(value):
            value = value.decode()
            self.assertEqual(value, self.config["timer-message"])
            global counter
            counter += 1
            event.set()

        self.mqttclient.subscribe(self.config["topic-pub"], mqtt_handler)
        st = SpawnTimer(self.config, self.mqttclient, self.logger)
        st.start()
        self.assertEqual(counter, 0)
        self.mqttclient.publish(self.config["topic-sub"], self.config["topic-command"])
        time.sleep(0.5)
        self.assertEqual(len(st._timer_list), 1)
        self.assertFalse(st._timer_list[0].is_stopped.is_set())
        event.wait(1)
        self.assertTrue(event.is_set())
        self.assertEqual(counter, 1)
        event.clear()
        st.stop()
        self.mqttclient.unsubscribe(self.config["topic-pub"], mqtt_handler)
        self.assertEqual(counter, 1)
        self.assertFalse(event.is_set())

    def test_3set_timer_once_onebad(self):
        self.logger.info("test_3set_timer_once_onebad")
        global counter
        counter = 0
        event = threading.Event()
        event.clear()

        def mqtt_handler(value):
            value = value.decode()
            self.assertEqual(value, self.config["timer-message"])
            global counter
            counter += 1
            event.set()

        self.mqttclient.subscribe(self.config["topic-pub"], mqtt_handler)
        st = SpawnTimer(self.config, self.mqttclient, self.logger)
        st.start()
        self.assertEqual(counter, 0)
        self.mqttclient.publish(self.config["topic-sub"], self.config["topic-command"]+"somerandomtext")
        time.sleep(0.5)
        self.assertEqual(len(st._timer_list),0)
        event.wait(1)
        self.assertFalse(event.is_set())
        self.assertEqual(counter, 0)
        st.stop()
        self.mqttclient.unsubscribe(self.config["topic-pub"], mqtt_handler)
        self.assertEqual(counter, 0)
        self.assertFalse(event.is_set())

    def test_4set_timer_once_nofilter(self):
        self.logger.info("test_4set_timer_once_nofilter")
        global counter
        counter = 0
        event = threading.Event()
        event.clear()

        def mqtt_handler(value):
            value = value.decode()
            self.assertEqual(value, self.config["timer-message"])
            global counter
            counter += 1
            event.set()

        self.config["topic-command"] = None
        self.mqttclient.subscribe(self.config["topic-pub"], mqtt_handler)
        st = SpawnTimer(self.config, self.mqttclient, self.logger)
        self.assertIsNone(st._topic_command)
        st.start()
        self.assertEqual(counter, 0)
        self.mqttclient.publish(self.config["topic-sub"], "somerandomtext")
        event.wait(5)
        self.assertTrue(event.is_set())
        self.assertEqual(counter, 1)
        event.clear()
        st.stop()
        self.mqttclient.unsubscribe(self.config["topic-pub"], mqtt_handler)
        self.assertEqual(counter, 1)
        self.assertFalse(event.is_set())

    def test_5set_timer_three_times_sequentially(self):
        self.logger.info("test_5set_timer_three_times_sequentially")
        global counter
        counter = 0
        event = threading.Event()
        event.clear()

        def mqtt_handler(value):
            self.logger.info(",,,,,,")
            value = value.decode()
            self.assertEqual(value, self.config["timer-message"])
            global counter
            counter += 1
            event.set()

        self.mqttclient.subscribe(self.config["topic-pub"], mqtt_handler)
        st = SpawnTimer(self.config, self.mqttclient, self.logger)
        st.start()

        for i in range(3):
            self.logger.info("............................")
            self.assertEqual(counter, i)
            self.mqttclient.publish(self.config["topic-sub"], self.config["topic-command"])
            time.sleep(0.5)
            if i == 0:
                self.assertEqual(len(st._timer_list), 1)
            else:
                self.assertEqual(len(st._timer_list), 2)
            event.wait(1)
            self.assertTrue(event.is_set())
            self.assertEqual(counter, i+1)
            self.assertEqual(len(st._timer_list), 1)
            event.clear()

        st.stop()
        self.assertEqual(len(st._timer_list), 0)
        self.mqttclient.unsubscribe(self.config["topic-pub"], mqtt_handler)
        self.assertEqual(counter, 3)
        self.assertFalse(event.is_set())

    def test_6set_timer_three_times_overlapping(self):
        self.logger.info("test_6set_timer_three_times_overlapping")
        global counter
        counter = 0
        event = threading.Event()
        event.clear()

        def mqtt_handler(value):
            value = value.decode()
            self.assertEqual(value, self.config["timer-message"])
            global counter
            counter += 1
            event.set()

        self.config["timer-value"] = 1
        self.mqttclient.subscribe(self.config["topic-pub"], mqtt_handler)
        st = SpawnTimer(self.config, self.mqttclient, self.logger)
        st.start()

        for i in range(3):
            self.mqttclient.publish(self.config["topic-sub"], self.config["topic-command"])
            time.sleep(0.5)

        time.sleep(2)
        self.assertTrue(event.is_set())
        event.clear()
        self.assertEqual(counter, 3)

        st.stop()
        self.mqttclient.unsubscribe(self.config["topic-pub"], mqtt_handler)
        self.assertEqual(counter, 3)
        self.assertFalse(event.is_set())

    def test_7set_timer_stop_signal(self):
        self.logger.info("test_7set_timer_stop_signal")
        global counter
        counter = 0
        event = threading.Event()
        event.clear()

        def mqtt_handler(value):
            value = value.decode()
            self.assertEqual(value, self.config["timer-message"])
            global counter
            counter += 1
            event.set()

        self.config["timer-value"] = 1
        self.mqttclient.subscribe(self.config["topic-pub"], mqtt_handler)
        st = SpawnTimer(self.config, self.mqttclient, self.logger)
        st.start()
        self.mqttclient.publish(self.config["topic-sub"], self.config["topic-command"])

        time.sleep(0.5)
        self.assertFalse(event.is_set())
        self.assertEqual(counter, 0)

        st.stop()
        self.assertEqual(len(st._timer_list), 0)
        self.mqttclient.unsubscribe(self.config["topic-pub"], mqtt_handler)
        event.wait(1)
        self.assertEqual(counter, 0)
        self.assertFalse(event.is_set())


if __name__ == '__main__':
    unittest.main()
