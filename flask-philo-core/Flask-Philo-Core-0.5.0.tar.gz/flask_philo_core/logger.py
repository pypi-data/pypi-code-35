from flask.logging import default_handler


import json_log_formatter
import logging


def init_logging(app):
    """
    Configure flask logger to support structured logging
    http://flask.pocoo.org/docs/dev/logging/
    https://github.com/marselester/json-log-formatter
    """

    # Removing default logger
    app.logger.removeHandler(default_handler)
    formatter = json_log_formatter.JSONFormatter()
    hndlr = logging.StreamHandler()
    hndlr.setFormatter(formatter)
    app.logger.addHandler(hndlr)
    log_level = app.config['LOG_LEVEL']
    app.logger.setLevel(log_level)
