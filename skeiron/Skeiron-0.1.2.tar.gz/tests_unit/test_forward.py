import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from pelops.mylogger import create_logger
import threading
from skeiron.forward import Forward


class TestForward(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tests_unit/config.yaml"
        cls.main_config = read_config(cls.filename)
        cls.logger = create_logger(cls.main_config["logger"], "TestForward")
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
            "name": "relay1",
            "type": "forward",
            "topic-sub": "/test/relay/1/sub",
            "topic-pub": "/test/relay/1/pub",
            "active": True
        }

    def tearDown(self):
        self.mqttclient.unsubscribe_all()

    def test_0init(self):
        self.logger.info("test_0init")
        relay = Forward(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(len(relay._topics_sub), 1)
        self.assertEqual(len(relay._topics_pub), 1)
        self.assertEqual(relay._topics_sub[0], self.config["topic-sub"])
        self.assertEqual(relay._topics_pub[0], self.config["topic-pub"])
        self.assertEqual(len(self.mqttclient._topic_handler), 0)

    def test_1startstop(self):
        self.logger.info("test_1startstop")
        relay = Forward(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(len(self.mqttclient._topic_handler), 0)
        relay.start()
        self.assertEqual(len(self.mqttclient._topic_handler), 1)
        self.assertListEqual(list(self.mqttclient._topic_handler.keys()), [self.config["topic-sub"]])
        relay.stop()
        self.assertEqual(len(self.mqttclient._topic_handler), 0)

    def test_2relay(self):
        self.logger.info("test_2relay")

        event = threading.Event()
        event.clear()
        global counter
        counter = 0

        global received
        received = ""

        def handler(value):
            global counter
            global received
            received = value.decode("utf-8")
            counter += 1
            event.set()

        self.mqttclient.subscribe(self.config["topic-pub"], handler)
        relay = Forward(self.config, self.mqttclient, self.logger)
        relay.start()
        event.wait(0.5)
        self.assertFalse(event.is_set())
        self.assertEqual(counter, 0)
        self.mqttclient.publish(self.config["topic-sub"], "somerandomtext")
        event.wait(1)
        self.assertTrue(event.is_set())
        self.assertEqual(counter, 1)
        self.assertEqual(received, "somerandomtext")
        event.clear()
        relay.stop()
        self.assertFalse(event.is_set())
        self.assertEqual(counter, 1)

    def test_3relay_replace_message(self):
        self.logger.info("test_3relay_replace_message")

        event = threading.Event()
        event.clear()
        global counter
        counter = 0

        global received
        received = ""

        def handler(value):
            global counter
            global received
            received = value.decode("utf-8")
            counter += 1
            event.set()

        self.config["replace-message"] = "replace-message"
        self.mqttclient.subscribe(self.config["topic-pub"], handler)
        relay = Forward(self.config, self.mqttclient, self.logger)
        relay.start()
        event.wait(0.5)
        self.assertFalse(event.is_set())
        self.assertEqual(counter, 0)
        self.mqttclient.publish(self.config["topic-sub"], "somerandomtext")
        event.wait(1)
        self.assertTrue(event.is_set())
        self.assertEqual(counter, 1)
        self.assertEqual(received, "replace-message")
        event.clear()
        relay.stop()
        self.assertFalse(event.is_set())
        self.assertEqual(counter, 1)


if __name__ == '__main__':
    unittest.main()
