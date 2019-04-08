# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Default sampler."""
from typing import Any, Dict, Optional

import numpy as np
from sklearn.model_selection import train_test_split

from automl.client.core.common.exceptions import ConfigException
from automl.client.core.common.types import DataInputType, DataSingleColumnInputType
from automl.client.core.common.sampling.abstract_sampler import AbstractSampler


class CountSampler(AbstractSampler):
    """Default sampler."""

    def __init__(self, seed: int, min_examples_per_class: int = 2000, max_rows: int = 10000,
                 is_constraint_driven: bool = True,
                 train_frac: Optional[float] = None) -> None:
        """
        Create default sampler.

        :param seed: Random seed to use to sample.
        :param min_examples_per_class: Minimum examples per class to sample.
        :param max_rows: Maximum rows to output.
        :param is_constraint_driven: Is constraint driven or not.
        :param train_frac: Fraction of data to be considered for training.
        """
        super().__init__()
        self._min_examples_per_class = min_examples_per_class
        self._max_rows = max_rows
        self._seed = seed
        self._is_constraint_driven = is_constraint_driven
        self._train_frac = train_frac

    def sample(self, X: DataInputType, y: DataSingleColumnInputType) -> Any:
        """
        Sample the give input data.

        :param X: Input data.
        :param y: Output label.
        :return: Sampled data.
        """
        # min max logic
        # minimum possible is n_classes * min_examples_per_class
        # max possible
        nrows = np.shape(X)[0]
        class_labels = np.unique(y)
        n_train_by_min_class_examples = len(class_labels) * self._min_examples_per_class
        n_train = min(n_train_by_min_class_examples, self._max_rows)
        constraint_train_frac = n_train / float(nrows)

        if self._is_constraint_driven:
            train_frac = constraint_train_frac
        else:
            if self._train_frac is None:
                raise ConfigException("If constrain train fraction is set to false, train_frac must be specified.")
            train_frac = self._train_frac

        # in case it's a really small dataset!, train_frac could be > 0.8 or even 1.
        train_frac = min(train_frac, 0.8)  # 0.8 guarantees and 80 20 split
        splits = train_test_split(X, y, test_size=1 - train_frac, random_state=self._seed, stratify=y)
        return splits
