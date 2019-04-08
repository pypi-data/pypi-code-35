# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the Mimic Explainer for computing explanations on black box models or functions.

The mimic explainer trains an explainable model to reproduce the output of the given black box model.
The explainable model is called a surrogate model and the black box model is called a teacher model.
Once trained to reproduce the output of the teacher model, the surrogate model's explanation can
be used to explain the teacher model.
"""

from azureml.explain.model.mimic import mimic_explainer
from ..scoring.scoring_model import TreeScoringModel, LinearScoringModel
from ..explanation.explanation import _create_local_explanation, _create_global_explanation, \
    _aggregate_global_from_local_explanation
from azureml.explain.model.dataset.decorator import tabular_decorator
from azureml.explain.model._internal.constants import ExplainParams
from ..common.aggregate import contrib_aggregator


@contrib_aggregator
class MimicExplainer(mimic_explainer.MimicExplainer):
    """Defines the Mimic Explainer for explaining black box models or functions."""

    def explain_global(self, evaluation_examples=None, create_scoring_model=False):
        """Globally explains the blackbox model using the surrogate model.

        If evaluation_examples are unspecified, retrieves global feature importances from explainable
        surrogate model.  Note this will not include per class feature importances.  If evaluation_examples
        are specified, aggregates local explanations to global from the given evaluation_examples - which
        computes both global and per class feature importances.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which to
            explain the model's output.  If specified, computes feature importances through aggregation.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param create_scoring_model: Creates a TreeExplainer that can be operationalized for
            local model explanations.
        :type create_scoring_model: bool
        :return: A model explanation object. It is guaranteed to be a GlobalExplanation. If evaluation_examples are
            passed in, it will also have the properties of a LocalExplanation. If the model is a classifier (has
            predict_proba), it will have the properties of ClassesMixin, and if evaluation_examples were passed in it
            will also have the properties of PerClassMixin. If create_scoring_model is set to True, it will have the
            properties of HasScoringModel.
        :rtype: DynamicGlobalExplanation
        """
        self._create_scoring_model = create_scoring_model
        kwargs = super(MimicExplainer, self)._get_explain_global_kwargs(evaluation_examples)
        scoring_model = None
        if self._create_scoring_model:
            try:
                scoring_model = TreeScoringModel(self.surrogate_model.model)
            except Exception:
                scoring_model = LinearScoringModel(self.surrogate_model.model,
                                                   self.initialization_examples.dataset)
        kwargs[ExplainParams.SCORING_MODEL] = scoring_model
        if evaluation_examples is not None:
            return _aggregate_global_from_local_explanation(**kwargs)
        return _create_global_explanation(**kwargs)

    @tabular_decorator
    def explain_local(self, evaluation_examples):
        """Locally explains the blackbox model on the provided examples using the surrogate model.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return: A model explanation object. It is guaranteed to be a LocalExplanation. If the model is a classifier,
            it will have the properties of the ClassesMixin.
        :rtype: DynamicLocalExplanation
        """
        kwargs = super(MimicExplainer, self)._get_explain_local_kwargs(evaluation_examples)
        scoring_model = None
        if self._create_scoring_model:
            try:
                scoring_model = TreeScoringModel(self.surrogate_model.model)
            except:
                scoring_model = LinearScoringModel(self.surrogate_model.model,
                                                   self.initialization_examples.dataset)
        kwargs[ExplainParams.SCORING_MODEL] = scoring_model
        return _create_local_explanation(**kwargs)
