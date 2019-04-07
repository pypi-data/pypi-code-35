import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from pelops.logging.mylogger import create_logger
from thyestes.timerservice import Timerservice
from thyestes.spawntimer import SpawnTimer
from thyestes.restarttimer import RestartTimer
import threading
import time


class TestTimerService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tests_unit/config.yaml"
        cls.main_config = read_config(cls.filename)
        cls.logger = create_logger(cls.main_config["logger"], "TestTimerService")
        cls.mqttclient = MyMQTTClient(cls.main_config["mqtt"], cls.logger, True)
        cls.logger.info("start ==============================================")

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("end ================================================")

    def setUp(self):
        self.logger.info("----------------------------------------------------")

    def tearDown(self):
        pass

    def test_0init(self):
        self.logger.info("test_0init")
        ts = Timerservice(self.main_config, self.mqttclient, self.logger, no_gui=True)
        self.assertIsNotNone(ts)
        self.assertEqual(len(ts._controller), 2)
        self.assertEqual(type(ts._controller[0]), RestartTimer)
        self.assertEqual(type(ts._controller[1]), SpawnTimer)

    def test_1startstop(self):
        self.logger.info("test_1startstop")
        ts = Timerservice(self.main_config, self.mqttclient, self.logger, no_gui=True)

        self.assertTrue(ts._controller[0]._stop_timer.is_set())
        self.assertTrue(ts._controller[0]._timer.is_stopped.is_set())
        self.assertTrue(ts._controller[1]._stop_timer.is_set())
        self.assertEqual(len(ts._controller[1]._timer_list), 0)
        ts.start()
        self.assertFalse(ts._controller[0]._stop_timer.is_set())
        self.assertTrue(ts._controller[0]._timer.is_stopped.is_set())
        self.assertEqual(len(ts._controller[1]._timer_list), 0)
        ts.stop()
        self.assertTrue(ts._controller[0]._stop_timer.is_set())
        self.assertTrue(ts._controller[0]._timer.is_stopped.is_set())
        self.assertTrue(ts._controller[1]._stop_timer.is_set())
        self.assertEqual(len(ts._controller[1]._timer_list), 0)

    def test_2activate_restarttimer(self):
        self.logger.info("test_2activate_restarttimer")
        global counter_spawn
        counter_spawn = 0
        event_spawn = threading.Event()
        event_spawn.clear()

        global counter_restart
        counter_restart = 0
        event_restart = threading.Event()
        event_restart.clear()

        def mqtt_handler_spawn(value):
            value = value.decode()
            self.assertEqual(value, self.main_config["timerservice"][1]["timer-message"])
            global counter_spawn
            counter_spawn += 1
            event_spawn.set()

        def mqtt_handler_restart(value):
            value = value.decode()
            self.assertEqual(value, self.main_config["timerservice"][0]["timer-message"])
            global counter_restart
            counter_restart += 1
            event_restart.set()

        self.mqttclient.subscribe(self.main_config["timerservice"][0]["topic-pub"], mqtt_handler_restart)
        self.mqttclient.subscribe(self.main_config["timerservice"][1]["topic-pub"], mqtt_handler_spawn)

        ts = Timerservice(self.main_config, self.mqttclient, self.logger, no_gui=True)
        ts.start()
        self.assertFalse(event_restart.is_set())
        self.assertFalse(event_spawn.is_set())
        self.assertEqual(counter_restart, 0)
        self.assertEqual(counter_spawn, 0)
        self.mqttclient.publish(self.main_config["timerservice"][0]["topic-sub"],
                                self.main_config["timerservice"][0]["topic-command"])
        event_spawn.wait(3)
        self.assertFalse(event_spawn.is_set())
        event_restart.wait(3)
        self.assertTrue(event_restart.is_set())
        event_restart.clear()
        self.assertEqual(counter_restart, 1)
        self.assertEqual(counter_spawn, 0)
        ts.stop()

        self.mqttclient.unsubscribe(self.main_config["timerservice"][0]["topic-pub"], mqtt_handler_restart)
        self.mqttclient.unsubscribe(self.main_config["timerservice"][1]["topic-pub"], mqtt_handler_spawn)
        self.assertFalse(event_restart.is_set())
        self.assertFalse(event_spawn.is_set())
        self.assertEqual(counter_restart, 1)
        self.assertEqual(counter_spawn, 0)

    def test_3activate_spawntimer(self):
        self.logger.info("test_3activate_spawntimer")
        global counter_spawn
        counter_spawn = 0
        event_spawn = threading.Event()
        event_spawn.clear()

        global counter_restart
        counter_restart = 0
        event_restart = threading.Event()
        event_restart.clear()

        def mqtt_handler_spawn(value):
            value = value.decode()
            self.assertEqual(value, self.main_config["timerservice"][1]["timer-message"])
            global counter_spawn
            counter_spawn += 1
            event_spawn.set()

        def mqtt_handler_restart(value):
            value = value.decode()
            self.assertEqual(value, self.main_config["timerservice"][0]["timer-message"])
            global counter_restart
            counter_restart += 1
            event_restart.set()

        self.mqttclient.subscribe(self.main_config["timerservice"][0]["topic-pub"], mqtt_handler_restart)
        self.mqttclient.subscribe(self.main_config["timerservice"][1]["topic-pub"], mqtt_handler_spawn)

        ts = Timerservice(self.main_config, self.mqttclient, self.logger, no_gui=True)
        ts.start()
        self.assertFalse(event_restart.is_set())
        self.assertFalse(event_spawn.is_set())
        self.assertEqual(counter_restart, 0)
        self.assertEqual(counter_spawn, 0)
        self.mqttclient.publish(self.main_config["timerservice"][1]["topic-sub"],
                                self.main_config["timerservice"][1]["topic-command"])
        event_spawn.wait(3)
        self.assertTrue(event_spawn.is_set())
        event_spawn.clear()
        event_restart.wait(3)
        self.assertFalse(event_restart.is_set())
        self.assertEqual(counter_restart, 0)
        self.assertEqual(counter_spawn, 1)
        ts.stop()

        self.mqttclient.unsubscribe(self.main_config["timerservice"][0]["topic-pub"], mqtt_handler_restart)
        self.mqttclient.unsubscribe(self.main_config["timerservice"][1]["topic-pub"], mqtt_handler_spawn)
        self.assertFalse(event_restart.is_set())
        self.assertFalse(event_spawn.is_set())
        self.assertEqual(counter_restart, 0)
        self.assertEqual(counter_spawn, 1)

    def test_4activate_both(self):
        self.logger.info("test_4activate_both")
        global counter_spawn
        counter_spawn = 0
        event_spawn = threading.Event()
        event_spawn.clear()

        global counter_restart
        counter_restart = 0
        event_restart = threading.Event()
        event_restart.clear()

        def mqtt_handler_spawn(value):
            value = value.decode()
            self.assertEqual(value, self.main_config["timerservice"][1]["timer-message"])
            global counter_spawn
            counter_spawn += 1
            event_spawn.set()

        def mqtt_handler_restart(value):
            value = value.decode()
            self.assertEqual(value, self.main_config["timerservice"][0]["timer-message"])
            global counter_restart
            counter_restart += 1
            event_restart.set()

        self.mqttclient.subscribe(self.main_config["timerservice"][0]["topic-pub"], mqtt_handler_restart)
        self.mqttclient.subscribe(self.main_config["timerservice"][1]["topic-pub"], mqtt_handler_spawn)

        ts = Timerservice(self.main_config, self.mqttclient, self.logger, no_gui=True)
        ts.start()
        self.assertFalse(event_restart.is_set())
        self.assertFalse(event_spawn.is_set())
        self.assertEqual(counter_restart, 0)
        self.assertEqual(counter_spawn, 0)
        self.mqttclient.publish(self.main_config["timerservice"][0]["topic-sub"],
                                self.main_config["timerservice"][0]["topic-command"])
        self.mqttclient.publish(self.main_config["timerservice"][1]["topic-sub"],
                                self.main_config["timerservice"][1]["topic-command"])
        event_spawn.wait(3)
        self.assertTrue(event_spawn.is_set())
        event_spawn.clear()
        event_restart.wait(3)
        self.assertTrue(event_restart.is_set())
        event_restart.clear()
        self.assertEqual(counter_restart, 1)
        self.assertEqual(counter_spawn, 1)
        ts.stop()

        self.mqttclient.unsubscribe(self.main_config["timerservice"][0]["topic-pub"], mqtt_handler_restart)
        self.mqttclient.unsubscribe(self.main_config["timerservice"][1]["topic-pub"], mqtt_handler_spawn)
        self.assertFalse(event_restart.is_set())
        self.assertFalse(event_spawn.is_set())
        self.assertEqual(counter_restart, 1)
        self.assertEqual(counter_spawn, 1)

    def test_5stop_both(self):
        self.logger.info("test_5stop_both")
        global counter_spawn
        counter_spawn = 0
        event_spawn = threading.Event()
        event_spawn.clear()

        global counter_restart
        counter_restart = 0
        event_restart = threading.Event()
        event_restart.clear()

        def mqtt_handler_spawn(value):
            value = value.decode()
            self.assertEqual(value, self.main_config["timerservice"][1]["timer-message"])
            global counter_spawn
            counter_spawn += 1
            event_spawn.set()

        def mqtt_handler_restart(value):
            value = value.decode()
            self.assertEqual(value, self.main_config["timerservice"][0]["timer-message"])
            global counter_restart
            counter_restart += 1
            event_restart.set()

        self.mqttclient.subscribe(self.main_config["timerservice"][0]["topic-pub"], mqtt_handler_restart)
        self.mqttclient.subscribe(self.main_config["timerservice"][1]["topic-pub"], mqtt_handler_spawn)

        ts = Timerservice(self.main_config, self.mqttclient, self.logger, no_gui=True)
        ts.start()
        self.assertFalse(event_restart.is_set())
        self.assertFalse(event_spawn.is_set())
        self.assertEqual(counter_restart, 0)
        self.assertEqual(counter_spawn, 0)

        time.sleep(0.5)
        self.assertFalse(event_restart.is_set())
        self.assertFalse(event_spawn.is_set())
        self.assertEqual(counter_restart, 0)
        self.assertEqual(counter_spawn, 0)
        ts.stop()

        self.mqttclient.publish(self.main_config["timerservice"][0]["topic-sub"],
                                self.main_config["timerservice"][0]["topic-command"])
        self.mqttclient.publish(self.main_config["timerservice"][1]["topic-sub"],
                                self.main_config["timerservice"][1]["topic-command"])

        event_spawn.wait(3)
        self.assertFalse(event_spawn.is_set())
        event_restart.wait(3)
        self.assertFalse(event_restart.is_set())
        self.assertEqual(counter_restart, 0)
        self.assertEqual(counter_spawn, 0)

        self.mqttclient.unsubscribe(self.main_config["timerservice"][0]["topic-pub"], mqtt_handler_restart)
        self.mqttclient.unsubscribe(self.main_config["timerservice"][1]["topic-pub"], mqtt_handler_spawn)
        self.assertFalse(event_restart.is_set())
        self.assertFalse(event_spawn.is_set())
        self.assertEqual(counter_restart, 0)
        self.assertEqual(counter_spawn, 0)


if __name__ == '__main__':
    unittest.main()

