# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Hold sweeper configuration."""
from typing import Any, Dict, List, Optional

import logging
import json
import os

from sklearn.pipeline import Pipeline

from automl.client.core.common._downloader import Downloader
from automl.client.core.common.exceptions import ConfigException


class SweeperConfig:
    """Holder for sweeper configurations."""

    CONFIG_DOWNLOAD_PREFIX = "https://aka.ms/automl-resources/configs/"
    CONFIG_DOWNLOAD_FILE = "config_v1.0.json"

    def __init__(self) -> None:
        """Initialize all attributes."""
        self._type = ''
        self._sampler = ''
        self._estimator = ''
        self._scorer = ''
        self._baseline = None  # type: Optional[Pipeline]
        self._experiment = None  # type: Optional[Pipeline]
        self._column_purposes = []  # type: List[str]
        self._epsilon = 0.0
        self._logger = logging.getLogger(self.__class__.__name__)

    @classmethod
    def from_dict(cls, dct: Dict[str, Any]) -> "SweeperConfig":
        """
        Load from dictionary.

        :param dct: The dictionary containing all the needed params.
        :return: Created sweeper configuration.
        """
        obj = SweeperConfig()
        obj._type = dct.get('type', '')
        obj._sampler = dct.get('sampler', '')
        obj._estimator = dct.get('estimator', '')
        obj._scorer = dct.get('scorer', '')
        obj._baseline = dct.get('baseline')
        obj._experiment = dct.get('experiment')
        obj._column_purposes = dct.get('column_purposes', [])
        obj._epsilon = dct.get('epsilon', 0.0)
        return obj

    @classmethod
    def _validate(cls, config: "SweeperConfig") -> None:
        """Validate the configuration."""
        assert config._type is not None
        assert config._sampler is not None
        assert config._estimator is not None
        assert config._baseline is not None
        assert config._experiment is not None
        assert config._column_purposes is not None
        assert len(config._column_purposes) > 0, "At least one column purpose should be specified"
        assert config._scorer is not None

    def get_config(self) -> Dict[str, Any]:
        """Provide configuration."""
        try:
            file_path = Downloader.download(self.CONFIG_DOWNLOAD_PREFIX, self.CONFIG_DOWNLOAD_FILE, os.getcwd())
            if file_path is None:
                raise ConfigException("Configuration url: {prefix}{file_path} is not accessible!.")

            with open(file_path, 'r') as f:
                cfg = json.load(f)  # type: Dict[str, Any]
                return cfg
        except Exception as e:
            self._logger.debug("Exception when trying to load config from the remote: "
                               "{prefix}{file_path}} with error {e}".format(prefix=self.CONFIG_DOWNLOAD_PREFIX,
                                                                            file_path=self.CONFIG_DOWNLOAD_FILE, e=e))
            return self.default()

    @classmethod
    def default(cls) -> Dict[str, Any]:
        """Return the default back up configuration."""
        cfg = {
            "sweeping_enabled": False,
            "enabled_sweepers": [{
                "type": "binary",
                "sampler": "count",
                "estimator": "logistic_regression",
                "scorer": "accuracy",
                "baseline": {
                    "featurizers": [
                        {
                            "id": "string_cast",
                            "type": "text"
                        },
                        {
                            "id": "bow_transformer",
                            "type": "text"
                        }
                    ]
                },
                "experiment": {
                    "featurizers": [
                        {
                            "id": "string_cast",
                            "type": "text"
                        },
                        {
                            "id": "word_embeddings",
                            "type": "text",
                            "args": [],
                            "kwargs": {
                                "embeddings": "wiki_news_300d_1M_subword"
                            }
                        }],
                    "include_baseline": True
                },
                "column_purposes": [
                    "text"
                ],
                "epsilon": 0.001
            }]
        }

        return cfg
