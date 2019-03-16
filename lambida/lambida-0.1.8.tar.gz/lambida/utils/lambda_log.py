"""AWS Lambda Logging."""

import logging
import sys
import os
import functools
import traceback
import boto3

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
        try:
            print(boto3)
            return handler(event, context)
        except Exception:
            log = logging_setup(context.aws_request_id)
            log.error('ERROR EVENT: {}'
                      .format(traceback.format_exc().replace('\n', "").replace('  ', ".")))
            raise
    return wrapper
