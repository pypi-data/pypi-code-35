import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.myconfigtools import read_config
from pelops.logging.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from lysidike.services.servicefactory import ServiceFactory
from lysidike.tasks.taskfactory import TaskFactory


class TestTaskFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "TestTaskFactory")
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
        config = self.config["publish-gateway"]["services"]
        services = ServiceFactory.get_services(config, self.mqtt_client, self.logger)
        self.assertIsNotNone(services)
        config = self.config["publish-gateway"]["tasks"]
        tasks = TaskFactory.get_tasks(config, services, self.mqtt_client, self.logger)
        self.assertIsNotNone(tasks)
        self.assertEqual(len(tasks), len(self.config["publish-gateway"]["tasks"]))


if __name__ == '__main__':
    unittest.main()

