# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class to hold feature configuration."""
from typing import Any, Dict, Optional

from automl.client.core.common.exceptions import ConfigException


class FeatureConfig:
    """Class to hold feature configuration."""

    def __init__(self, _id: Optional[str] = None, _type: Optional[str] = None, _args: Any = [],
                 _kwargs: Any = {}) -> None:
        """
        Initialize all attributes.

        :param _id: Id of the featurizer.
        :param _type: Type or column purpose the featurizer works on.
        :param _args: Arguments to be send to the featurizer.
        :param _kwargs: Keyword arguments to be send to the featurizer.
        """
        self._id = _id
        self._type = _type
        self._args = _args
        self._kwargs = _kwargs

    @classmethod
    def from_dict(cls, dct: Dict[str, Any]) -> "FeatureConfig":
        """
        Load from dictionary.

        :param dct: Dictionary holding all the needed params.
        :return: Created object.
        """
        obj = FeatureConfig()
        if 'id' in dct and 'type' in dct:
            obj._id = dct.get('id')
            obj._type = dct.get('type')
            obj._args = dct.get('args', [])
            obj._kwargs = dct.get('kwargs', {})
        else:
            raise ConfigException("Invalid featurizer configuration. Cannot find `id' or `type'.")
        return obj
