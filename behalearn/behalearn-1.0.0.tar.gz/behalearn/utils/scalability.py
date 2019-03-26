import numpy as np
from pandas import Series, DataFrame
from collections import Iterable

from behalearn.authentication.user_authentication import authentication_metrics


def scalability(data, steps, metrics, fold_size, cv,
                steps_params=None, user_column='id_user'):
    """
    Compute classification results w.r.t. the number of users in the model

    :param data: DataFrame with features for each user
    :param steps: array of objects for pipeline execution
    :param metrics: metrics to compute
    :param fold_size: count (or list of counts) of users in each fold
    :param cv: number of repeats for each fold_size
    :param steps_params: parameters for steps
    :param user_column: name of column with user identifier
    :return: DataFrame with computed metrics for number of users in the model
    """

    if steps_params is None:
        steps_params = {}

    if not isinstance(fold_size, Iterable):
        fold_size = [fold_size]

    users = data[user_column].unique()

    scores = DataFrame()
    for size in fold_size:
        if len(users) < size:
            raise ValueError('More users in test than in dataset')

        size_scores = Series()
        for _ in range(cv):
            users_test_ids = np.random.choice(users, size,
                                              replace=False)
            users_test = data[data[user_column].isin(users_test_ids)]

            size_metrics = authentication_metrics(users_test,
                                                  steps, metrics,
                                                  pipeline_params=steps_params)
            size_scores = size_scores.add(size_metrics.mean(), fill_value=0)

        size_scores = size_scores.drop(user_column) \
                                 .divide(cv)
        size_scores['fold_size'] = size
        size_scores['cv'] = cv
        scores = scores.append(size_scores, ignore_index=True)

    scores['fold_size'] = scores['fold_size'].astype('int')
    scores['cv'] = scores['cv'].astype('int')
    return scores
