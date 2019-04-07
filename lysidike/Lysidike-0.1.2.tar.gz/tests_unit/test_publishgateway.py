import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.myconfigtools import read_config
from pelops.logging.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from lysidike.publishgateway import PublishGateway
import time


class TestPublishGateway(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "TestPublishGateway")
        cls.logger.info("start")
        cls.mqtt_client = MyMQTTClient(cls.config["mqtt"], cls.logger)
        cls.mqtt_client.connect()

    @classmethod
    def tearDownClass(cls):
        cls.mqtt_client.disconnect()
        cls.logger.info("end")

    def setUp(self):
        self.logger.info("-----------------------------------------------------------------------")

    def tearDown(self):
        self.logger.info(".......................................................................")

    def test_00create(self):
        pg = PublishGateway(self.config, self.mqtt_client, self.logger, no_gui=True)
        self.assertIsNotNone(pg)
        self.assertEqual(len(pg._services), len(self.config["publish-gateway"]["services"]))
        self.assertEqual(len(pg._tasks), len(self.config["publish-gateway"]["tasks"]))

    def test_00start_stop(self):
        pg = PublishGateway(self.config, self.mqtt_client, self.logger, no_gui=True)
        self.assertIsNotNone(pg)
        pg.start()
        time.sleep(1)
        pg.stop()


if __name__ == '__main__':
    unittest.main()

