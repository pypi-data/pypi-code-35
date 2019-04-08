# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the base API for explainable models."""

from abc import ABCMeta, abstractmethod
import inspect

try:
    from azureml._logging import ChainedIdentity
except ImportError:
    from ...common.chained_identity import ChainedIdentity


def _get_initializer_args(function, surrogate_init_args):
    """Return a list of args to default values for the given function that are in the given argument dict.

    :param function: The function to retrieve the arguments from.
    :type function: Function
    :param surrogate_init_args: The arguments to initialize the surrogate model.
    :type surrogate_init_args: dict
    :return: A mapping from argument name to value for the surrogate model.
    :rtype: dict
    """
    args, _, _, defaults = inspect.getargspec(function)
    all_args = dict(zip(reversed(args), reversed(defaults)))
    return dict([(arg, surrogate_init_args.pop(arg)) for arg in all_args if arg in surrogate_init_args])


class BaseExplainableModel(ChainedIdentity):
    """The base class for models that can be explained."""

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        """Initialize the Explainable Model."""
        super(BaseExplainableModel, self).__init__(**kwargs)
        self._logger.debug('Initializing BaseExplainableModel')

    @abstractmethod
    def fit(self, **kwargs):
        """Abstract method to fit the explainable model."""
        pass

    @abstractmethod
    def predict(self, dataset, **kwargs):
        """Abstract method to predict labels using the explainable model."""
        pass

    @abstractmethod
    def predict_proba(self, dataset, **kwargs):
        """Abstract method to predict probabilities using the explainable model."""
        pass

    @abstractmethod
    def explain_global(self, **kwargs):
        """Abstract method to get the global feature importances from the trained explainable model."""
        pass

    @abstractmethod
    def explain_local(self, evaluation_examples, **kwargs):
        """Abstract method to get the local feature importances from the trained explainable model."""
        pass

    @property
    @abstractmethod
    def model(self):
        """Abstract method to get the underlying model."""
        pass
