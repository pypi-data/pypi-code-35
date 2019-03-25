# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the LIMEExplainer for computing explanations on black box models using LIME."""

from lime.lime_tabular import LimeTabularExplainer
import numpy as np

from azureml.explain.model.common.blackbox_explainer import BlackBoxExplainer, blackbox_aggregator, \
    init_blackbox_decorator
from azureml.explain.model.dataset.decorator import tabular_decorator, init_tabular_decorator
from ..scoring.scoring_model import KNNScoringModel
from ..explanation.explanation import _create_local_explanation
from azureml.explain.model._internal.constants import ExplanationParams, ExplainParams, ExplainType

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Starting from version 2.2.1', UserWarning)
    from shap.common import DenseData


@blackbox_aggregator
class LIMEExplainer(BlackBoxExplainer):
    """Defines the LIME Explainer for explaining black box models or functions."""

    @init_tabular_decorator
    @init_blackbox_decorator
    def __init__(self, model, initialization_examples, is_function=False, explain_subset=None,
                 nclusters=10, features=None, classes=None, verbose=False, categorical_features=[],
                 show_progress=True, **kwargs):
        """Initialize the LIME Explainer.

        :param model: The model to explain or function if is_function is True.
        :type model: model that implements predict or predict_proba or function that accepts a 2d ndarray
        :param initialization_examples: A matrix of feature vector examples (# examples x # features) for
            initializing the explainer.
        :type initialization_examples: numpy.array or pandas.DataFrame or iml.datatypes.DenseData or
            scipy.sparse.csr_matrix
        :param is_function: Default set to false, set to True if passing function instead of model.
        :type is_function: bool
        :param explain_subset: List of feature indices. If specified, only selects a subset of the
            features in the evaluation dataset for explanation. The subset can be the top-k features
            from the model summary.
        :type explain_subset: list[int]
        :param nclusters: Number of means to use for approximation. A dataset is summarized with nclusters mean
            samples weighted by the number of data points they each represent. When the number of initialization
            examples is larger than (10 x nclusters), those examples will be summarized with k-means where
            k = nclusters.
        :type nclusters: int
        :param features: A list of feature names.
        :type features: list[str]
        :param classes: Class names as a list of strings. The order of the class names should match
            that of the model output.  Only required if explaining classifier.
        :type classes: list[str]
        :param verbose: If true, uses verbose logging in LIME.
        :type verbose: bool
        :param categorical_features: Categorical feature names for LIME.
        :type categorical_features: list[str]
        :param show_progress: Default to 'True'.  Determines whether to display the explanation status bar
            when using LIMEExplainer.
        :type show_progress: bool
        """
        super(LIMEExplainer, self).__init__(model, is_function=is_function, **kwargs)
        self._logger.debug('Initializing LIMEExplainer')
        self.initialization_examples = initialization_examples
        self.is_classification = False
        self.features = features
        self.classes = classes
        self.nclusters = nclusters
        self.explain_subset = explain_subset
        self.show_progress = show_progress
        function, summary = self._prepare_function_and_summary(self.function, self.original_data_ref,
                                                               self.current_index_list, nclusters=nclusters,
                                                               explain_subset=explain_subset, **kwargs)
        if isinstance(summary, DenseData):
            summary = summary.data
        result = function(summary[0].reshape((1, -1)))
        # If result is 2D array, this is classification scenario, otherwise regression
        if len(result.shape) == 2:
            self.is_classification = True
            mode = ExplainType.CLASSIFICATION
        elif len(result.shape) == 1:
            self.is_classification = False
            mode = ExplainType.REGRESSION
        else:
            raise Exception('Invalid function specified, does not conform to specifications on prediction')
        self.explainer = LimeTabularExplainer(summary, feature_names=features, class_names=classes,
                                              categorical_features=categorical_features, verbose=verbose,
                                              mode=mode, discretize_continuous=False)
        self.explainer.function = function

    @tabular_decorator
    def explain_global(self, evaluation_examples, sampling_policy=None, create_scoring_model=False):
        """Explain the model globally by aggregating local explanations to global.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param sampling_policy: Optional policy for sampling the evaluation examples.  See documentation on
            SamplingPolicy for more information.
        :type sampling_policy: SamplingPolicy
        :param create_scoring_model: Creates a model that can be used for scoring to approximate the feature
            importance values of data faster than LimeTabularExplainer.
        :type create_scoring_model: bool
        :return: A model explanation object containing the global explanation.
        :rtype: GlobalExplanation
        """
        kwargs = {ExplainParams.METHOD: ExplainType.LIME,
                  ExplainParams.SAMPLING_POLICY: sampling_policy,
                  ExplainParams.CREATE_SCORING_MODEL: create_scoring_model}
        return self._explain_global(evaluation_examples, **kwargs)

    @tabular_decorator
    def explain_local(self, evaluation_examples):
        """Explain the function locally by using LIME.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: DatasetWrapper
        :param features: A list of feature names.
        :type features: list[str]
        :param classes: Class names as a list of strings. The order of the class names should match
            that of the model output.  Only required if explaining classifier.
        :type classes: list[str]
        :return: A model explanation object containing the local explanation.
        :rtype: LocalExplanation
        """
        if self.classes is None and self.is_classification:
            raise ValueError('LIME Explainer requires classes to be specified')
        if self.classes is not None and not self.is_classification:
            if self.model is None:
                error = 'Classes is specified but function was predict, not predict_proba.'
            else:
                error = 'Classes is specified but model does not define predict_proba, only predict.'
            raise ValueError(error)

        # Compute subset info prior
        if self.explain_subset:
            evaluation_examples.take_subset(self.explain_subset)

        # sample the evaluation examples
        # note: the sampled data is also used by KNN
        if self.sampling_policy is not None and self.sampling_policy.allow_eval_sampling:
            sampling_method = self.sampling_policy.sampling_method
            max_dim_clustering = self.sampling_policy.max_dim_clustering
            evaluation_examples.sample(max_dim_clustering, sampling_method=sampling_method)
        features = evaluation_examples.get_features(features=self.features)
        if self.explain_subset:
            features = features[self.explain_subset]
        kwargs = {ExplainParams.METHOD: ExplainType.LIME}
        kwargs[ExplainParams.FEATURES] = features
        original_evaluation = evaluation_examples.original_dataset
        evaluation_examples = evaluation_examples.dataset
        if len(evaluation_examples.shape) == 1:
            evaluation_examples = evaluation_examples.reshape(1, -1)

        self._logger.debug('Running LIMEExplainer')
        if self.is_classification:
            kwargs[ExplanationParams.CLASSES] = self.classes
            num_classes = len(self.classes)
            labels = list(range(num_classes))
        else:
            num_classes = 1
            labels = None
        lime_explanations = []

        def tqdm_func(*i, **kwargs):
            return i[0]

        # This is used to get around code style build error F811
        tqdm = tqdm_func
        if self.show_progress:
            try:
                from tqdm import tqdm
            except ImportError:
                self._logger.info('Failed to import tqdm to show progress bar')
        if self.explain_subset:
            self.original_data_ref[0] = original_evaluation
            self.current_index_list.append(0)
            for ex_idx, example in tqdm(enumerate(evaluation_examples)):
                self.current_index_list[0] = ex_idx
                lime_explanations.append(self.explainer.explain_instance(example,
                                                                         self.explainer.function,
                                                                         labels=labels))
            self.current_index_list = [0]
        else:
            for ex_idx, example in tqdm(enumerate(evaluation_examples)):
                lime_explanations.append(self.explainer.explain_instance(example,
                                                                         self.explainer.function,
                                                                         labels=labels))
        if self.is_classification:
            lime_values = [None] * num_classes
            for lime_explanation in lime_explanations:
                for label in labels:
                    map_values = dict(lime_explanation.as_list(label=label))
                    if lime_values[label - 1] is None:
                        lime_values[label - 1] = [[map_values.get(feature, 0.0) for feature in features]]
                    else:
                        lime_values[label - 1].append([map_values.get(feature, 0.0) for feature in features])
        else:
            lime_values = None
            for lime_explanation in lime_explanations:
                map_values = dict(lime_explanation.as_list())
                if lime_values is None:
                    lime_values = [[map_values.get(feature, 0.0) for feature in features]]
                else:
                    lime_values.append([map_values.get(feature, 0.0) for feature in features])
        expected_values = None
        scoring_model = None
        if self._create_scoring_model:
            scoring_model = KNNScoringModel(evaluation_examples, lime_values)
        return _create_local_explanation(local_importance_values=np.array(lime_values),
                                         expected_values=np.array(expected_values),
                                         classification=self.is_classification,
                                         scoring_model=scoring_model,
                                         **kwargs)
