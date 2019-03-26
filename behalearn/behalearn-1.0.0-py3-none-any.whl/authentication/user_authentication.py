from collections import defaultdict

from sklearn.base import TransformerMixin
from sklearn.exceptions import NotFittedError
from collections import Iterable
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


class UserLabelIdentifier(TransformerMixin):
    """
    Identify whether sample belongs (1) to some user or not (0)

    :param user_column: name of column which contains user identifier
    :param label_column: name of column which will store user label in result
    """

    def __init__(self, user_column='id_user', label_column='user_label'):
        self._user_id = None
        self._user_column = user_column
        self._label_column = label_column

    def fit(self, X, y=None, user_id=None, **fit_params):
        if user_id is None:
            raise ValueError(f'{type(self).__name__}.fit function \'user_id\' '
                             f'param must be specified')
        self._user_id = user_id
        return self

    def transform(self, X, **transform_params):
        if self._user_id is None:
            raise NotFittedError(f'This {type(self).__name__}s '
                                 f'instance is not fitted yet')

        X = X.copy()
        X[self._label_column] = 0
        X.loc[X[self._user_column] == self._user_id, self._label_column] = 1
        return X


def user_metrics(y_true, y_pred, metrics, user_id=None):
    """
    Compute metrics from ML model results

    :param y_true: expected results
    :param y_pred: predicted results
    :param metrics: function or list of functions which accepts
                    y_true and y_pred as params and returns single value
    :param user_id: identifier of user, if you want 'id_user' column in result
    :return:
    """

    if not isinstance(metrics, Iterable):
        metrics = [metrics]

    column_names = [metric.__name__ for metric in metrics]
    data = [metric(y_true, y_pred) for metric in metrics]

    if user_id is not None:
        column_names.append('id_user')
        data.append(user_id)

    return {key: value for key, value in zip(column_names, data)}


def authentication_metrics(data, pipeline, metrics, pipeline_params=None,
                           user_column='id_user'):
    """
    Trains estimators for each user and return computed metrics

    :param metrics: array of metrics to compute
    :param data: DataFrame with features for each user
    :param pipeline_params: setting for pipeline
    :param pipeline: array of objects for pipeline execution
    :param user_column: name of column with user ids
    :return: DataFrame with computed metrics for each user
    """
    if pipeline_params is None:
        pipeline_params = {}

    metric_names = [x.__name__ for x in metrics]
    result_metrics = pd.DataFrame(columns=[user_column, *metric_names])

    auth_res = authentication_results(data, pipeline, pipeline_params)

    for id_user, group in auth_res.groupby(user_column):
        metrics_for_user = user_metrics(group['y_test'],
                                        group['y_pred'],
                                        metrics, id_user)
        result_metrics = result_metrics.append(metrics_for_user,
                                               ignore_index=True)

    return result_metrics


def authentication_results(data, pipeline, pipeline_params=None,
                           user_column='id_user', proba=False):
    """
    Trains estimators for each user and return predicted values

    :param data: DataFrame with features for each user
    :param pipeline_params: setting for pipeline
    :param pipeline: array of objects for pipeline execution
    :param user_column: name of column with user ids
    :param proba: include probabilities
                  (estimator in pipeline must support predict_proba)
    :return: DataFrame with computed probabilities for each user
    """
    if pipeline_params is None:
        pipeline_params = {}

    result = defaultdict(list)

    for user_id in data[user_column].unique():
        df_user_label = UserLabelIdentifier() \
            .fit_transform(data, user_id=user_id)

        user_df = df_user_label[df_user_label[user_column] == user_id]
        others_df = df_user_label[df_user_label[user_column] != user_id]

        X_train_user, X_test_user, y_train_user, y_test_user = \
            train_test_split(user_df.drop(columns=[user_column,
                                                   'user_label']),
                             user_df.user_label)

        X_train_others, X_test_others, y_train_others, y_test_others = \
            train_test_split(others_df.drop(columns=[user_column,
                                                     'user_label']),
                             others_df.user_label)

        X_train = pd.concat([X_train_user, X_train_others], ignore_index=True)
        X_test = pd.concat([X_test_user, X_test_others], ignore_index=True)
        y_train = pd.concat([y_train_user, y_train_others], ignore_index=True)
        y_test = pd.concat([y_test_user, y_test_others], ignore_index=True)

        estimator = Pipeline(pipeline).set_params(**pipeline_params) \
            .fit(X_train, y_train)

        y_pred = estimator.predict(X_test)

        result[user_column].extend([user_id] * len(X_test.index))
        result['y_test'].extend(y_test)
        result['y_pred'].extend(y_pred)

        if proba:
            y_pred_proba = estimator.predict_proba(X_test)
            result['proba0'].extend(y_pred_proba[:, 0])
            result['proba1'].extend(y_pred_proba[:, 1])

    return pd.DataFrame(result)
