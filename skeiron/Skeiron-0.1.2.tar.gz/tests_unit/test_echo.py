import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from pelops.mylogger import create_logger
import threading
from skeiron.echo import Echo


class TestEcho(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tests_unit/config.yaml"
        cls.main_config = read_config(cls.filename)
        cls.logger = create_logger(cls.main_config["logger"], "TestEcho")
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
            "name": "relay2",
            "type": "echo",
            "topic": "/test/relay/2",
            "active": True
        }

    def tearDown(self):
        self.mqttclient.unsubscribe_all()

    def test_0init(self):
        self.logger.info("test_0init")
        relay = Echo(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(len(relay._topics_sub), 1)
        self.assertEqual(len(relay._topics_pub), 1)
        self.assertEqual(relay._topics_sub[0], self.config["topic"])
        self.assertEqual(relay._topics_pub[0], self.config["topic"])
        self.assertEqual(len(self.mqttclient._topic_handler), 0)

    def test_1startstop(self):
        self.logger.info("test_1startstop")
        relay = Echo(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(len(self.mqttclient._topic_handler), 0)
        relay.start()
        self.assertEqual(len(self.mqttclient._topic_handler), 1)
        self.assertListEqual(list(self.mqttclient._topic_handler.keys()), [self.config["topic"]])
        relay.stop()
        self.assertEqual(len(self.mqttclient._topic_handler), 0)

    def test_2relay(self):
        self.logger.info("test_2relay")

        event = threading.Event()
        event.clear()
        global counter
        counter = 0

        def handler(value):
            global counter
            counter += 1
            event.set()

        self.mqttclient.subscribe(self.config["topic"], handler)
        relay = Echo(self.config, self.mqttclient, self.logger)
        relay.start()
        event.wait(0.5)
        self.assertFalse(event.is_set())
        self.assertEqual(counter, 0)
        self.mqttclient.publish(self.config["topic"], "somerandomtext")
        event.wait(1)
        self.assertTrue(event.is_set())
        self.assertEqual(counter, 1)
        event.clear()
        relay.stop()
        self.assertFalse(event.is_set())
        self.assertEqual(counter, 1)


if __name__ == '__main__':
    unittest.main()
