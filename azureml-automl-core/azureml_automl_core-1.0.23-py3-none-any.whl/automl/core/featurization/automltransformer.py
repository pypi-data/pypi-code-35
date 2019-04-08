# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base logger class for all the transformers."""
from typing import Optional
import logging

from sklearn.base import BaseEstimator, TransformerMixin


class AutoMLTransformer(BaseEstimator, TransformerMixin):
    """Base logger class for all the transformers."""

    def __init__(self):
        """Init the logger class."""
        self.logger = None  # type: Optional[logging.Logger]

    def __getstate__(self):
        """
        Overriden to remove logger object when pickling.

        :return: this object's state as a dictionary
        """
        state = super(AutoMLTransformer, self).__getstate__()
        newstate = {**state, **self.__dict__}
        newstate['logger'] = None
        return newstate

    def _init_logger(self, logger: Optional[logging.Logger]) -> None:
        """
        Init the logger.

        :param logger: the logger handle.
        :type logger: logging.Logger.
        """
        self.logger = logger

    def _logger_wrapper(self, level: str, message: str) -> None:
        """
        Log a message with a given debug level in a log file.

        :param level: log level (info or debug)
        :param message: log message
        """
        # Check if the logger object is valid. If so, log the message
        # otherwise pass
        if self.logger is not None:
            if level == 'info':
                self.logger.info(message)
            elif level == 'warning':
                self.logger.warning(message)
            elif level == 'debug':
                self.logger.debug(message)
