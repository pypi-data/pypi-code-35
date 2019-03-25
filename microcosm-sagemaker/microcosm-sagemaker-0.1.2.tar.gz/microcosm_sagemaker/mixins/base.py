from abc import ABCMeta, abstractmethod
from json import dump as json_dump
from pathlib import Path
from random import seed


STATIC_SEED = 42


class BundleBase(metaclass=ABCMeta):
    """
    We want to test a variety of model structures while making it easy to swap out models
    in a larger training harness.

    As such, we rely on the basic conventions laid out by sklearn.  Namely, we `fit` when
    we want to train (or otherwise analyze our data) and output model artifacts to a specified
    location on disk.  We `load` when we want to serialize a model from disk.  And finally we
    `transform` when we want to predict on a new datapoint.

    This bundle base also provides some helper logic around random seeds to make sure that
    training loops are reproducable.

    """
    def __init__(self, graph):
        self._environment = graph.config

    def prefit(self, artifact_path):
        """
        Function called by convention before a fit is executed
        """
        self._set_constant_seed()
        self._save_environment(artifact_path)

    @abstractmethod
    def fit(self, artifact_path):
        """
        Train a model.

        :param artifact_path: {str} location to place model artifacts
        :param configuration: {dict} of configuration values
        """
        pass

    @abstractmethod
    def load(self, artifact_path):
        """
        Serialize saved artifacts into runtime.

        :param artifact_path: {str} location of saved model artifacts
        """
        pass

    @abstractmethod
    def predict(self, *args, **kwargs):
        """
        Predict the value of some datapoint, specified by the *args and **kwargs.
        """
        pass

    def _set_constant_seed(self, constant=STATIC_SEED):
        seed(constant)

        try:
            from torch import manual_seed
            manual_seed(constant)
        except ModuleNotFoundError:
            pass

        try:
            from tf.random import set_random_seed
            set_random_seed(constant)
        except ModuleNotFoundError:
            pass

    def _save_environment(self, artifact_dir):
        configuration_path = Path(artifact_dir) / "configuration.json"
        with open(configuration_path, "w") as configuration_file:
            json_dump(self._environment, configuration_file)
