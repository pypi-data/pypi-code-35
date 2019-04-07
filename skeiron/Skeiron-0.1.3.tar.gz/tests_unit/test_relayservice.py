import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from pelops.logging.mylogger import create_logger
from skeiron.relayservice import Relayservice
import skeiron.forward
import skeiron.echo
import skeiron.collect
import skeiron.distribute
import skeiron.multiply
import threading
import time


class TestRelayservice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tests_unit/config.yaml"
        cls.main_config = read_config(cls.filename)
        cls.logger = create_logger(cls.main_config["logger"], "TestRelayservice")
        cls.mqttclient = MyMQTTClient(cls.main_config["mqtt"], cls.logger, True)
        cls.mqttclient.connect()

        cls.service_pub_list = [
            "/test/relay/1/pub",
            "/test/relay/2",
            "/test/relay/3/pub",
            "/test/relay/4/pub1",
            "/test/relay/4/pub2",
            "/test/relay/4/pub3",
            "/test/relay/5/pub1",
            "/test/relay/5/pub2",
            "/test/relay/5/pub3"
        ]

        cls.service_sub_list = [
            "/test/relay/1/sub",
            "/test/relay/2",
            "/test/relay/3/sub1",
            "/test/relay/3/sub2",
            "/test/relay/3/sub3",
            "/test/relay/4/sub",
            "/test/relay/5/sub1",
            "/test/relay/5/sub2",
            "/test/relay/5/sub3",
        ]

        cls.logger.info("start ==============================================")

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("end ================================================")
        cls.mqttclient.disconnect()

    def setUp(self):
        self.logger.info("----------------------------------------------------")

    def tearDown(self):
        self.mqttclient.unsubscribe_all()

    def test_0init(self):
        self.logger.info("test_0init")
        rs = Relayservice(self.main_config, self.mqttclient, self.logger, no_gui=True)
        self.assertIsNotNone(rs)
        self.assertEqual(len(rs._relay_list), 5)
        self.assertEqual(len(self.mqttclient._topic_handler), 0)
        expected_types = [skeiron.forward.Forward, skeiron.echo.Echo, skeiron.collect.Collect,
                          skeiron.distribute.Distribute, skeiron.multiply.Multiply]
        created_types = []
        for entry in rs._relay_list:
            created_types.append(type(entry))
        self.assertEqual(expected_types, created_types)

    def test_1startstop(self):
        self.logger.info("test_1startstop")
        rs = Relayservice(self.main_config, self.mqttclient, self.logger, no_gui=True)
        self.assertEqual(len(self.mqttclient._topic_handler), 0)
        rs.start()
        self.assertEqual(len(self.mqttclient._topic_handler), 9)
        rs.stop()
        self.assertEqual(len(self.mqttclient._topic_handler), 0)

    def test_2functionality(self):
        self.logger.info("test_1startstop")
        global total
        total = 0

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
                global total
                total += 1
                self.counter += 1
                self.event.set()

        event_handlers = []
        for topic in self.service_pub_list:
            eh = EventHandler(topic, self.mqttclient)
            eh.start()
            event_handlers.append(eh)

        rs = Relayservice(self.main_config, self.mqttclient, self.logger, no_gui=True)
        rs.start()
        time.sleep(1)

        for topic in self.service_sub_list:
            self.mqttclient.publish(topic, topic)
            time.sleep(0.1)

        time.sleep(1)

        for eh in event_handlers:
            eh.event.wait(1)
            self.assertTrue(eh.event.is_set())

        rs.stop()

        receivedtotal = 0
        for eh in event_handlers:
            eh.stop()
            self.assertTrue(eh.event.is_set())
            self.assertGreater(eh.counter, 0)
            receivedtotal += eh.counter
        self.assertEqual(receivedtotal, total)


if __name__ == '__main__':
    unittest.main()
