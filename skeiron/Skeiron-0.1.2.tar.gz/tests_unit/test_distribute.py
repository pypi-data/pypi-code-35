import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from pelops.mylogger import create_logger
import threading
import time
from skeiron.distribute import Distribute


class TestDistribute(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tests_unit/config.yaml"
        cls.main_config = read_config(cls.filename)
        cls.logger = create_logger(cls.main_config["logger"], "TestDistribute")
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
            "name": "relay4",
            "type": "distribute",
            "topic-sub": "/test/relay/4/sub",
            "topics-pub": [
                "/test/relay/4/pub1",
                "/test/relay/4/pub2",
                "/test/relay/4/pub3"
            ],
            "active": True
        }

    def tearDown(self):
        self.mqttclient.unsubscribe_all()

    def test_0init(self):
        self.logger.info("test_0init")
        relay = Distribute(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(len(relay._topics_sub), 1)
        self.assertEqual(len(relay._topics_pub), len(self.config["topics-pub"]))
        self.assertEqual(relay._topics_sub[0], self.config["topic-sub"])
        self.assertListEqual(relay._topics_pub, self.config["topics-pub"])
        self.assertEqual(len(self.mqttclient._topic_handler), 0)

    def test_1startstop(self):
        self.logger.info("test_1startstop")
        relay = Distribute(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(len(self.mqttclient._topic_handler), 0)
        relay.start()
        self.assertEqual(len(self.mqttclient._topic_handler), 1)
        self.assertListEqual(list(self.mqttclient._topic_handler.keys()), [self.config["topic-sub"]])
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

        relay = Distribute(self.config, self.mqttclient, self.logger)
        relay.start()
        time.sleep(0.5)
        for eh in event_handlers:
            self.assertFalse(eh.event.is_set())
            self.assertEqual(eh.counter, 0)

        self.mqttclient.publish(self.config["topic-sub"], "somerandomtext")
        for eh in event_handlers:
            eh.event.wait(0.5)
            self.assertTrue(eh.event.is_set())
            self.assertEqual(eh.counter, 1)
            eh.event.clear()

        relay.stop()

        for eh in event_handlers:
            eh.stop()
            self.assertFalse(eh.event.is_set())
            self.assertEqual(eh.counter, 1)


if __name__ == '__main__':
    unittest.main()
