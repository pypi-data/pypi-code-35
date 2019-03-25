# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the explanations that are returned from explaining models."""

import numpy as np
import uuid

from azureml.explain.model._internal.common import _sort_values, _order_imp
from azureml.explain.model._internal.constants import Dynamic, ExplainParams, ExplanationParams, History
from azureml.explain.model.explanation.explanation import LocalExplanation, GlobalExplanation, \
    ExpectedValuesMixin, ClassesMixin, PerClassMixin


class TextExplanation(LocalExplanation):
    """Defines the mixin for text explanations."""

    def __init__(self, **kwargs):
        """Create the text explanation."""
        super(TextExplanation, self).__init__(**kwargs)
        order = _order_imp(np.abs(self.local_importance_values))
        self._local_importance_rank = _sort_values(self._features, order)
        self._logger.debug('Initializing TextExplanation')
        if len(order.shape) == 3:
            i = np.arange(order.shape[0])[:, np.newaxis]
            j = np.arange(order.shape[1])[:, np.newaxis]
            self._ordered_local_importance_values = np.array(self.local_importance_values)[i, j, order]
        else:
            self._ordered_local_importance_values = self.local_importance_values

    @property
    def local_importance_rank(self):
        """Feature names sorted by importance.

        This property exists for text explanations only and not for local because currently
        we are doing text explanations for a single document and it is more difficult to
        define order for multiple instances.  Note this is subject to change if we eventually
        add global explanations for text explainers.

        :return: The feature names sorted by importance.
        :rtype: list
        """
        return self._local_importance_rank.tolist()

    @property
    def ordered_local_importance_values(self):
        """Get the feature importance values ordered by importance.

        This property exists for text explanations only and not for local because currently
        we are doing text explanations for a single document and it is more difficult to
        define order for multiple instances.  Note this is subject to change if we eventually
        add global explanations for text explainers.

        :return: For a model with a single output such as regression, this
            returns a list of feature importance values. For models with vector outputs this function
            returns a list of such lists, one for each output. The dimension of this matrix
            is (# examples x # features).
        :rtype: list
        """
        return self._ordered_local_importance_values

    @classmethod
    def _does_quack(cls, explanation):
        """Validate that the explanation object passed in is a valid TextExplanation.

        :param explanation: The explanation to be validated.
        :type explanation: object
        :return: True if valid else False
        :rtype: bool
        """
        if not super()._does_quack(explanation):
            return False
        if not hasattr(explanation, History.LOCAL_IMPORTANCE_RANK) or explanation.local_importance_rank is None:
            return False
        if (not hasattr(explanation, History.ORDERED_LOCAL_IMPORTANCE_VALUES) or
                explanation.ordered_local_importance_values is None):
            return False
        return True


class HasScoringModel(object):
    """Defines an explanation that can be operationalized for real-time scoring."""

    def __init__(self, scoring_model=None, **kwargs):
        """Create the operationalization explanation from scoring model.

        :param scoring_model: The scoring model.
        :type scoring_model: azureml.explain.model.scoring.ScoringModel
        """
        super(HasScoringModel, self).__init__(**kwargs)
        self._scoring_model = scoring_model

    @property
    def scoring_model(self):
        """Return the scoring model.

        :rtype: azureml.explain.model.scoring.ScoringModel
        :return: The scoring model.
        """
        return self._scoring_model

    @staticmethod
    def _does_quack(explanation):
        """Validate that the explanation object passed in is a valid HasScoringModel.

        :param explanation: The explanation to be validated.
        :type explanation: object
        :return: True if valid else False
        :rtype: bool
        """
        if not hasattr(explanation, ExplainParams.SCORING_MODEL) or explanation.scoring_model is None:
            return False
        return True


