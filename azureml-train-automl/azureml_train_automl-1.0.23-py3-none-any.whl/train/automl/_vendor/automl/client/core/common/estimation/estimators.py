# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""IoC container of all estimators."""
from typing import Any, Dict, Optional
from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression

from automl.client.core.common import utilities


class Estimators:
    """IoC container of all estimators."""

    @classmethod
    def get(cls, sweeper_name: str, *args: Any, **kwargs: Any) -> Optional[BaseEstimator]:
        """
        Create and return the request estimator.

        :param sweeper_name: Name of the requested sweeper.
        """
        if hasattr(cls, sweeper_name):
            member = getattr(cls, sweeper_name)
            if callable(member):  # Make sure the member is a callable.
                return member(*args, **kwargs)

        return None

    @classmethod
    def default(cls) -> BaseEstimator:
        """Create and return default estimator."""
        return cls.logistic_regression()

    @classmethod
    def logistic_regression(cls, *args: Any, **kwargs: Any) -> LogisticRegression:
        """Create a Logistic regression estimator."""
        if not kwargs:
            kwargs = {"C": 1.0}

        return LogisticRegression(*args, **kwargs)
