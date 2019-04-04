import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from pelops.mylogger import create_logger
import threading
import time
from skeiron.multiply import Multiply


class TestMultiply(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tests_unit/config.yaml"
        cls.main_config = read_config(cls.filename)
        cls.logger = create_logger(cls.main_config["logger"], "TestMultiply")
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
            "name": "relay5",
            "type": "multiply",
            "topics-sub": [
                "/test/relay/5/sub1",
                "/test/relay/5/sub2",
                "/test/relay/5/sub3",
            ],
            "topics-pub": [
                "/test/relay/5/pub1",
                "/test/relay/5/pub2",
                "/test/relay/5/pub3"
            ],
            "active": True
        }

    def tearDown(self):
        self.mqttclient.unsubscribe_all()

    def test_0init(self):
        self.logger.info("test_0init")
        relay = Multiply(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(len(relay._topics_sub), len(self.config["topics-sub"]))
        self.assertEqual(len(relay._topics_pub), len(self.config["topics-pub"]))
        self.assertListEqual(relay._topics_sub, self.config["topics-sub"])
        self.assertListEqual(relay._topics_pub, self.config["topics-pub"])
        self.assertEqual(len(self.mqttclient._topic_handler), 0)

    def test_1startstop(self):
        self.logger.info("test_1startstop")
        relay = Multiply(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(len(self.mqttclient._topic_handler), 0)
        relay.start()
        self.assertEqual(len(self.mqttclient._topic_handler), len(self.config["topics-sub"]))
        self.assertEqual(list(self.mqttclient._topic_handler.keys()), self.config["topics-sub"])
        relay.stop()
        self.assertEqual(len(self.mqttclient._topic_handler), 0)

    def test_2relay(self):
        self.logger.info("test_2relay")

        class EventHandler:
            event = None
            counter = None
            topic = None
            mqttclient = None

            def __init__(self, topic, mqttclient):
                self.topic = topic
                self.mqttclient  = mqttclient
                self.event = threading.Event()
                self.event.clear()
                self.counter = 0

            def start(self):
                self.mqttclient.subscribe(self.topic, self.handler)

            def stop(self):
                self.mqttclient.unsubscribe(self.topic, self.handler)

            def handler(self, value):
                self.counter += 1
                self.event.set()

        event_handlers = []

        for topic in self.config["topics-pub"]:
            eh = EventHandler(topic, self.mqttclient)
            eh.start()
            event_handlers.append(eh)

        relay = Multiply(self.config, self.mqttclient, self.logger)
        relay.start()
        time.sleep(0.5)
        for eh in event_handlers:
            self.assertFalse(eh.event.is_set())
            self.assertEqual(eh.counter, 0)

        i = 0
        for topic in self.config["topics-sub"]:
            i+=1
            self.mqttclient.publish(topic, "somerandomtext:"+topic)
            for eh in event_handlers:
                eh.event.wait(0.5)
                self.assertTrue(eh.event.is_set())
                self.assertEqual(eh.counter, i)
                eh.event.clear()

        relay.stop()

        for eh in event_handlers:
            eh.stop()
            self.assertFalse(eh.event.is_set())
            self.assertEqual(eh.counter, i)


if __name__ == '__main__':
    unittest.main()
