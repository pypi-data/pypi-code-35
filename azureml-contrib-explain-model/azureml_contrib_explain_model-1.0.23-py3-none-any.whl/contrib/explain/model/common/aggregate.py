# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the aggregate explainer decorator for aggregating local explanations to global."""

from ..explanation.explanation import _aggregate_global_from_local_explanation


def contrib_aggregator(cls):
    """Monkey patches the _aggregate_global_from_local_explanation on the contrib explainers.

    :param cls: The class to monkey-patch.
    :type cls: BaseExplainer
    :return: The monkey patched explainer.
    :rtype: BaseExplainer
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
        kwargs = self._get_explain_global_agg_kwargs(evaluation_examples, sampling_policy=sampling_policy,
                                                     create_scoring_model=create_scoring_model, **kwargs)
        # Aggregate local explanation to global
        return _aggregate_global_from_local_explanation(**kwargs)
    cls._explain_global = _explain_global
    return cls
