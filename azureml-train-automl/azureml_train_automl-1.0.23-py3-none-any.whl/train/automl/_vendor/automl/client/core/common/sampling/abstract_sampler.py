# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base class for all samplers."""
from typing import Any, Tuple

from abc import ABC, abstractmethod
import logging

from automl.client.core.common.types import DataInputType, DataSingleColumnInputType


class AbstractSampler(ABC):
    """Base class for all samplers."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize logger for the sub class."""
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def sample(self, X: DataInputType, y: DataSingleColumnInputType) -> \
            Tuple[DataInputType, DataInputType, DataSingleColumnInputType, DataSingleColumnInputType]:
        """All sub classes should implement this."""
        raise NotImplementedError()
