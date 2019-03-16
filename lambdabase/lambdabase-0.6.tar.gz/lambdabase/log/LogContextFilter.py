import logging
from lambdabase.log.LogMessage import LogMessage


class ContextFilter(logging.Filter):
    """
    Logging context filer. Extract the pertinant details
    the incoming record and format as key value pairs
    """
    def filter(self, record):
        """
        Extract the log message object and reformat into
        something the log handler is expecting
        """
        if isinstance(record.msg, LogMessage):
            if isinstance(record.msg.params, dict):
                record.__dict__.update(record.msg.params)
                record.msg = record.msg.message
        return True
