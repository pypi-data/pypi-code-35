# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Holding the preprocess functions."""
import numpy as np
import pandas as pd
import scipy
from sklearn import preprocessing
from . import constants

from azureml.train.automl._preprocessorcontexts import (RawDataContext,
                                                        TransformedDataContext)
from automl.client.core.common.constants import Transformers
from automl.client.core.common.utilities import (_check_if_column_data_type_is_int,
                                                 _get_column_data_type_as_str,
                                                 _log_raw_data_stat)
from automl.client.core.common.preprocess import (DataTransformer,
                                                  LaggingTransformer,
                                                  RawFeatureStats)
from automl.client.core.common.exceptions import (DataException,
                                                  ServiceException)
from automl.client.core.common._cv_splits import (_CVSplits,
                                                  FeaturizedCVSplit,
                                                  FeaturizedTrainValidTestSplit)
from automl.client.core.common.data_transformation import (_get_transformer_x,
                                                           _add_raw_column_names_to_X,
                                                           _y_transform,
                                                           _remove_nan_rows_in_X_y)
from automl.client.core.common.constants import TimeSeries


# TODO: Remove this file once we have remote runs moved over.


def _transform_data(raw_data_context, preprocess=False, logger=None, run_id=None):
    """
    Transform input data from RawDataContext to TransformedDataContext.

    :param raw_data_context: The raw input data.
    :type raw_data_context: RawDataContext
    :param preprocess: pre process data
    :type preprocess: boolean
    :param logger: The logger
    :type logger: logger
    :param run_id: run id
    :type run_id: str
    """
    if logger:
        logger.info("Pre-processing user data")

    if raw_data_context.preprocess is None:
        raw_data_context.preprocess = preprocess

    y_df = raw_data_context.y
    if type(y_df) is not pd.DataFrame:
        y_df = pd.DataFrame(y_df)
    y_raw_stats = RawFeatureStats(y_df.iloc[:, 0])
    _log_raw_data_stat(
        y_raw_stats,
        logger=logger,
        prefix_message="[YCol]"
    )

    x_is_sparse = scipy.sparse.issparse(raw_data_context.X)
    if raw_data_context.preprocess is False or raw_data_context.preprocess == "False" or x_is_sparse:
        # log the data characteristics as it won't going into preprocessing part.
        if x_is_sparse:
            if logger:
                logger.info("The sparse matrix is not supported for getting col charateristics.")
        else:
            x_df = raw_data_context.X
            if not isinstance(x_df, pd.DataFrame):
                x_df = pd.DataFrame(raw_data_context.X)
            for column in x_df.columns:
                raw_stats = RawFeatureStats(x_df[column])
                _log_raw_data_stat(
                    raw_stats,
                    logger=logger,
                    prefix_message="[XColNum:{}]".format(x_df.columns.get_loc(column))
                )

    X, y, sample_weight = _remove_nan_rows_in_X_y(
        raw_data_context.X, raw_data_context.y,
        sample_weight=raw_data_context.sample_weight,
        logger=logger
    )
    X_valid, y_valid, sample_weight_valid = _remove_nan_rows_in_X_y(
        raw_data_context.X_valid, raw_data_context.y_valid,
        sample_weight=raw_data_context.sample_weight_valid,
        logger=logger
    )

    y_transformer, y, y_valid = _y_transform(y, y_valid, raw_data_context.task_type, logger)

    transformed_data_context = TransformedDataContext(X=X,
                                                      y=y,
                                                      X_valid=X_valid,
                                                      y_valid=y_valid,
                                                      sample_weight=sample_weight,
                                                      sample_weight_valid=sample_weight_valid,
                                                      x_raw_column_names=raw_data_context.x_raw_column_names,
                                                      cv_splits_indices=raw_data_context.cv_splits_indices,
                                                      validation_size=raw_data_context.validation_size,
                                                      num_cv_folds=raw_data_context.num_cv_folds,
                                                      logger=logger,
                                                      run_id=run_id,
                                                      enable_cache=raw_data_context.enable_cache,
                                                      data_store=raw_data_context.data_store,
                                                      run_targets=raw_data_context.run_target,
                                                      temp_location=raw_data_context.temp_location,
                                                      task_timeout=raw_data_context.task_timeout)

    x_is_sparse = scipy.sparse.issparse(transformed_data_context.X)
    transformer, lag_transformer, ts_transformer = None, None, None
    if ((raw_data_context.preprocess is False or raw_data_context.preprocess == "False") and
            raw_data_context.timeseries is False) or x_is_sparse:
        if logger:
            logger.info("No preprocessing of data to be done here")
    elif raw_data_context.preprocess is True or raw_data_context.preprocess == "True":
        try:
            transformed_data_context.X = _add_raw_column_names_to_X(raw_data_context.x_raw_column_names,
                                                                    transformed_data_context.X)
            transformer, transformed_data_context.X = _get_transformer_x(transformed_data_context.X,
                                                                         transformed_data_context.y,
                                                                         raw_data_context.task_type,
                                                                         logger)
        except ValueError:
            raise Exception(
                "Cannot preprocess training data. Run after processing manually.")

        if transformed_data_context.X_valid is not None:
            try:
                transformed_data_context.X_valid = _add_raw_column_names_to_X(
                    raw_data_context.x_raw_column_names, transformed_data_context.X_valid)
                transformed_data_context.X_valid = transformer.transform(transformed_data_context.X_valid)
            except ValueError:
                raise Exception(
                    "Cannot preprocess validation data. Run after processing manually.")

        if raw_data_context.lag_length is not None and raw_data_context.lag_length > 0:
            # Get engineered names from Data Transformer if available
            x_raw_column_names = np.asarray(raw_data_context.x_raw_column_names)
            if transformer is not None:
                x_raw_column_names = np.asarray(transformer.get_engineered_feature_names())

            # Create a lagging transformer
            lag_transformer = LaggingTransformer(raw_data_context.lag_length)

            # Fit/Transform using lagging transformer
            transformed_data_context.X = lag_transformer.fit_transform(
                _add_raw_column_names_to_X(x_raw_column_names, transformed_data_context.X),
                transformed_data_context.y)

            if transformed_data_context.X_valid is not None:
                transformed_data_context.X_valid = lag_transformer.transform(
                    _add_raw_column_names_to_X(x_raw_column_names,
                                               transformed_data_context.X_valid))
            if logger:
                logger.info(
                    "lagging transformer is enabled with length {}.".format(
                        raw_data_context.lag_length))

        transformed_data_context._set_transformer(x_transformer=transformer,
                                                  lag_transformer=lag_transformer)
    elif raw_data_context.timeseries is True:
        try:
            transformed_data_context.X = _add_raw_column_names_to_X(raw_data_context.x_raw_column_names,
                                                                    transformed_data_context.X)
            ts_transformer, transformed_data = _get_ts_transformer_x(transformed_data_context.X,
                                                                     transformed_data_context.y,
                                                                     raw_data_context.timeseries_param_dict,
                                                                     logger)
            target_column_name = ts_transformer.target_column_name
            if raw_data_context.timeseries_param_dict is not None and \
               target_column_name in transformed_data.columns:
                    transformed_data_context.y = transformed_data.pop(target_column_name).values
                    transformed_data_context.X = transformed_data.values
        except ValueError:
            raise Exception(
                "Cannot preprocess time series data. Run after cleaning and processing manually.")

        if transformed_data_context.X_valid is not None:
            try:
                transformed_data_context.X_valid = _add_raw_column_names_to_X(
                    raw_data_context.x_raw_column_names,
                    transformed_data_context.X_valid)
                transformed_data_valid = ts_transformer.transform(transformed_data_context.X_valid,
                                                                  transformed_data_context.y_valid)
                transformed_data_context.y_valid = transformed_data_valid.pop(target_column_name).values
                transformed_data_context.X_valid = transformed_data_valid.values
            except ValueError:
                raise Exception(
                    "Cannot preprocess time series validation data. Run after processing manually.")

        transformed_data_context._set_transformer(ts_transformer=ts_transformer)

        if scipy.sparse.issparse(transformed_data_context.X):
            transformed_data_context.X = transformed_data_context.X.todense()
    else:
        if logger:
            logger.info(
                "lagging transformer is enabled with length {}.".format(raw_data_context.lag_length))

    transformed_data_context._set_transformer(transformer, lag_transformer, y_transformer=y_transformer,
                                              ts_transformer=ts_transformer)

    # Create featurized versions of cross validations if user configuration specifies cross validations
    _create_cv_splits_transformed_data(transformed_data_context, raw_data_context.x_raw_column_names,
                                       X, y, sample_weight, raw_data_context.timeseries, logger)

    # Refit transformers
    raw_X = _add_raw_column_names_to_X(raw_data_context.x_raw_column_names, X)
    transformed_data_context._refit_transformers(raw_X, y)

    if isinstance(transformed_data_context.X, pd.DataFrame):
        # X should be a numpy array
        transformed_data_context.X = transformed_data_context.X.values

    if raw_data_context.preprocess:
        transformed_data_context._update_cache()

    return transformed_data_context


