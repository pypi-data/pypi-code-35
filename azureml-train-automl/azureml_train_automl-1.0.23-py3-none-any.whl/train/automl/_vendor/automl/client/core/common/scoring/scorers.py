# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Factory for scorers."""
from typing import Any, Dict, Optional
from .abstract_scorer import AbstractScorer
from .accuracy_scorer import AccuracyScorer


class Scorers:
    """Factory for scorers."""

    @classmethod
    def get(cls, sweeper_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Create and return the request sweeper.

        :param sweeper_name: Name of the requested sweeper.
        """
        if hasattr(cls, sweeper_name):
            member = getattr(cls, sweeper_name)
            if callable(member):
                return member(*args, **kwargs)
        return None

    @classmethod
    def default(cls, *args: Any, **kwargs: Any) -> AbstractScorer:
        """Create and return the default scorer."""
        return cls.accuracy(*args, **kwargs)

    @classmethod
    def accuracy(cls, *args: Any, **kwargs: Any) -> AccuracyScorer:
        """Create and return the accuracy scorer."""
        return AccuracyScorer(*args, **kwargs)
