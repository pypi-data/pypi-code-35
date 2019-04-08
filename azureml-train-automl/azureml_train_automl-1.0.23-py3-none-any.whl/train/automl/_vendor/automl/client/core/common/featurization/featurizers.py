# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Featurizer factory."""
from typing import Any, Optional

from automl.client.core.common import utilities
from automl.client.core.common.featurization import AutoMLTransformer
from .text import TextFeaturizers
from automl.client.core.common.configuration.feature_config import FeatureConfig


class Featurizers:
    """Featurizer factory."""

    @classmethod
    def get(cls, config: FeatureConfig) -> Any:
        """Get featurizer given an id and type. Initialize with params defined in the config.

        :param config: Configuration containing required feature details.
        :return: Featurizer instance or None.
        """
        assert config is not None and config._id is not None
        # TODO Handle other featurizers
        if config._type == "text" and hasattr(TextFeaturizers, config._id):
            factory_method = getattr(TextFeaturizers, config._id)
            if callable(factory_method):
                return factory_method(*config._args, **config._kwargs)

        return None
