# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for timeseries preprocessing."""
import copy
import inspect
import json
import numpy as np
import pandas as pd
import sys
import warnings

from collections import defaultdict
from sklearn.base import TransformerMixin
from typing import DefaultDict, Dict, List, Union

from automl.client.core.common.constants import TimeSeriesInternal, TimeSeries
from automl.client.core.common.featurization.timeseries.rolling_window import RollingWindow
from automl.client.core.common.featurization.timeseries.lag_lead_operator import LagLeadOperator
from automl.client.core.common.featurization.timeseries.missingdummies_transformer import MissingDummiesTransformer
from automl.client.core.common.featurization.timeseries.numericalize_transformer import NumericalizeTransformer
from automl.client.core.common.memory_utilities import get_data_memory_size
from automl.client.core.common.featurization.timeseries.abstract_timeseries_transformer \
    import AbstractTimeSeriesTransformer
from automl.client.core.common._engineered_feature_names import \
    _FeatureTransformersAsJSONObject, _TransformationFunctionNames, _OperatorNames, \
    FeatureTypeRecognizer, _Transformer, _FeatureTransformers, _FeatureNameJSONTag


# Prevent warnings when using Jupyter
warnings.simplefilter("ignore")
pd.options.mode.chained_assignment = None


class TimeSeriesTransformer(AbstractTimeSeriesTransformer):
    """Class for timeseries preprocess."""

    REMOVE_LAG_LEAD_WARN = "The lag-lead operator was removed due to memory limitation."
    REMOVE_ROLLING_WINDOW_WARN = "The rolling window operator was removed due to memory limitation."

    def __init__(self, logger=None, **kwargs):
        """
        Construct for the class.

        :param logger: The logger to be used in the pipeline.
        :type logger: logging.Logger
        :param kwargs: dictionary contains metadata for TimeSeries.
                       time_column_name: The column containing dates.
                       grain_column_names: The set of columns defining the
                       multiple time series.
                       origin_column_name: latest date from which actual values
                       of all features are assumed to be known with certainty.
                       drop_column_names: The columns which will needs
                       to be removed from the data set.
                       group: the group column name.
        :type kwargs: dict
        """
        self._transforms = {}   # type: Dict[str, TransformerMixin]
        if TimeSeriesInternal.LAGS_TO_CONSTRUCT in kwargs.keys():
            self._get_transformer_params(LagLeadOperator,
                                         TimeSeriesInternal.LAG_LEAD_OPERATOR,
                                         **kwargs)
        if TimeSeriesInternal.WINDOW_SIZE in kwargs.keys() and TimeSeriesInternal.TRANSFORM_DICT in kwargs.keys():
            # We need to disable the horizon detection, because it is very slow on large data sets.
            kwargs['check_max_horizon'] = False
            self._get_transformer_params(RollingWindow,
                                         TimeSeriesInternal.ROLLING_WINDOW_OPERATOR,
                                         **kwargs)
        self._max_horizon = kwargs.get(TimeSeries.MAX_HORIZON, TimeSeriesInternal.MAX_HORIZON_DEFAULT)
        super(TimeSeriesTransformer, self).__init__(logger, **kwargs)

    def _get_transformer_params(self, cls, name, **kwargs):
        """
        Create the transformer if type cls and put it to the self._transforms with label name.

        :param cls: the class of transformer to be constructed.
        :type cls: type
        :param name: Transformer label.
        :type name: str
        :param kwargs: the dictionary of parameters to be parsed.
        :type kwargs: dict

        """
        rw = {}
        valid_args = inspect.getargspec(cls.__init__)[0]
        for k, v in kwargs.items():
            if k in valid_args:
                rw[k] = v

        self._transforms[name] = cls(**rw)

    def _construct_pre_processing_pipeline(self, tsdf, drop_column_names):
        """Return the featurization pipeline."""
        from .forecasting_pipeline import AzureMLForecastPipeline
        from .grain_index_featurizer import GrainIndexFeaturizer
        from .time_series_imputer import TimeSeriesImputer
        from .time_index_featurizer import TimeIndexFeaturizer

        numerical_columns = [x for x in tsdf.select_dtypes(include=[np.number]).columns
                             if x not in drop_column_names]
        if self.target_column_name in numerical_columns:
            numerical_columns.remove(self.target_column_name)
        if self.original_order_column in numerical_columns:
            numerical_columns.remove(self.original_order_column)

        imputation_dict = {col: tsdf[col].median() for col in numerical_columns}
        impute_missing_numerical_values = TimeSeriesImputer(
            input_column=numerical_columns, value=imputation_dict, freq=self.freq)

        time_index_featurizer = TimeIndexFeaturizer(overwrite_columns=True)

        categorical_columns = [x for x in tsdf.select_dtypes(['object', 'category', 'bool']).columns
                               if x not in drop_column_names]
        if self.group_column in categorical_columns:
            categorical_columns.remove(self.group_column)

        # pipeline:
        default_pipeline = AzureMLForecastPipeline([
            ('make_numeric_na_dummies', MissingDummiesTransformer(numerical_columns)),
            ('impute_na_numeric_columns', impute_missing_numerical_values),
            ('make_time_index_featuers', time_index_featurizer)
        ])

        # To get the determined behavior sort the self._transforms.
        transforms_ordered = sorted(self._transforms.keys())
        for transform in transforms_ordered:
            # Add the transformer to the default pipeline
            default_pipeline.add_pipeline_step(transform, self._transforms[transform])

        # Don't apply grain featurizer when there is single timeseries
        if self.dummy_grain_column not in self.grain_column_names:
            grain_index_featurizer = GrainIndexFeaturizer(overwrite_columns=True)
            default_pipeline.add_pipeline_step('make_grain_features', grain_index_featurizer)

        default_pipeline.add_pipeline_step('make_categoricals_numeric', NumericalizeTransformer())
        return default_pipeline

    def _create_feature_transformer_graph(self, graph, feature_from, feature_to, transformer):
        """
        Add the each feature's transform procedure into the graph.

        :param graph: a dictionary contains feature's transformer path
        :type graph: dict
        :param feature_from: feature name before transform
        :type feature_from: str
        :param feature_to: feature name after transform
        :type feature_to: str
        :param transformer: the name of transformer processed the feature
        :type transformer: str
        """
        if feature_to in graph:
            graph[feature_to].append([feature_from, transformer])
        else:
            if feature_from in graph:
                # Deep copy the feature's pre transformers
                graph[feature_to] = copy.deepcopy(graph[feature_from])
                graph[feature_to].append([feature_from, transformer])
            else:
                graph[feature_to] = [[feature_from, transformer]]

    def _generate_json_for_engineered_features(self, tsdf):
        """
        Create the transformer json format for each engineered feature.

        :param graph: a dictionary contains feature's transformer path
        :type graph: dict
        """
        # Create the feature transformer graph from pipeline's steps
        # The dict contains key-> list, list includes a series of transformers
        graph = defaultdict(list)   # type: DefaultDict[str, List[List[Union[str, TransformerMixin]]]]
        for name, transformer in self.pipeline._steps:
            if name == TimeSeriesInternal.MAKE_NUMERIC_NA_DUMMIES:
                for col in transformer.numerical_columns:
                    self._create_feature_transformer_graph(graph, col, col + '_WASNULL', name)
            elif name == TimeSeriesInternal.IMPUTE_NA_NUMERIC_COLUMNS:
                for col in transformer.input_column:
                    self._create_feature_transformer_graph(graph, col, col, name)
            elif name == TimeSeriesInternal.MAKE_TIME_INDEX_FEATURES:
                for col in transformer.preview_time_feature_names(tsdf):
                    self._create_feature_transformer_graph(graph, tsdf.time_colname, col, name)
            elif name == TimeSeriesInternal.MAKE_GRAIN_FEATURES:
                for col in tsdf.grain_colnames:
                    self._create_feature_transformer_graph(graph, col, 'grain_' + col, name)
            elif name == TimeSeriesInternal.MAKE_CATEGORICALS_NUMERIC:
                for col in transformer._categories_by_col.keys():
                    self._create_feature_transformer_graph(graph, col, col, name)
            elif name in [TimeSeriesInternal.LAG_LEAD_OPERATOR, TimeSeriesInternal.ROLLING_WINDOW_OPERATOR]:
                for col in transformer.preview_column_names(tsdf):
                    features = None
                    if name == TimeSeriesInternal.LAG_LEAD_OPERATOR:
                        features = transformer.lags_to_construct.keys()
                    else:
                        features = transformer.transform_dict.values()
                    raw_feature = tsdf.ts_value_colname
                    for feature in features:
                        if col.startswith(feature):
                            raw_feature = feature
                    self._create_feature_transformer_graph(graph, raw_feature, col, name)

        for engineered_feature_name in self.engineered_feature_names:
            col_transformers = graph.get(engineered_feature_name, [])
            transformers = []   # type: List[_Transformer]
            val = ''
            for col, transformer in col_transformers:
                input_feature = col
                # for each engineered feature's transform path, only store the first transformer's
                # input which is raw feature name, other transformers' input are previous transformer
                if len(transformers) > 0:
                    input_feature = len(transformers)
                if transformer == TimeSeriesInternal.MAKE_NUMERIC_NA_DUMMIES:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.ImputationMarker,
                            operator=None,
                            feature_type=FeatureTypeRecognizer.Numeric,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.IMPUTE_NA_NUMERIC_COLUMNS:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.Imputer,
                            operator=_OperatorNames.Mean,
                            feature_type=FeatureTypeRecognizer.Numeric,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.MAKE_TIME_INDEX_FEATURES:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.DateTime,
                            operator=None,
                            feature_type=FeatureTypeRecognizer.DateTime,
                            should_output=True)
                    )
                    val = engineered_feature_name
                elif transformer == TimeSeriesInternal.MAKE_GRAIN_FEATURES:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.GrainMarker,
                            operator=None,
                            feature_type=FeatureTypeRecognizer.Ignore,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.MAKE_CATEGORICALS_NUMERIC:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.LabelEncoder,
                            operator=None,
                            feature_type=FeatureTypeRecognizer.Categorical,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.LAG_LEAD_OPERATOR:
                    # engineered_feature_name of lag operation is %target_col_name%_lags%size%%period"
                    # put the %size%%period% to val
                    val = engineered_feature_name[(len(col) + 4):]
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.Lag,
                            operator=None,
                            feature_type=FeatureTypeRecognizer.Numeric,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.ROLLING_WINDOW_OPERATOR:
                    # engineered_feature_name of rollingwindow operation is %target_col_name%_func%size%%period"
                    # put the %size%%period% to val
                    func_value = engineered_feature_name[len(col) + 1:].split("_", 2)
                    func = func_value[0]
                    val = func_value[1]
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.RollingWindow,
                            operator=func,
                            feature_type=FeatureTypeRecognizer.Numeric,
                            should_output=True)
                    )

            feature_transformers = _FeatureTransformers(transformers)
            # Create the JSON object
            transformation_json = feature_transformers.encode_transformations_from_list()
            transformation_json_data = transformation_json._entire_transformation_json_data
            transformation_json_data[_FeatureNameJSONTag.Value] = val
            self._engineered_feature_name_json_objects[engineered_feature_name] = \
                transformation_json_data

    def _get_json_str_for_engineered_feature_name(self,
                                                  engineered_feature_name):
        """
        Return JSON string for engineered feature name.

        :param engineered_feature_name: Engineered feature name for
            whom JSON string is required
        :return: JSON string for engineered feature name
        """
        # If the JSON object is not valid, then return None
        if engineered_feature_name not in self._engineered_feature_name_json_objects:
            engineered_feature_name_json_obj = []   # type: List[_FeatureTransformersAsJSONObject]
        else:
            engineered_feature_name_json_obj = \
                self._engineered_feature_name_json_objects[engineered_feature_name]

        # Convert JSON into string and return
        return json.dumps(engineered_feature_name_json_obj)

    def get_json_strs_for_engineered_feature_names(self,
                                                   engi_feature_name_list):
        """
        Return JSON string list for engineered feature names.

        :param engi_feature_name_list: Engineered feature names for
            whom JSON strings are required
        :return: JSON string list for engineered feature names
        """
        engineered_feature_names_json_str_list = []

        # Walk engineering feature name list and get the corresponding
        # JSON string
        for engineered_feature_name in engi_feature_name_list:

            json_str = \
                self._get_json_str_for_engineered_feature_name(
                    engineered_feature_name)

            engineered_feature_names_json_str_list.append(json_str)

        # Return the list of JSON strings for engineered feature names
        return engineered_feature_names_json_str_list

    def fit(self, df, y=None):
        """
        Perform the raw data validation and identify the transformations to apply.

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray

        :return: DataTransform object.
        :raises: Value Error for non-dataframe and empty dataframes.

        """
        # Override the parent class fit method to define if there is enough memory
        # for using LagLeadOperator and RollingWindow.
        self._remove_lag_lead_and_rw_maybe(df, y)
        super(TimeSeriesTransformer, self).fit(df, y)

    def _remove_lag_lead_and_rw_maybe(self, df, y):
        """
        Remove the LagLead and or RollingWindow operator from the pipeline if there is not enough memory.

        :param df: DataFrame representing text, numerical or categorical input.
        :type df: pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray

        """
        memory_per_df = get_data_memory_size(df)
        if y is not None:
            memory_per_df += get_data_memory_size(y)
        remove_ll_rw = True
        try:
            total_memory = TimeSeriesTransformer.get_all_ram(self.logger)
            remove_ll_rw = TimeSeriesInternal.MEMORY_FRACTION_FOR_DF < self._max_horizon * memory_per_df / total_memory
        except Exception as e:
            if self.logger is not None:
                self.logger.warning(repr(e))
        if remove_ll_rw:
            self._remove_step_maybe(TimeSeriesInternal.LAG_LEAD_OPERATOR,
                                    TimeSeriesTransformer.REMOVE_LAG_LEAD_WARN)
            self._remove_step_maybe(TimeSeriesInternal.ROLLING_WINDOW_OPERATOR,
                                    TimeSeriesTransformer.REMOVE_ROLLING_WINDOW_WARN)

    def _remove_step_maybe(self, step_name, warning_text):
        """
        Safely remove the pipeline step.

        :param step_name: The name of a pipeline step.
        :type step_name: str
        :param warning_text: The warning text to be shown to user.
                             If None, no warning will be shown.
        :type warning_text: str

        """
        if step_name in self._transforms.keys():
            del self._transforms[step_name]
            if warning_text is not None:
                print(warning_text)

    @staticmethod
    def get_all_ram(errlogger=None):
        """
        Get all RAM in bytes.

        This method is a workaround to the psutil.virtual_memory()[0] method, which can not be
        used because of BatchAI problem.
        :returns: The RAM on the machine.
        :rtype: long

        """
        if sys.platform == 'win32':
            from automl.client.core.common.win32_helper import Win32Helper
            return Win32Helper.get_all_ram()
        else:
            try:  # On Linux we can use sysconf mechanism.
                import os
                return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
            except ValueError:  # No sysconf.
                # fallback to psutil.
                try:
                    import psutil
                    return psutil.virtual_memory()[0]
                except Exception as e:
                    message = ("The psutil module is not installed. Please run \"pip install psutil\".\n"
                               "Unable to determine the amount of memory, Lag Lead Operator and Rolling Window"
                               "will be dropped")
                    if errlogger is not None:
                        errlogger.warning(message)
                    warnings.warn(message)
                    raise e
