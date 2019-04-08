# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Factory for sweepers."""
from typing import Any, Optional

from automl.client.core.common.estimation import Estimators
from automl.client.core.common.sampling import Samplers
from automl.client.core.common.scoring import Scorers
from .abstract_sweeper import AbstractSweeper
from .binary_sweeper import BinarySweeper


class Sweepers:
    """Factory for sweepers."""

    @classmethod
    def default(cls, *args: Any, **kwargs: Any) -> AbstractSweeper:
        """
        Create and return the default sweeper.

        :return: Return default sweeper.
        """
        return cls.binary(*args, **kwargs)

    @classmethod
    def get(cls, sweeper_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Create and return the request sweeper.

        :param sweeper_name: Name of the requested sweeper.
        """
        if hasattr(cls, sweeper_name):
            member = getattr(cls, sweeper_name)
            if callable(member):                 # Check that the member is a callable
                return member(*args, **kwargs)

        return None

    @classmethod
    def binary(cls, *args: Any, **kwargs: Any) -> BinarySweeper:
        """Binary sweeper."""
        return BinarySweeper(*args, **kwargs)
