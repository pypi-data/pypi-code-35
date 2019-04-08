# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines an explainable linear model."""
import numpy as np
import scipy as sp

from azureml.explain.model.mimic.models.explainable_model import BaseExplainableModel, _get_initializer_args
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDClassifier, SGDRegressor

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Starting from version 2.2.1', UserWarning)
    import shap

DEFAULT_RANDOM_STATE = 123


def _compute_local_shap_values(model, evaluation_examples, multiclass, mean, covariance, seed):
    """Compute the local shap values.

    :param model: The linear model to compute the shap values for.
    :type model: linear model that implements predict or predict_proba
    :param evaluation_examples: The evaluation examples.
    :type evaluation_examples: numpy or scipy array
    :param multiclass: True if this is a multiclass model.
    :type multiclass: bool
    :param mean: The mean of the dataset by columns.
    :type mean: numpy.array
    :param covariance: The covariance matrix of the dataset.
    :type covariance: numpy.array
    :param seed: Random number seed.
    :type seed: int
    """
    feature_dependence = 'correlation'
    if sp.sparse.issparse(evaluation_examples):
        feature_dependence = 'interventional'
    np.random.seed(seed)
    if multiclass:
        coefs = model.coef_
        intercepts = model.intercept_
        shap_values = []
        if isinstance(intercepts, list):
            coef_intercept_list = zip(coefs, intercepts)
        else:
            coef_intercept_list = [(coef, intercepts) for coef in coefs]
        for class_coef, intercept in coef_intercept_list:
            linear_explainer = shap.LinearExplainer((class_coef, intercept), (mean, covariance),
                                                    feature_dependence=feature_dependence)
            shap_values.append(linear_explainer.shap_values(evaluation_examples))
        return shap_values
    else:
        linear_explainer = shap.LinearExplainer(model, (mean, covariance), feature_dependence=feature_dependence)
        return linear_explainer.shap_values(evaluation_examples)


class LinearExplainableModel(BaseExplainableModel):
    """Linear explainable model."""

    def __init__(self, multiclass=False, random_state=DEFAULT_RANDOM_STATE, **kwargs):
        """Initialize the LinearExplainableModel.

        :param multiclass: Set to true to generate a multiclass model.
        :type multiclass: bool
        :param random_state: Int to seed the model.
        :type random_state: int
        """
        self.multiclass = multiclass
        self.random_state = random_state
        if self.multiclass:
            initializer = LogisticRegression
            kwargs['random_state'] = random_state
        else:
            initializer = LinearRegression
        initializer_args = _get_initializer_args(initializer, kwargs)
        self._linear = initializer(**initializer_args)
        super(LinearExplainableModel, self).__init__(**kwargs)
        self._logger.debug('Initializing LinearExplainableModel')

    __init__.__doc__ = (__init__.__doc__ +
                        '\nIf multiclass=True, uses the parameters for LogisticRegression:\n' +
                        LogisticRegression.__doc__ +
                        '\nOtherwise, if multiclass=False, uses the parameters for LinearRegression:\n' +
                        LinearRegression.__doc__)

    def fit(self, dataset, labels, **kwargs):
        """Call linear fit to fit the explainable model.

        Store the mean and covariance of the background data for local explanation.

        :param dataset: The dataset to train the model on.
        :type dataset: numpy or scipy array
        :param labels: The labels to train the model on.
        :type labels: numpy or scipy array
        """
        self._linear.fit(dataset, labels, **kwargs)
        self.mean = dataset.mean(0)
        if not sp.sparse.issparse(dataset):
            self.covariance = np.cov(dataset, rowvar=False)
        else:
            # Not needed for sparse case
            self.covariance = None

    fit.__doc__ = (fit.__doc__ +
                   '\nIf multiclass=True, uses the parameters for LogisticRegression:\n' +
                   LogisticRegression.fit.__doc__ +
                   '\nOtherwise, if multiclass=False, uses the parameters for LinearRegression:\n' +
                   LinearRegression.fit.__doc__)

    def predict(self, dataset, **kwargs):
        """Call linear predict to predict labels using the explainable model.

        :param dataset: The dataset to predict on.
        :type dataset: numpy or scipy array
        :return: The predictions of the model.
        :rtype: list
        """
        return self._linear.predict(dataset)

    predict.__doc__ = (predict.__doc__ +
                       '\nIf multiclass=True, uses the parameters for LogisticRegression:\n' +
                       LogisticRegression.predict.__doc__ +
                       '\nOtherwise, if multiclass=False, uses the parameters for LinearRegression:\n' +
                       LinearRegression.predict.__doc__)

    def predict_proba(self, dataset, **kwargs):
        """Call linear predict_proba to predict probabilities using the explainable model.

        :param dataset: The dataset to predict probabilities on.
        :type dataset: numpy or scipy array
        :return: The predictions of the model.
        :rtype: list
        """
        if self.multiclass:
            return self._linear.predict_proba(dataset)
        else:
            raise Exception('predict_proba not supported for regression or binary classification dataset')

    predict_proba.__doc__ = (predict_proba.__doc__ +
                             '\nIf multiclass=True, uses the parameters for LogisticRegression:\n' +
                             LogisticRegression.predict_proba.__doc__ +
                             '\nOtherwise predict_proba is not supported for regression or binary classification.\n')

    def explain_global(self, **kwargs):
        """Call coef_ to get the global feature importances from the linear surrogate model.

        :return: The global explanation of feature importances.
        :rtype: list
        """
        coef = self._linear.coef_
        if (len(coef.shape) == 2):
            return np.mean(coef, axis=0)
        return coef

    def explain_local(self, evaluation_examples, **kwargs):
        """Use LinearExplainer to get the local feature importances from the trained explainable model.

        :param evaluation_examples: The evaluation examples to compute local feature importances for.
        :type evaluation_examples: numpy or scipy array
        :return: The local explanation of feature importances.
        :rtype: Union[list, numpy.ndarray]
        """
        return _compute_local_shap_values(self._linear, evaluation_examples, self.multiclass,
                                          self.mean, self.covariance, self.random_state)

    @property
    def model(self):
        """Retrieve the underlying model.

        :return: The linear model, either classifier or regressor.
        :rtype: Union[LogisticRegression, LinearRegression]
        """
        return self._linear


