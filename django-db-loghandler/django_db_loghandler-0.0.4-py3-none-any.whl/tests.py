from django.test import TestCase
from db_log.models import LogRecord
from db_log.handlers import DBLogHandler
from db_log.handlers import get_audit_logger
import logging

# Create your tests here.
class DBLogTestCase(TestCase):
    def setUp(self):
        pass

    def test_logging_add_user(self):
        logger = logging.getLogger("test_user")
        logger = get_audit_logger(logger, level=logging.DEBUG)
        logger.info("TEST INFO", username="user")
        objects = LogRecord.objects.filter(logger="test_user", username="user", level=logging.INFO)
        print(objects)
        self.assertEqual(1, len(objects))

    def test_logging_with_extra(self):
        logger = logging.getLogger("test_with_extra")
        logger.addHandler(DBLogHandler())
        logger.setLevel(logging.INFO)
        logger.info("TEST INFO", extra={"username":"user"})
        objects = LogRecord.objects.filter(logger="test_with_extra", username="user", level=logging.INFO)
        print(objects)
        self.assertEqual(1, len(objects))


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
