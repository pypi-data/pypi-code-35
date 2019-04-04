import unittest
import os
import io
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.myconfigtools import read_config, validate_config
from pelops.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from lysidike.services.servicefactory import ServiceFactory
from lysidike.tasks.task import Task
from lysidike.services.stdoutservice import StdOutService
from lysidike.services.emailservice import EmailService
from contextlib import redirect_stdout
import time


class TestTask(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "TestTask")
        cls.logger.info("start")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.mqtt_client = MyMQTTClient(self.config["mqtt"], self.logger)
        self.mqtt_client.connect()

        self.services = ServiceFactory.get_services(self.config["publish-gateway"]["services"], self.mqtt_client,
                                                    self.logger)
        self.assertIsNotNone(self.services)
        self.logger.info("-----------------------------------------------------------------------")

    def tearDown(self):
        self.logger.info(".......................................................................")
        self.mqtt_client.disconnect()
        self.logger.info("end")

    def test_00init_stdout(self):
        config = {
            "name": "immediate",
            "service": "stdout",
            "subject": "immediate information",
            "every-nth-message": 1,
            "every-nth-second": 2,
            "topics-sub": ["/test/d", "/test/a"]
        }
        task = Task(config, self.services, self.mqtt_client, self.logger)
        self.assertIsNotNone(task)
        self.assertEqual(type(task._service), StdOutService)
        self.assertEqual("immediate", task.name)
        self.assertEqual("immediate information", task._subject)
        self.assertEqual(len(task._topics_sub), 2)
        self.assertEqual(task._topics_sub[0], "/test/d")
        self.assertEqual(task._topics_sub[1], "/test/a")
        self.assertEqual(task._every_nth_message, 1)
        self.assertEqual(task._every_nth_second, 2)

    def test_01init_email(self):
        config = {
            "name": "immediate",
            "service": "email",
            "subject": "immediate information",
            "every-nth-message": 1,
            "every-nth-second": 2,
            "topics-sub": ["/test/d", "/test/a"]
        }
        task = Task(config, self.services, self.mqtt_client, self.logger)
        self.assertIsNotNone(task)
        self.assertEqual(type(task._service), EmailService)
        self.assertEqual("immediate", task.name)
        self.assertEqual("immediate information", task._subject)
        self.assertEqual(len(task._topics_sub), 2)
        self.assertEqual(task._topics_sub[0], "/test/d")
        self.assertEqual(task._topics_sub[1], "/test/a")
        self.assertEqual(task._every_nth_message, 1)
        self.assertEqual(task._every_nth_second, 2)

    def test_02start_stop(self):
        config = {
            "name": "immediate",
            "service": "stdout",
            "subject": "immediate information",
            "every-nth-message": 1,
            "every-nth-second": 2,
            "topics-sub": ["/test/d", "/test/a"]
        }
        task = Task(config, self.services, self.mqtt_client, self.logger)
        self.assertIsNotNone(task)
        task.start()
        self.logger.info("... waiting 0.1 seconds ...")
        time.sleep(0.1)
        task.stop()

    def test_03immediate(self):
        config = {
            "name": "immediate",
            "service": "stdout",
            "subject": "immediate information",
            "every-nth-message": 1,
            "every-nth-second": 0,
            "topics-sub": ["/test/d"]
        }
        task = Task(config, self.services, self.mqtt_client, self.logger)
        self.assertIsNotNone(task)
        self.assertEqual(task._every_nth_message, 1)
        self.assertEqual(task._every_nth_second, 0)
        self.assertFalse(task._use_every_second)
        self.assertTrue(task._use_every_message)

        task.start()
        time.sleep(0.1)
        f = io.StringIO()
        with redirect_stdout(f):
            self.mqtt_client.publish("/test/d", "a")
            time.sleep(0.1)
        output = f.getvalue()
        self.assertEqual(output.count("\n"), 11)
        f = io.StringIO()
        with redirect_stdout(f):
            self.mqtt_client.publish("/test/d", "a")
            self.mqtt_client.publish("/test/d", "a")
            time.sleep(0.1)
        output = f.getvalue()
        self.assertEqual(output.count("\n"), 22)
        task.stop()

    def test_04collect(self):
        config = {
            "name": "immediate",
            "service": "stdout",
            "subject": "immediate information",
            "every-nth-message": 2,
            "every-nth-second": 0,
            "topics-sub": ["/test/d"]
        }
        task = Task(config, self.services, self.mqtt_client, self.logger)
        self.assertIsNotNone(task)
        self.assertEqual(task._every_nth_message, 2)
        self.assertEqual(task._every_nth_second, 0)
        self.assertFalse(task._use_every_second)
        self.assertTrue(task._use_every_message)

        task.start()
        time.sleep(0.1)
        f = io.StringIO()
        with redirect_stdout(f):
            self.mqtt_client.publish("/test/d", "a")
            self.mqtt_client.publish("/test/d", "a")
            time.sleep(0.1)
        output = f.getvalue()
        self.assertEqual(output.count("\n"), 12)
        f = io.StringIO()
        with redirect_stdout(f):
            self.mqtt_client.publish("/test/d", "a")
            self.mqtt_client.publish("/test/d", "a")
            self.mqtt_client.publish("/test/d", "a")
            self.mqtt_client.publish("/test/d", "a")
            time.sleep(0.1)
        output = f.getvalue()
        self.assertEqual(output.count("\n"), 24)
        task.stop()

    def test_05time(self):
        config = {
            "name": "immediate",
            "service": "stdout",
            "subject": "immediate information",
            "every-nth-message": 0,
            "every-nth-second": 1,
            "topics-sub": ["/test/d"]
        }
        task = Task(config, self.services, self.mqtt_client, self.logger)
        self.assertIsNotNone(task)
        self.assertEqual(task._every_nth_message, 0)
        self.assertEqual(task._every_nth_second, 1)
        self.assertTrue(task._use_every_second)
        self.assertFalse(task._use_every_message)

        task.start()
        time.sleep(0.1)
        f = io.StringIO()
        with redirect_stdout(f):
            self.mqtt_client.publish("/test/d", "a")
            time.sleep(1)
        output = f.getvalue()
        self.assertEqual(output.count("\n"), 11)
        f = io.StringIO()
        with redirect_stdout(f):
            self.mqtt_client.publish("/test/d", "a")
            time.sleep(0.1)
            self.mqtt_client.publish("/test/d", "a")
            time.sleep(1)
        output = f.getvalue()
        self.assertEqual(output.count("\n"), 12)
        f = io.StringIO()
        with redirect_stdout(f):
            time.sleep(2)
        output = f.getvalue()
        self.assertEqual(output.count("\n"), 20)
        task.stop()


if __name__ == '__main__':
    unittest.main()