class SGDExplainableModel(BaseExplainableModel):
    """Stochastic Gradient Descent explainable model."""

    def __init__(self, multiclass=False, random_state=DEFAULT_RANDOM_STATE, **kwargs):
        """Initialize the SGDExplainableModel.

        :param multiclass: Set to true to generate a multiclass model.
        :type multiclass: bool
        :param random_state: Int to seed the model.
        :type random_state: int
        """
        self.multiclass = multiclass
        self.random_state = random_state
        if self.multiclass:
            initializer = SGDClassifier
        else:
            initializer = SGDRegressor
        initializer_args = _get_initializer_args(initializer, kwargs)
        self._sgd = initializer(random_state=random_state, **initializer_args)
        super(SGDExplainableModel, self).__init__(**kwargs)
        self._logger.debug('Initializing SGDExplainableModel')

    __init__.__doc__ = (__init__.__doc__ +
                        '\nIf multiclass=True, uses the parameters for SGDClassifier:\n' +
                        SGDClassifier.__doc__ +
                        '\nOtherwise, if multiclass=False, uses the parameters for SGDRegressor:\n' +
                        SGDRegressor.__doc__)

    def fit(self, dataset, labels, **kwargs):
        """Call linear fit to fit the explainable model.

        Store the mean and covariance of the background data for local explanation.

        :param dataset: The dataset to train the model on.
        :type dataset: numpy or scipy array
        :param labels: The labels to train the model on.
        :type labels: numpy or scipy array
        """
        self._sgd.fit(dataset, labels, **kwargs)
        self.mean = dataset.mean(0)
        if not sp.sparse.issparse(dataset):
            self.covariance = np.cov(dataset, rowvar=False)
        else:
            # Not needed for sparse case
            self.covariance = None

    fit.__doc__ = (fit.__doc__ +
                   '\nIf multiclass=True, uses the parameters for SGDClassifier:\n' +
                   SGDClassifier.fit.__doc__ +
                   '\nOtherwise, if multiclass=False, uses the parameters for SGDRegressor:\n' +
                   SGDRegressor.fit.__doc__)

    def predict(self, dataset, **kwargs):
        """Call SGD predict to predict labels using the explainable model.

        :param dataset: The dataset to predict on.
        :type dataset: numpy or scipy array
        :return: The predictions of the model.
        :rtype: list
        """
        return self._sgd.predict(dataset)

    predict.__doc__ = (predict.__doc__ +
                       '\nIf multiclass=True, uses the parameters for SGDClassifier:\n' +
                       SGDClassifier.predict.__doc__ +
                       '\nOtherwise, if multiclass=False, uses the parameters for SGDRegressor:\n' +
                       SGDRegressor.predict.__doc__)

    def predict_proba(self, dataset, **kwargs):
        """Call SGD predict_proba to predict probabilities using the explainable model.

        :param dataset: The dataset to predict probabilities on.
        :type dataset: numpy or scipy array
        :return: The predictions of the model.
        :rtype: list
        """
        if self.multiclass:
            return self._sgd.predict_proba(dataset)
        else:
            raise Exception('predict_proba not supported for regression or binary classification dataset')

    predict_proba.__doc__ = (predict_proba.__doc__ +
                             '\nIf multiclass=True, uses the parameters for SGDClassifier:\n' +
                             SGDClassifier.predict_proba.__doc__ +
                             '\nOtherwise predict_proba is not supported for regression or binary classification.\n')

    def explain_global(self, **kwargs):
        """Call coef_ to get the global feature importances from the SGD surrogate model.

        :return: The global explanation of feature importances.
        :rtype: list
        """
        coef = self._sgd.coef_
        if (len(coef.shape) == 2):
            return np.mean(coef, axis=0)
        return coef

    def explain_local(self, evaluation_examples, **kwargs):
        """Use LinearExplainer to get the local feature importances from the trained explainable model.

        :param evaluation_examples: The evaluation examples to compute local feature importances for.
        :type evaluation_examples: numpy or scipy array
        :return: The local explanation of feature importances.
        :rtype: Union[list, numpy.ndarray]
        """
        return _compute_local_shap_values(self._sgd, evaluation_examples, self.multiclass,
                                          self.mean, self.covariance, self.random_state)

    @property
    def model(self):
        """Retrieve the underlying model.

        :return: The SGD model, either classifier or regressor.
        :rtype: Union[SGDClassifier, SGDRegressor]
        """
        return self._sgd
