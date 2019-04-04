import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from pelops.mylogger import create_logger
import threading
from skeiron.collect import Collect


class TestCollect(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tests_unit/config.yaml"
        cls.main_config = read_config(cls.filename)
        cls.logger = create_logger(cls.main_config["logger"], "TestCollect")
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
            "topics-sub": [
                "/test/relay/3/sub1",
                "/test/relay/3/sub2",
                "/test/relay/3/sub3",
            ],
            "topic-pub": "/test/relay/3/pub",
            "active": True
        }

    def tearDown(self):
        self.mqttclient.unsubscribe_all()

    def test_0init(self):
        self.logger.info("test_0init")
        relay = Collect(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(len(relay._topics_sub), len(self.config["topics-sub"]))
        self.assertEqual(len(relay._topics_pub), 1)
        self.assertListEqual(relay._topics_sub, self.config["topics-sub"])
        self.assertEqual(relay._topics_pub[0], self.config["topic-pub"])
        self.assertEqual(len(self.mqttclient._topic_handler), 0)

    def test_1startstop(self):
        self.logger.info("test_1startstop")
        relay = Collect(self.config, self.mqttclient, self.logger)
        self.assertIsNotNone(relay)
        self.assertEqual(len(self.mqttclient._topic_handler), 0)
        relay.start()
        self.assertEqual(len(self.mqttclient._topic_handler), len(self.config["topics-sub"]))
        self.assertEqual(list(self.mqttclient._topic_handler.keys()), self.config["topics-sub"])
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

        self.mqttclient.subscribe(self.config["topic-pub"], handler)
        relay = Collect(self.config, self.mqttclient, self.logger)
        relay.start()
        event.wait(0.5)
        self.assertFalse(event.is_set())
        self.assertEqual(counter, 0)

        i = 0
        for topic in self.config["topics-sub"]:
            i+=1
            self.mqttclient.publish(topic, "somerandomtext:"+topic)
            event.wait(1)
            self.assertTrue(event.is_set())
            self.assertEqual(counter, i)
            event.clear()

        relay.stop()
        self.assertFalse(event.is_set())
        self.assertEqual(counter, i)


if __name__ == '__main__':
    unittest.main()
