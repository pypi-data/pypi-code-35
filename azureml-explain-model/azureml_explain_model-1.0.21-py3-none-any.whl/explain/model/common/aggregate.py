# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the aggregate explainer decorator for aggregating local explanations to global."""

from functools import wraps
from ..explanation.explanation import _aggregate_global_from_local_explanation
from azureml.explain.model._internal.constants import ExplainParams


def init_aggregator_decorator(init_func):
    """Decorate a constructor to wrap initialization examples in a DatasetWrapper.

    Provided for convenience for tabular data explainers.

    :param init_func: Initialization constructor where the second argument is a dataset.
    :type init_func: Initialization constructor.
    """
    @wraps(init_func)
    def init_wrapper(self, model, *args, **kwargs):
        self.sampling_policy = None
        return init_func(self, model, *args, **kwargs)
    return init_wrapper


def global_aggregator(cls):
    """Decorate explainer to allow aggregating local explanations to global.

    Adds a protected method _explain_global that creates local explanations
    and then aggregates them to a global explanation by averaging.
    """
    def _explain_global(self, evaluation_examples, sampling_policy=None, create_scoring_model=False, **kwargs):
        """Explains the model by aggregating local explanations to global.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param sampling_policy: Optional policy for sampling the evaluation examples.  See documentation on
            SamplingPolicy for more information.
        :type sampling_policy: SamplingPolicy
        :param create_scoring_model: Creates a model that can be used for scoring to approximate the feature
            importance values of data faster than LimeTabularExplainer.
        :type create_scoring_model: bool
        :return: A model explanation object containing the local and global explanation.
        :rtype: BaseExplanation
        """
        self.sampling_policy = sampling_policy
        self._create_scoring_model = create_scoring_model
        if self.classes is not None:
            kwargs[ExplainParams.CLASSES] = self.classes
        # first get local explanation
        local_explanation = self.explain_local(evaluation_examples)
        # Aggregate local explanation to global
        return _aggregate_global_from_local_explanation(local_explanation=local_explanation, **kwargs)
    setattr(cls, '_explain_global', _explain_global)
    return cls
