import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from pelops.mylogger import create_logger
from skeiron.relayfactory import RelayFactory
import skeiron.forward
import skeiron.echo
import skeiron.collect
import skeiron.distribute
import skeiron.multiply


class TestRelayFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tests_unit/config.yaml"
        cls.main_config = read_config(cls.filename)
        cls.logger = create_logger(cls.main_config["logger"], "TestRelayFactory")
        cls.mqttclient = MyMQTTClient(cls.main_config["mqtt"], cls.logger, True)
        cls.mqttclient.connect()

        cls.logger.info("start ==============================================")

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("end ================================================")
        cls.mqttclient.disconnect()

    def setUp(self):
        self.logger.info("----------------------------------------------------")

    def tearDown(self):
        self.mqttclient.unsubscribe_all()

    def test_0create_forward(self):
        self.logger.info("test_0create_forward")
        pos = 0
        self.assertEqual(self.main_config["relayservice"][pos]["type"], "forward")
        relay = RelayFactory.create_relay(self.main_config["relayservice"][pos], self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(type(relay), skeiron.forward.Forward)

    def test_1create_echo(self):
        self.logger.info("test_1create_echo")
        pos = 1
        self.assertEqual(self.main_config["relayservice"][pos]["type"], "echo")
        relay = RelayFactory.create_relay(self.main_config["relayservice"][pos], self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(type(relay), skeiron.echo.Echo)

    def test_2create_collect(self):
        self.logger.info("test_2create_collect")
        pos = 2
        self.assertEqual(self.main_config["relayservice"][pos]["type"], "collect")
        relay = RelayFactory.create_relay(self.main_config["relayservice"][pos], self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(type(relay), skeiron.collect.Collect)

    def test_3create_distribute(self):
        self.logger.info("test_3create_distribute")
        pos = 3
        self.assertEqual(self.main_config["relayservice"][pos]["type"], "distribute")
        relay = RelayFactory.create_relay(self.main_config["relayservice"][pos], self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(type(relay), skeiron.distribute.Distribute)

    def test_4create_multiply(self):
        self.logger.info("test_4create_multiply")
        pos = 4
        self.assertEqual(self.main_config["relayservice"][pos]["type"], "multiply")
        relay = RelayFactory.create_relay(self.main_config["relayservice"][pos], self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(type(relay), skeiron.multiply.Multiply)

    def test_5create_rubbish(self):
        self.logger.info("test_5create_rubbish")
        config = self.main_config["relayservice"][0].copy()
        config["type"] = "rubbish"
        with self.assertRaises(ValueError):
            relay = RelayFactory.create_relay(config, self.mqttclient, self.logger)

    def test_6create_relay_list(self):
        self.logger.info("test_6create_relay_list")
        self.assertEqual(len(self.main_config["relayservice"]), 6)
        list = RelayFactory.create_relay_list(self.main_config["relayservice"], self.mqttclient, self.logger)
        self.assertEqual(len(list), 5)
        expected_types = [skeiron.forward.Forward, skeiron.echo.Echo, skeiron.collect.Collect,
                          skeiron.distribute.Distribute, skeiron.multiply.Multiply]
        created_types = []
        for entry in list:
            created_types.append(type(entry))
        self.assertEqual(expected_types, created_types)


if __name__ == '__main__':
    unittest.main()
