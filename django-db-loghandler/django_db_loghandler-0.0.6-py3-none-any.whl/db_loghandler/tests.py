from django.test import TestCase
from db_loghandler.models import LogRecord
from db_loghandler import DBLogHandler
from db_loghandler import get_audit_logger
import logging

# Create your tests here.
class DBLogTestCase(TestCase):
    def setUp(self):
        pass

    def test_logging_add_user(self):
        logger = logging.getLogger("test_user")
        logger = get_audit_logger(logger, level=logging.DEBUG)
        logger.info("TEST INFO", username="user")
        record = LogRecord.objects.get(logger="test_user", level=logging.INFO)
        self.assertEqual("user", record.username)

    def test_logging_with_extra(self):
        logger = logging.getLogger("test_with_extra")
        logger.addHandler(DBLogHandler())
        logger.setLevel(logging.INFO)
        logger.info("TEST INFO", extra={"username": "user"})
        record = LogRecord.objects.get(logger="test_with_extra", level=logging.INFO)
        self.assertEqual("user", record.username)

    def test_logging_level(self):
        """Testing writing logging"""
        logger = logging.getLogger("test_level")
        logger.addHandler(DBLogHandler())
        logger.setLevel(logging.DEBUG)
        logger.debug("TEST DEBUG")
        record = LogRecord.objects.get(logger="test_level", level=logging.DEBUG)
        self.assertEqual(record.msg, "TEST DEBUG")
        logger.error("TEST ERROR")
        record = LogRecord.objects.get(logger="test_level", level=logging.ERROR)
        self.assertEqual(record.msg, "TEST ERROR")

    def test_logging_trace(self):
        logger = logging.getLogger("test_trace")
        logger.addHandler(DBLogHandler())
        logger.setLevel(logging.INFO)
        try:
            raise AttributeError
        except AttributeError:
            logger.info("TEST TRACE", exc_info=True)
        record = LogRecord.objects.get(logger="test_trace", level=logging.INFO)
        self.assertEqual(record.msg, "TEST TRACE")
        self.assertTrue(record.trace.startswith("Traceback"))

    def test_logging_with_format(self):
        logger = logging.getLogger("test_format")
        logger.addHandler(DBLogHandler())
        logger.setLevel(logging.INFO)
        logger.info("TEST %s", "FORMAT")
        record = LogRecord.objects.get(logger="test_format", level=logging.INFO)
        self.assertEqual(record.msg, "TEST FORMAT")
