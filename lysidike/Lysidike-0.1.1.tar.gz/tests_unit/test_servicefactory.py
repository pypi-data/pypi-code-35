import unittest
import os
import io
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.myconfigtools import read_config, validate_config
from pelops.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from lysidike.services.servicefactory import ServiceFactory
from lysidike.services.emailservice import EmailService
from lysidike.services.stdoutservice import StdOutService


class TestServiceFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "TestServiceFactory")
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

    def test_00create_stdout(self):
        config = self.config["publish-gateway"]["services"]["stdout"]
        service = ServiceFactory.get_service("stdout", config, self.mqtt_client, self.logger)
        self.assertIsNotNone(service)
        self.assertEqual(type(service), StdOutService)

    def test_01create_email(self):
        config = self.config["publish-gateway"]["services"]["email"]
        service = ServiceFactory.get_service("email", config, self.mqtt_client, self.logger)
        self.assertIsNotNone(service)
        self.assertEqual(type(service), EmailService)

    def test_10create_all(self):
        config = self.config["publish-gateway"]["services"]
        services = ServiceFactory.get_services(config, self.mqtt_client, self.logger)
        self.assertIsNotNone(services)
        self.assertEqual(len(services), 2)
        self.assertEqual(type(services["email"]), EmailService)
        self.assertEqual(type(services["stdout"]), StdOutService)


if __name__ == '__main__':
    unittest.main()

