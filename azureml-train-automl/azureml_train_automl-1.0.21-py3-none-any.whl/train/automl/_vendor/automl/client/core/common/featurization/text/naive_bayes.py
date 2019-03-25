# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Wrapper for sklearn Multinomial Naive Bayes."""
from typing import Optional
import logging

from sklearn.naive_bayes import MultinomialNB

from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.common.featurization.automltransformer import AutoMLTransformer
from automl.client.core.common.model_wrappers import _AbstractModelWrapper


class NaiveBayes(AutoMLTransformer, _AbstractModelWrapper):
    """Wrapper for sklearn Multinomial Naive Bayes."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Construct the Naive Bayes transformer.

        :param logger: Logger to be injected to usage in this class.
        """
        super().__init__()
        self.model = MultinomialNB()
        self._init_logger(logger)

    def fit(self, x, y=None):
        """
        Naive Bayes transform to learn conditional probablities for textual data.

        :param x: The data to transform.
        :type x: numpy.ndarray or pandas.series
        :param y: Target values.
        :type y: numpy.ndarray
        :return: The instance object: self.
        """
        self.model.fit(x, y)
        return self

    def get_model(self):
        """
        Return inner NB model.

        :return: NaiveBayes model.
        """
        return self.model

    @function_debug_log_wrapped
    def transform(self, x):
        """
        Transform data x.

        :param x: The data to transform.
        :type x: numpy.ndarray or pandas.series
        :return: Prediction probability values from Naive Bayes model.
        """
        return self.model.predict_proba(x)
