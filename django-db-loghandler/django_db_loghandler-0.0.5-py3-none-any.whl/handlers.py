import logging
import traceback


class DBLogHandler(logging.Handler):
    def emit(self, record):
        from db_log.models import LogRecord
        trace = ""
        exc = record.exc_info
        if exc:
            trace = traceback.format_exc()
        record.exc_info = None
        msg = self.format(record)
        log = LogRecord.objects.create(
            logger=record.name, level=record.levelno, trace=trace, msg=msg
        )
        if getattr(record, "username", None):
            log.username = record.username
            log.save()


class DBLogAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        request = kwargs.pop("request", None)
        username = kwargs.pop("username", "")
        self.extra["username"] = username
        self.extra["request"] = request
        kwargs["extra"] = self.extra
        return msg, kwargs


def get_audit_logger(logger, level=logging.INFO):
    h = DBLogHandler()
    logger.addHandler(h)
    logger.setLevel(level)
    return DBLogAdapter(logger, {})
