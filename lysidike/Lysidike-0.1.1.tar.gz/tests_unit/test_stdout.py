import unittest
import os
import io
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.myconfigtools import read_config, validate_config
from pelops.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from lysidike.services.stdoutservice import StdOutService
import datetime
from contextlib import redirect_stdout


class TestSTDOUTService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "TestSTDOUTService")
        cls.logger.info("start")
        cls.mqtt_client = MyMQTTClient(cls.config["mqtt"], cls.logger)
        cls.mqtt_client.connect()
        cls.service_config = cls.config["publish-gateway"]["services"]["stdout"]

    @classmethod
    def tearDownClass(cls):
        cls.mqtt_client.disconnect()
        cls.logger.info("end")

    def setUp(self):
        self.logger.info("-----------------------------------------------------------------------")

    def tearDown(self):
        self.logger.info(".......................................................................")

    def test_0init(self):
        stdout = StdOutService(self.service_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(stdout)

    def test_1startstop(self):
        stdout = StdOutService(self.service_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(stdout)
        stdout.start()
        stdout.stop()

    def test_2testconnection(self):
        stdout = StdOutService(self.service_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(stdout)
        stdout.start()
        self.assertTrue(stdout._test_connection())
        stdout.stop()

    def test_3rendermessages(self):
        stdout = StdOutService(self.service_config, self.mqtt_client, self.logger)
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
        stdout = StdOutService(self.service_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(stdout)
        message = "test message"
        subject = "test subject"

        f = io.StringIO()
        with redirect_stdout(f):
            stdout._send_message(subject, message)
        output = f.getvalue()
        lines = output.split("\n")

        self.assertEqual(lines[0], "------------------------------------------------------------------------------")
        self.assertEqual(lines[1][:1], "@")
        timestamp = datetime.datetime.strptime(lines[1][1:], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.assertEqual(lines[1][1:], timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(lines[2], subject)
        self.assertEqual(lines[3], "")
        self.assertEqual(lines[4], message)
        self.assertEqual(lines[5], "..............................................................................")


if __name__ == '__main__':
    unittest.main()
