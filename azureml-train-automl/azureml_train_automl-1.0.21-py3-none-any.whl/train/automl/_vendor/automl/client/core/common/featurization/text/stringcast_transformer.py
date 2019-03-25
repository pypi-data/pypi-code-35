# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Cast input to string."""
from typing import Optional, Type
import logging

import numpy as np

from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.common.featurization.automltransformer import AutoMLTransformer


class StringCastTransformer(AutoMLTransformer):
    """
    Cast input to string and lower case it if needed.

    The input and output type is same for this transformer.
    """

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """Initialize the Logger object.

        :param logger: Logger to be injected to usage in this class.
        """
        super().__init__()
        self._init_logger(logger)

    def fit(self, x: np.ndarray, y: np.ndarray = None) -> "StringCastTransformer":
        """
        Fit function for string cast transform.

        :param x: Input array.
        :param y: Target values.
        :return: The instance object: self.
        """
        return self

    @function_debug_log_wrapped
    def transform(self, x: np.ndarray) -> np.ndarray:
        """
        Transform data x into array of strings.

        :param x: The data to transform.
        :return: The transformed data as array of strings.
        """
        return x.astype(str)
