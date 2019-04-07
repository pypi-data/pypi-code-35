import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.myconfigtools import read_config
from pelops.logging.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from lysidike.services.emailservice import EmailService
import datetime


class TestEMAILService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "TestEMAILService")
        cls.logger.info("start")
        cls.mqtt_client = MyMQTTClient(cls.config["mqtt"], cls.logger)
        cls.mqtt_client.connect()
        cls.service_config = cls.config["publish-gateway"]["services"]["email"]
        # assume that username is a valid email address for the account - i dont want to place a real
        # email address into the config yaml file ...
        cls.service_config["from"] = cls.service_config["username"]
        cls.service_config["to"] = cls.service_config["username"]

    @classmethod
    def tearDownClass(cls):
        cls.mqtt_client.disconnect()
        cls.logger.info("end")

    def setUp(self):
        self.logger.info("-----------------------------------------------------------------------")

    def tearDown(self):
        self.logger.info(".......................................................................")

    def test_0init(self):
        stdout = EmailService(self.service_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(stdout)

    def test_1startstop(self):
        stdout = EmailService(self.service_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(stdout)
        stdout.start()
        stdout.stop()

    def test_2testconnection(self):
        stdout = EmailService(self.service_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(stdout)
        stdout.start()
        self.assertTrue(stdout._test_connection())
        stdout.stop()

    def test_3rendermessages(self):
        stdout = EmailService(self.service_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(stdout)
        messages = []
        start = datetime.date(year=2018, month=1, day=1)
        for i in range(2):
            timestamp = start + datetime.timedelta(days=i)
            topic = "\\test\\test"
            m = i
            messages.append((timestamp, topic, m))
        message = stdout._render_message(messages)

        expected_message = "received 2 messages since last update.\n\n"
        expected_message += "Messages:\n"
        expected_message += "  2018-01-01T00:00:00.000000Z; \\test\\test; '0'\n"
        expected_message += "  2018-01-02T00:00:00.000000Z; \\test\\test; '1'\n"
        expected_message += "EOF\n"

        self.assertEqual(message, expected_message)

    def test_4sendmessage(self):
        email = EmailService(self.service_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(email)
        message = "test message @{}.".format(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        subject = "test subject"
        email._send_message(subject, message)

    def test_5sendmessage_multiple_tos(self):
        self.service_config["to"] = [self.service_config["to"], self.service_config["to"]]
        email = EmailService(self.service_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(email)
        message = "test message @{}.".format(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        subject = "test subject"
        email._send_message(subject, message)

if __name__ == '__main__':
    unittest.main()
