"""
Function for basic model validation. Sklearn has very nice implementations
of a much wider variety of model validation metrics.
"""

import numpy as np
from squidward.utils import exactly_1d

np.seterr(over="raise")

def preprocess(func):
    """
    Decorator function used for preprocessing for classification
    validation metrics.
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function for decorator.
        """
        if args:
            prediction, target = args[0], args[1]
            prediction, target = exactly_1d(prediction), exactly_1d(target)
        if kwargs:
            prediction, target = kwargs['prediction'], kwargs['target']
            prediction, target = exactly_1d(prediction), exactly_1d(target)
        if prediction.shape[0] != target.shape[0]:
            raise Exception("Number of predictions does not match number of targets.")
        return func(prediction=prediction, target=target)
    return wrapper

@preprocess
def rmse(prediction, target):
    """
    Calculate of the root mean squared error of univariate regression model.
    """
    return np.sqrt(np.sum((prediction-target) **2)/target.shape[0])

@preprocess
def acc(prediction, target):
    """
    Calculate the accuracy of univariate classification problem.
    """
    return target[target == prediction].shape[0]/target.shape[0]

# TODO: add the following methods
# brier_score
# precision
# recall
# roc_auc
#posterior_checkes