def _create_local_explanation(expected_values=None, classification=True,
                              scoring_model=None, text_explanation=False, explanation_id=None, **kwargs):
    """Dynamically creates an explanation based on local type and specified data.

    :param expected_values: The expected values of the model.
    :type expected_values: list
    :param classification: Indicates if this is a classification or regression explanation.
    :type classification: bool
    :param scoring_model: The scoring model.
    :type scoring_model: ScoringModel
    :param text_explanation: Indicates if this is a text explanation.
    :type text_explanation: bool
    :param explanation_id: If specified, puts the local explanation under a preexisting explanation object.
        If not, a new unique identifier will be created for the explanation.
    :type explanation_id: str
    :return: A model explanation object. It is guaranteed to be a LocalExplanation. If expected_values is not None, it
        will also have the properties of the ExpectedValuesMixin. If classification is set to True, it will have the
        properties of the ClassesMixin. If text_explanation is set to True, it will have the properties of
        TextExplanation. If scoring_model is not None, it will have the properties of HasScoringModel.
    :rtype: DynamicLocalExplanation
    """
    exp_id = explanation_id or str(uuid.uuid4())
    if text_explanation:
        mixins = [TextExplanation]
    else:
        mixins = [LocalExplanation]
    if expected_values is not None:
        mixins.append(ExpectedValuesMixin)
        kwargs[ExplanationParams.EXPECTED_VALUES] = expected_values
    if scoring_model is not None:
        mixins.append(HasScoringModel)
        kwargs[ExplainParams.SCORING_MODEL] = scoring_model
    if classification:
        mixins.append(ClassesMixin)
    DynamicLocalExplanation = type(Dynamic.LOCAL_EXPLANATION, tuple(mixins), {})
    local_explanation = DynamicLocalExplanation(explanation_id=exp_id, **kwargs)
    return local_explanation


def _create_global_explanation(local_explanation=None, expected_values=None,
                               classification=True, scoring_model=None,
                               text_explanation=False, explanation_id=None, **kwargs):
    """Dynamically creates an explanation based on global type and specified data.

    :param local_explanation: The local explanation information to include with global,
        can be done when the global explanation is a summary of local explanations.
    :type local_explanation: LocalExplanation
        :param expected_values: The expected values of the model.
        :type expected_values: list
    :param classification: Indicates if this is a classification or regression explanation.
    :type classification: bool
    :param scoring_model: The scoring model.
    :type scoring_model: ScoringModel
    :param text_explanation: Indicates if this is a text explanation.
    :type text_explanation: bool
    :param explanation_id: If specified, puts the global explanation under a preexisting explanation object.
        If not, a new unique identifier will be created for the explanation.
    :type explanation_id: str
    :return: A model explanation object. It is guaranteed to be a GlobalExplanation. If local_explanation is not None,
        it will also have the properties of a LocalExplanation. If expected_values is not None, it will have the
        properties of ExpectedValuesMixin. If classification is set to True, it will have the properties of
        ClassesMixin, and if a local explanation was passed in it will also have the properties of PerClassMixin. If
        text_explanation is set to True, it will have the properties of TextExplanation. If create_scoring_model is
        set to True, it will have the properties of HasScoringModel.
    :rtype: DynamicGlobalExplanation
    """
    if local_explanation is not None and LocalExplanation._does_quack(local_explanation):
        exp_id = local_explanation.id
    else:
        exp_id = explanation_id or str(uuid.uuid4())
    mixins = [GlobalExplanation]
    # Special case: for aggregate explanations, we can include both global
    # and local explanations for the user as an optimization, so they
    # don't have to call both explain_global and explain_local and redo the
    # same computation twice
    if local_explanation is not None:
        mixins.append(LocalExplanation)
        kwargs[ExplainParams.LOCAL_IMPORTANCE_VALUES] = np.array(local_explanation.local_importance_values)
    # In the mimic case, we don't aggregate so we can't have per class information
    # but currently in other cases when we aggregate local explanations we get per class
    if classification:
        if local_explanation is not None:
            mixins.append(PerClassMixin)
        else:
            mixins.append(ClassesMixin)
    if expected_values is not None:
        mixins.append(ExpectedValuesMixin)
        kwargs[ExplanationParams.EXPECTED_VALUES] = expected_values
    if scoring_model is not None:
        mixins.append(HasScoringModel)
        kwargs[ExplainParams.SCORING_MODEL] = scoring_model
    DynamicGlobalExplanation = type(Dynamic.GLOBAL_EXPLANATION, tuple(mixins), {})
    global_explanation = DynamicGlobalExplanation(explanation_id=exp_id, **kwargs)
    return global_explanation
