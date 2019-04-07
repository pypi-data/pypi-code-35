import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from pelops.logging.mylogger import create_logger
from thyestes.timerfactory import TimerFactory
from thyestes.spawntimer import SpawnTimer
from thyestes.restarttimer import RestartTimer


class TestTimerFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tests_unit/config.yaml"
        cls.main_config = read_config(cls.filename)
        cls.logger = create_logger(cls.main_config["logger"], "TestTimerFactory")
        cls.mqttclient = MyMQTTClient(cls.main_config["mqtt"], cls.logger, True)
        cls.logger.info("start ==============================================")

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("end ================================================")

    def setUp(self):
        self.logger.info("----------------------------------------------------")

    def tearDown(self):
        pass

    def test_0create_controller_restarttimer(self):
        self.logger.info("test_0create_controller_restarttimer")
        c = TimerFactory.create_controller(self.main_config["timerservice"][0], self.mqttclient, self.logger)
        self.assertIsNotNone(c)
        self.assertTrue(type(c), RestartTimer)

    def test_1create_controller_spawntimer(self):
        self.logger.info("test_1create_controller_spawntimer")
        c = TimerFactory.create_controller(self.main_config["timerservice"][1], self.mqttclient, self.logger)
        self.assertIsNotNone(c)
        self.assertTrue(type(c), SpawnTimer)

    def test_2create_controller_inactive(self):
        self.logger.info("test_2create_controller_inactive")
        c = TimerFactory.create_controller(self.main_config["timerservice"][2], self.mqttclient, self.logger)
        self.assertIsNone(c)

    def test_3create_controller_unknown(self):
        self.logger.info("test_3create_controller_unknown")
        conf = self.main_config["timerservice"][1].copy()
        conf["on-new-command-behavior"] = "somerandomtext"
        with self.assertRaises(ValueError):
            c = TimerFactory.create_controller(conf, self.mqttclient, self.logger)

    def test_4create_controllers(self):
        self.logger.info("test_4create_controllers")
        c = TimerFactory.create_controller_list(self.main_config["timerservice"], self.mqttclient, self.logger)
        self.assertIsNotNone(c)
        self.assertEqual(len(c), 2)


if __name__ == '__main__':
    unittest.main()
