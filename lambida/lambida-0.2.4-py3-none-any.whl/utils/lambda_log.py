"""AWS Lambda Logging."""
import logging
import sys
import os
import functools
import traceback


def logging_setup(aws_request_id):
    """Basic config."""
    root = logging.getLogger(os.path.basename(__file__))
    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(levelname)s RequestId: "+aws_request_id+" %(message)s")
        handler.setFormatter(formatter)
        root.addHandler(handler)
        root.setLevel(logging.INFO)
        root.propagate = False
        return root
    return root


def log_event_on_error(handler):
    """Basic Error Logger."""
    @functools.wraps(handler)
    def wrapper(event, context):
        aws_request_id = context.aws_request_id
        invoked_function_arn = context.invoked_function_arn
        log = logging_setup(aws_request_id)
        try:
            log.info('Event from {}: {}'.format(invoked_function_arn, event))
            return handler(event, context)
        except Exception:
            log.error('Exception from {}: {}'
                      .format(invoked_function_arn, 
                              traceback.format_exc()
                                  .replace('\n', "")
                                  .replace('  ', ".")))
    return wrapper