def _get_ts_transformer_x(x, y, timeseries_param_dict, logger=None):
    """
    Given data, compute transformations and transformed data.

    :param x: input data
    :param y: labels
    :param timeseries_param_dict: timeseries metadata
    :param logger: logger object for logging data from pre-processing
    :return: transformer, transformed_x
    """
    try:
        from automl.client.core.common.timeseries import TimeSeriesTransformer
    except ImportError as ie:
        raise ie
    tst = TimeSeriesTransformer(logger=logger, **timeseries_param_dict)
    x_transform = tst.fit_transform(x, y)

    return tst, x_transform


def _create_cv_splits_transformed_data(transformed_data_context, x_raw_column_names, X, y,
                                       sample_weight, if_timeseries, logger=None):
    """
    Create featurized data for individual CV splits using the data transformer and lagging trransformer.

    :param x_raw_column_names: List of raw column names
    :param X: Raw training data
    :param y: Raw output variable data
    :param sample_weight: Sample weight
    :param logger: logger for logging
    :param if_timeseries: If time series is set by user
    :return:
    """
    # Check if CV splits need to featruized
    if transformed_data_context.num_cv_folds is not None or \
        (transformed_data_context.validation_size is not None and
         transformed_data_context.validation_size > 0.0) or \
            transformed_data_context.cv_splits_indices is not None:

        if if_timeseries is True:
            raise ValueError("Time series is not supported with cross validation")

        if logger:
            logger.info("Creating cross validations")

        # Add raw column names to raw training data
        raw_X = _add_raw_column_names_to_X(x_raw_column_names, X)
        raw_y = y

        # Create CV splits object
        transformed_data_context.cv_splits = \
            _CVSplits(raw_X, raw_y,
                      frac_valid=transformed_data_context.validation_size,
                      CV=transformed_data_context.num_cv_folds,
                      cv_splits_indices=transformed_data_context.cv_splits_indices)

        if logger:
            logger.info("Found cross validation type: " + str(transformed_data_context.cv_splits._cv_split_type))

        # If data transformer or lagging transformers are valid, then featurize individual CV splits
        if transformed_data_context.transformers[Transformers.X_TRANSFORMER] is not None or \
                transformed_data_context.transformers[Transformers.LAG_TRANSFORMER] is not None:

            data_transformer = transformed_data_context.transformers[Transformers.X_TRANSFORMER]
            lag_transformer = transformed_data_context.transformers[Transformers.LAG_TRANSFORMER]

            if transformed_data_context.cv_splits.get_cv_split_indices() is not None:
                if logger:
                    logger.info("Creating featurized version of CV splits data")

                # Walk all CV split indices and featurize individual train and validation set pair
                transformed_data_context.cv_splits._featurized_cv_splits = []
                cv_split_index = 0
                for X_train, y_train, sample_wt_train, X_test, y_test, sample_wt_test \
                        in transformed_data_context.cv_splits.apply_CV_splits(raw_X, raw_y, sample_weight):

                    if data_transformer is not None:
                        X_train = data_transformer.fit_transform(X_train, y_train)
                        X_test = data_transformer.transform(X_test)

                    if lag_transformer is not None:
                        X_train = lag_transformer.fit_transform(X_train, y_train)
                        X_test = lag_transformer.transform(X_test)

                    # Create the featurized CV split object
                    featurized_cv = FeaturizedCVSplit(
                        X_train, y_train, sample_wt_train,
                        X_test, y_test, sample_wt_test, None, None)

                    if logger:
                        logger.info(str(featurized_cv))

                    # Flush the featurized data on the cache store
                    transformed_data_context._update_cache_with_featurized_data(
                        transformed_data_context._featurized_cv_split_key_initials +
                        str(cv_split_index), featurized_cv)

                    # Clear the in-memory data for the featurized data and record the cache store and key
                    featurized_cv._clear_featurized_data_and_record_cache_store(
                        transformed_data_context.cache_store,
                        transformed_data_context._featurized_cv_split_key_initials + str(cv_split_index))

                    cv_split_index += 1

                    # Append to the list of featurized CV splits
                    transformed_data_context.cv_splits._featurized_cv_splits.append(featurized_cv)

            else:
                if logger:
                    logger.info("Creating featurized data for train and validation data")

                X_train, y_train, sample_weight_train, X_valid, y_valid, \
                    sample_weight_valid, _, _, _ = \
                    transformed_data_context.cv_splits.get_train_validation_test_chunks(raw_X, raw_y, sample_weight)

                if data_transformer is not None:
                    if X_train is not None:
                        X_train = data_transformer.fit_transform(X_train, y_train)
                    if X_valid is not None:
                        X_valid = data_transformer.transform(X_valid)

                if lag_transformer is not None:
                    if X_train is not None:
                        X_train = lag_transformer.fit_transform(X_train, y_train)
                    if X_valid is not None:
                        X_valid = lag_transformer.transform(X_valid)

                # Create the featurized train, valid and test object
                featurized_train_test_valid = FeaturizedTrainValidTestSplit(
                    X_train, y_train, sample_weight_train,
                    X_valid, y_valid, sample_weight_valid,
                    None, None, None, None, None)

                if logger:
                    logger.info(str(featurized_train_test_valid))

                # Flush the featurized data on the cache store
                transformed_data_context._update_cache_with_featurized_data(
                    transformed_data_context._featurized_train_test_valid_key_initials,
                    featurized_train_test_valid)

                # Clear the in-memory data for the featurized data and record the cache store and key
                featurized_train_test_valid._clear_featurized_data_and_record_cache_store(
                    transformed_data_context.cache_store,
                    transformed_data_context._featurized_train_test_valid_key_initials)

                transformed_data_context.cv_splits._featurized_train_test_valid_chunks = featurized_train_test_valid

        if logger:
            logger.info("Completed creating cross-validation folds and featurizing them")
