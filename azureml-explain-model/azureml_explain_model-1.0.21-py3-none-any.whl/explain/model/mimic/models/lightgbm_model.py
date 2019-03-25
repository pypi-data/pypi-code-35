# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines an explainable lightgbm model."""

from .explainable_model import BaseExplainableModel, _get_initializer_args
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Starting from version 2.2.1', UserWarning)
    import shap
    try:
        from lightgbm import LGBMRegressor, LGBMClassifier
    except ImportError:
        print("Could not import lightgbm, required if using LGBMExplainableModel")

DEFAULT_RANDOM_STATE = 123


class LGBMExplainableModel(BaseExplainableModel):
    """LightGBM (fast, high performance framework based on decision tree) explainable model.

    Please see documentation for more details: https://github.com/Microsoft/LightGBM
    """

    def __init__(self, multiclass=False, random_state=DEFAULT_RANDOM_STATE, **kwargs):
        """Initialize the LightGBM Model.

        Additional arguments to LightGBMClassifier and LightGBMRegressor can be passed through kwargs.

        :param multiclass: Set to true to generate a multiclass model.
        :type multiclass: bool
        :param random_state: Int to seed the model.
        :type random_state: int
        """
        self.multiclass = multiclass
        if self.multiclass:
            initializer = LGBMClassifier
        else:
            initializer = LGBMRegressor
        initializer_args = _get_initializer_args(initializer, kwargs)
        self._lgbm = initializer(random_state=random_state, **initializer_args)
        super(LGBMExplainableModel, self).__init__(**kwargs)
        self._logger.debug('Initializing LGBMExplainableModel')

    try:
        __init__.__doc__ = (__init__.__doc__ +
                            '\nIf multiclass=True, uses the parameters for LGBMClassifier:\n' +
                            LGBMClassifier.__init__.__doc__ +
                            '\nOtherwise, if multiclass=False, uses the parameters for LGBMRegressor:\n' +
                            LGBMRegressor.__init__.__doc__)
    except Exception:
        print("Could not import lightgbm, required if using LGBMExplainableModel")

    def fit(self, dataset, labels, **kwargs):
        """Call lightgbm fit to fit the explainable model.

        :param dataset: The dataset to train the model on.
        :type dataset: numpy or scipy array
        :param labels: The labels to train the model on.
        :type labels: numpy or scipy array
        """
        self._lgbm.fit(dataset, labels, **kwargs)

    try:
        fit.__doc__ = (fit.__doc__ +
                       '\nIf multiclass=True, uses the parameters for LGBMClassifier:\n' +
                       LGBMClassifier.fit.__doc__ +
                       '\nOtherwise, if multiclass=False, uses the parameters for LGBMRegressor:\n' +
                       LGBMRegressor.fit.__doc__)
    except Exception:
        print("Could not import lightgbm, required if using LGBMExplainableModel")

    def predict(self, dataset, **kwargs):
        """Call lightgbm predict to predict labels using the explainable model.

        :param dataset: The dataset to predict on.
        :type dataset: numpy or scipy array
        :return: The predictions of the model.
        :rtype: list
        """
        return self._lgbm.predict(dataset, **kwargs)

    try:
        predict.__doc__ = (predict.__doc__ +
                           '\nIf multiclass=True, uses the parameters for LGBMClassifier:\n' +
                           LGBMClassifier.predict.__doc__ +
                           '\nOtherwise, if multiclass=False, uses the parameters for LGBMRegressor:\n' +
                           LGBMRegressor.predict.__doc__)
    except Exception:
        print("Could not import lightgbm, required if using LGBMExplainableModel")

    def predict_proba(self, dataset, **kwargs):
        """Call lightgbm predict_proba to predict probabilities using the explainable model.

        :param dataset: The dataset to predict probabilities on.
        :type dataset: numpy or scipy array
        :return: The predictions of the model.
        :rtype: list
        """
        if self.multiclass:
            return self._lgbm.predict_proba(dataset, **kwargs)
        else:
            raise Exception("predict_proba not supported for regression or binary classification dataset")

    try:
        predict_proba.__doc__ = (predict_proba.__doc__ +
                                 '\nIf multiclass=True, uses the parameters for LGBMClassifier:\n' +
                                 LGBMClassifier.predict_proba.__doc__ +
                                 '\nOtherwise predict_proba is not supported for ' +
                                 'regression or binary classification.\n')
    except Exception:
        print("Could not import lightgbm, required if using LGBMExplainableModel")

    def explain_global(self, **kwargs):
        """Call lightgbm feature importances to get the global feature importances from the explainable model.

        :return: The global explanation of feature importances.
        :rtype: list
        """
        return self._lgbm.feature_importances_

    def explain_local(self, evaluation_examples, **kwargs):
        """Use TreeExplainer to get the local feature importances from the trained explainable model.

        :param evaluation_examples: The evaluation examples to compute local feature importances for.
        :type evaluation_examples: numpy or scipy array
        :return: The local explanation of feature importances.
        :rtype: Union[list, numpy.ndarray]
        """
        tree_explainer = shap.TreeExplainer(self._lgbm)
        if len(evaluation_examples.shape) == 1:
            evaluation_examples = evaluation_examples.reshape(1, -1)
        return tree_explainer.shap_values(evaluation_examples)

    @property
    def model(self):
        """Retrieve the underlying model.

        :return: The lightgbm model, either classifier or regressor.
        :rtype: Union[LGBMClassifier, LGBMRegressor]
        """
        return self._lgbm
