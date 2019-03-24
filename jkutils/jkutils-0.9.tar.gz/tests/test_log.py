import logging

from . import logger


class A:
    pass


def test_log():
    logger.debug("debug")
    logger.info("info")
    logger.set_default_fields(log_id=logger.log_id, default_id="000000000")
    logger.warning("warning")
    logger.warn("warn")
    logger.error("error")
    logger.remove_default_field("default_id", "test_id")
    logger.critical("critical")
    logger.info("dict", uid=123, phone="12774147414")
    logger.remove_default_all_fields()
    logging.info("logging info")

    logger.info({"qwe": A()})
    logger.info(A())
    assert 1
