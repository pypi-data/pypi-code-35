# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Preprocessing class that can be added in pipeline for input."""
from typing import Any, cast, Dict, List, Optional, Tuple, Type, Union

import json
import logging
import math

import numpy as np
import pandas as pd
from pandas.core.indexes.base import Index
from pandas.core.series import Series
from sklearn_pandas import DataFrameMapper


from automl.client.core.common import constants, utilities
from automl.client.core.common.types import TransformerType

from .._engineered_feature_names import _GenerateEngineeredFeatureNames, \
    FeatureTypeRecognizer, _Transformer, _TransformationFunctionNames, _FeatureTransformers, _OperatorNames
from automl.client.core.common.logging_utilities import function_debug_log_wrapped

from .categorical import CategoricalFeaturizers
from .datetime import DateTimeFeaturesTransformer
from .generic import GenericFeaturizers
from .text import get_ngram_len, TextTransformer, TextFeaturizers
from .automltransformer import AutoMLTransformer

from ..stats_computation import PreprocessingStatistics as _PreprocessingStatistics, \
    RawFeatureStats

from ..column_purpose_detection.columnpurpose_detector import ColumnPurposeDetector
from ..column_purpose_detection.columnpurpose_sweeper import ColumnPurposeSweeper


class DataTransformer(AutoMLTransformer):
    """
    Preprocessing class that can be added in pipeline for input.

    This class does the following:
    1. Numerical inputs treated as it is.
    2. For dates: year, month, day and hour are features
    3. For text, tfidf features
    4. Small number of unique values for a column that is not float become
        categoricals

    :param task: 'classification' or 'regression' depending on what kind of
    ML problem to solve.
    :param is_onnx_compatible: if works in onnx compatible mode.
    """

    def __init__(self,
                 task: Optional[str] = constants.Tasks.CLASSIFICATION,
                 is_onnx_compatible: bool = False,
                 logger: Optional[logging.Logger] = None):
        """
        Initialize for data transformer for pre-processing raw user data.

        :param task: 'classification' or 'regression' depending on what kind
        of ML problem to solve.
        :type task: str or azureml.train.automl.constants.Tasks
        :param is_onnx_compatible: if works in onnx compatible mode.
        :param logger: External logger handler.
        :type logger: logging.Logger
        """
        super().__init__()
        if task not in constants.Tasks.ALL:
            raise ValueError("Unknown task")

        self._task_type = task
        self._is_onnx_compatible = is_onnx_compatible
        self.mapper = None                           # type: Optional[DataFrameMapper]

        # External logger if None, then no logs
        self._init_logger(logger)
        # Maintain a list of raw feature names
        self._raw_feature_names = []                 # type: List[str]
        # Maintain engineered feature name class
        self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
        # Maintain statistics about the pre-processing stage
        self._pre_processing_stats = _PreprocessingStatistics()
        # Text transformer
        self._text_transformer = None                # type: Optional[TextTransformer]

    @function_debug_log_wrapped
    def _learn_transformations(self, df, y=None):
        """
        Learn data transformation to be done on the raw data.

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: numpy.ndarray or pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray or pandas.DataFrame
        """
        utilities.check_input(df)
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        if self._engineered_feature_names_class is None:
            # Create class for engineered feature names
            self._engineered_feature_names_class = \
                _GenerateEngineeredFeatureNames()

        self.mapper = DataFrameMapper(self._get_transforms(df), input_df=True, sparse=True)

    def fit_transform_with_logger(self, X, y=None, logger=None, **fit_params):
        """
        Wrap the fit_transform function for the Data transformer class.

        :param X: Dataframe representing text, numerical or categorical input.
        :type X:numpy.ndarray or pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray or pandas.DataFrame
        :param fit_params: Additional parameters for fit_transform().
        :param logger: External logger handler.
        :type logger: logging.Logger
        :return: Transformed data.
        """
        # Init the logger
        self.logger = logger
        # Call the fit and transform function
        return self.fit_transform(X, y, **fit_params)

    @function_debug_log_wrapped
    def fit(self, df, y=None):
        """
        Perform the raw data validation and identify the transformations to apply.

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: numpy.ndarray or pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray or pandas.DataFrame
        :return: DataTransform object.
        :raises: Value Error for non-dataframe and empty dataframes.
        """
        utilities.check_input(df)
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        if not self.mapper:
            self._logger_wrapper(
                'info', 'Featurizer mapper not found so learn all ' +
                        'the transforms')
            self._learn_transformations(df, y)

        self.mapper.fit(df, y)

        return self

    @function_debug_log_wrapped
    def transform(self, df):
        """
        Transform the input raw data with the transformations idetified in fit stage.

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: numpy.ndarray or pandas.DataFrame
        :return: Numpy array.
        """
        if not self.mapper:
            raise Exception("fit not called")

        utilities.check_input(df)

        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        transformed_data = self.mapper.transform(df)

        if self._engineered_feature_names_class is not None:
            if not self._engineered_feature_names_class.are_engineered_feature_names_available():
                # Generate engineered feature names if they are not already generated
                self._engineered_feature_names_class.parse_raw_feature_names(self.mapper.transformed_names_)

        return transformed_data

    def get_engineered_feature_names(self):
        """
        Get the engineered feature names.

        Return the list of engineered feature names as string after data transformations on the
        raw data have been finished.

        :return: The list of engineered fearure names as strings
        """
        return self._engineered_feature_names_class._engineered_feature_names

    def _get_json_str_for_engineered_feature_name(self,
                                                  engineered_feature_name):
        """
        Return JSON string for engineered feature name.

        :param engineered_feature_name: Engineered feature name for
                                        whom JSON string is required
        :return: JSON string for engineered feature name
        """
        engineered_feature_name_json_obj = self._engineered_feature_names_class. \
            get_json_object_for_engineered_feature_name(engineered_feature_name)

        # If the JSON object is not valid, then return None
        if engineered_feature_name_json_obj is None:
            self._logger_wrapper('info', "Not a valid feature name " + engineered_feature_name)
            return None

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

            if json_str is not None:
                engineered_feature_names_json_str_list.append(json_str)

        # Return the list of JSON strings for engineered feature names
        return engineered_feature_names_json_str_list

    def _get_transforms(self, df: pd.DataFrame) -> List[TransformerType]:
        """
        Identify the transformations for all the columns in the dataframe.

        :param df: Input dataframe.
        :type df: numpy.ndarray or pandas.DataFrame
        :return: Transformations that go into datamapper.
        """
        transforms = []                         # type: List[TransformerType]

        columns = df.columns
        dtypes = df.dtypes

        # Column purpose determination and stats computation
        stats_and_column_purposes = ColumnPurposeDetector.get_raw_stats_and_column_purposes(df)
        self._raw_feature_names, new_column_names = self._generate_new_column_names(columns)

        self._logger_wrapper('info', "Start getting transformers.")

        # Group by column purpose
        # Iterate over the groups

        for column_index, (dtype, column) in enumerate(zip(dtypes, columns)):

            raw_stats, detected_column_purpose = stats_and_column_purposes[column_index]
            new_column_name = new_column_names[column_index]

            current_column_transforms = self._get_transforms_per_column_purpose(column,
                                                                                new_column_name,
                                                                                detected_column_purpose,
                                                                                raw_stats)

            if current_column_transforms:
                transforms.extend(current_column_transforms)
            else:
                # skip if hashes or ignore case
                self._logger_wrapper('info', "Hashes or single value column detected. No transforms needed")

            # TODO Move this to column purpose detection
            utilities._log_raw_data_stat(
                raw_stats, self.logger,
                prefix_message="[XColNum:{}]".format(
                    columns.get_loc(column)
                )
            )

            # TODO Move this to column purpose detection
            self._logger_wrapper(
                'info',
                "Preprocess transformer for col {}, datatype: {}, detected "
                "datatype {}".format(
                    columns.get_loc(column),
                    str(dtype),
                    str(detected_column_purpose)
                )
            )

            # Update pre-processing stats_computation
            self._pre_processing_stats.update_raw_feature_stats(detected_column_purpose)

        transforms.extend(self._sweep_column_purpose(transforms, columns, dtypes,
                                                     stats_and_column_purposes, new_column_names))

        if not transforms:
            # can happen when we get all hashes
            self._logger_wrapper('warning', "No features could be identified or generated")
            raise ValueError("No features could be identified or generated")

        # Log the transformations done for raw data into the logs
        self._logger_wrapper('info', self._get_transformations_str(columns, transforms))

        # Log stats_computation about raw data
        self._logger_wrapper('info',
                             self._pre_processing_stats.get_raw_data_stats())

        self._logger_wrapper('info', "End getting transformers.")
        return transforms

    def _sweep_column_purpose(self, transforms: List[TransformerType],
                              columns: Index, dtypes: Series,
                              stats_and_column_purposes: List[Tuple[RawFeatureStats, str]],
                              new_column_names: List[str]) -> List[TransformerType]:
        """
        Perform column purpose sweeping and return appropriate transforms.

        :param transforms: Current set of transforms.
        :param columns: Current set of columns in the data frame.
        :param dtypes: Current pandas dtypes.
        :param stats_and_column_purposes: Stats and column purposes of various columns.
        :param new_column_names: New columns names for Engineered feature name generation.
        :return:
        """
        column_index = 0
        if not transforms and len(columns) == 1:
            if not np.issubdtype(dtypes[column_index], np.number):
                raw_stats, column_purpose = stats_and_column_purposes[column_index]
                alternate_column_purpose = ColumnPurposeSweeper.safe_convert_column_type(column_purpose)
                if alternate_column_purpose:
                    self._logger_wrapper(
                        "info",
                        "Column index: {column_index}, current column purpose: {detected_column_purpose}, "
                        "Alternate column purpose: {alternate_column_purpose}".format(
                            detected_column_purpose=column_purpose,
                            column_index=column_index,
                            alternate_column_purpose=alternate_column_purpose))
                    return self._get_transforms_per_column_purpose(columns[column_index],
                                                                   new_column_names[column_index],
                                                                   alternate_column_purpose,
                                                                   raw_stats)

        return []

    def _get_transforms_per_column_purpose(
            self,
            column: str,
            new_column_name: str,
            detected_column_purpose: str,
            raw_stats: RawFeatureStats) -> List[TransformerType]:
        """
        Obtain transformations based on column purpose and feature stats.

        :param column: Column name.
        :param new_column_name: New column name for engineered features.
        :param detected_column_purpose: Column purpose detected.
        :param raw_stats: Raw statistics of the column.
        :return: List of transformations to be done on this column.
        """
        if detected_column_purpose == FeatureTypeRecognizer.Numeric:
            tr = []         # type: List[TransformerType]

            tr.extend(self._get_numeric_transforms(column, new_column_name))
            # if there are lot of imputed values, add an imputation marker
            if raw_stats.num_na > 0.01 * raw_stats.total_number_vals:
                tr.extend(self._get_imputation_marker_transforms(column, new_column_name))

            return tr

        if detected_column_purpose == FeatureTypeRecognizer.DateTime:
            return self._get_datetime_transforms(column, new_column_name)
        if detected_column_purpose == FeatureTypeRecognizer.CategoricalHash:
            return self._get_categorical_hash_transforms(column, new_column_name, raw_stats.num_unique_vals)

        if detected_column_purpose == FeatureTypeRecognizer.Categorical:
            return self._get_categorical_transforms(column, new_column_name, raw_stats.num_unique_vals)

        if detected_column_purpose == FeatureTypeRecognizer.Text:
            self._text_transformer = self._text_transformer or \
                TextTransformer(self._task_type, self.logger, self._is_onnx_compatible)
            return self._text_transformer.get_transforms(column, new_column_name, get_ngram_len(raw_stats.lengths),
                                                         self._engineered_feature_names_class)

        return []

    def _get_categorical_hash_transforms(
            self,
            column: str,
            column_name: str,
            num_unique_categories: int) -> List[TransformerType]:
        """
        Create a list of transforms for categorical hash data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :param num_unique_categories: Number of unique categories
        :return: Categorical hash transformations to use in a list.
        """
        # Add the transformations to be done and get the alias name
        # for the hashing one hot encode transform.
        categorical_hash_string_cast_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.StringCast,
            operator=None,
            feature_type=FeatureTypeRecognizer.CategoricalHash,
            should_output=False)
        # This transformation depends on the previous# transformation
        categorical_hash_onehot_encode_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=_TransformationFunctionNames.HashOneHotEncode,
            operator=None, feature_type=None,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = \
            _FeatureTransformers(
                [categorical_hash_string_cast_transformer,
                 categorical_hash_onehot_encode_transformer])

        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = self._engineered_feature_names_class.get_raw_feature_alias_name(json_obj)

        # Add the transformations to be done and get the alias name
        # for the raw column.
        number_of_bits = pow(2, int(math.log(num_unique_categories, 2)) + 1)
        tr = [(column, [TextFeaturizers.string_cast(logger=self.logger),
                        CategoricalFeaturizers.hashonehot_vectorizer(
                            hashing_seed_val=constants.hashing_seed_value,
                            num_cols=int(number_of_bits),
                            logger=self.logger)],
               {'alias': str(alias_column_name)})]

        return tr

    def _get_datetime_transforms(
            self,
            column: str,
            column_name: str) -> List[TransformerType]:
        """
        Create a list of transforms for date time data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :return: Date time transformations to use in a list.
        """
        # Add the transformations to be done and get the alias name
        # for the date time transform.
        datatime_imputer_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.Imputer,
            operator=_OperatorNames.Mode,
            feature_type=FeatureTypeRecognizer.DateTime,
            should_output=True)
        # This transformation depends on the previous transformation
        datatime_string_cast_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=_TransformationFunctionNames.StringCast,
            operator=None, feature_type=None,
            should_output=False)
        # This transformation depends on the previous transformation
        datatime_datetime_transformer = _Transformer(
            parent_feature_list=[2],
            transformation_fnc=_TransformationFunctionNames.DateTime,
            operator=None, feature_type=None,
            should_output=False)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers(
            [datatime_imputer_transformer,
             datatime_string_cast_transformer,
             datatime_datetime_transformer])
        # Create the JSON object
        json_obj = \
            feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

        # Add the transformations to be done and get the alias name
        # for the raw column.
        tr = [(column,
               [CategoricalFeaturizers.cat_imputer(logger=self.logger),
                TextFeaturizers.string_cast(logger=self.logger),
                DateTimeFeaturesTransformer(logger=self.logger)],
               {'alias': str(alias_column_name)})]

        return tr

    def _get_categorical_transforms(
            self,
            column: str,
            column_name: str,
            num_unique_categories: int) -> List[TransformerType]:
        """
        Create a list of transforms for categorical data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :param num_unique_categories: Number of unique categories
        :return: Categorical transformations to use in a list.
        """
        if num_unique_categories <= 2:

            # Add the transformations to be done and get the alias name
            # for the hashing label encode transform.
            cat_two_category_imputer_transformer = _Transformer(
                parent_feature_list=[str(column_name)],
                transformation_fnc=_TransformationFunctionNames.Imputer,
                operator=_OperatorNames.Mode,
                feature_type=FeatureTypeRecognizer.Categorical,
                should_output=True)
            # This transformation depends on the previous transformation
            cat_two_category_string_cast_transformer = _Transformer(
                parent_feature_list=[1],
                transformation_fnc=_TransformationFunctionNames.StringCast,
                operator=None, feature_type=None,
                should_output=False)
            # This transformation depends on the previous transformation
            cat_two_category_label_encode_transformer = _Transformer(
                parent_feature_list=[2],
                transformation_fnc=_TransformationFunctionNames.LabelEncoder,
                operator=None, feature_type=None,
                should_output=True)
            # Create an object to convert transformations into JSON object
            feature_transformers = _FeatureTransformers(
                [cat_two_category_imputer_transformer,
                 cat_two_category_string_cast_transformer,
                 cat_two_category_label_encode_transformer])
            # Create the JSON object
            json_obj = \
                feature_transformers.encode_transformations_from_list()
            # Persist the JSON object for later use and obtain an alias name
            alias_column_name = self._engineered_feature_names_class.get_raw_feature_alias_name(json_obj)

            # Add the transformations to be done and get the alias name
            # for the raw column.
            tr = [(column,
                   [CategoricalFeaturizers.cat_imputer(logger=self.logger),
                    TextFeaturizers.string_cast(logger=self.logger),
                    CategoricalFeaturizers.labelencoder(
                        hashing_seed_val=constants.hashing_seed_value,
                        logger=self.logger)],
                   {'alias': str(alias_column_name)})]

            return tr
        else:
            # Add the transformations to be done and get the alias name
            # for the hashing one hot encode transform.
            cat_multiple_category_string_cast_transformer = _Transformer(
                parent_feature_list=[str(column_name)],
                transformation_fnc=_TransformationFunctionNames.StringCast,
                operator=None, feature_type=FeatureTypeRecognizer.Categorical,
                should_output=False)
            # This transformation depends on the previous transformation
            cat_multiple_category_countvec_transformer = _Transformer(
                parent_feature_list=[1],
                transformation_fnc=_TransformationFunctionNames.CountVec,
                operator=_OperatorNames.CharGram, feature_type=None,
                should_output=True)
            # Create an object to convert transformations into JSON object
            feature_transformers = _FeatureTransformers([
                cat_multiple_category_string_cast_transformer,
                cat_multiple_category_countvec_transformer])
            # Create the JSON object
            json_obj = feature_transformers.encode_transformations_from_list()
            # Persist the JSON object for later use and obtain an alias name
            alias_column_name = self._engineered_feature_names_class.get_raw_feature_alias_name(json_obj)

            # use CountVectorizer for both Hash and CategoricalHash for now
            tr = [(column,
                   [TextFeaturizers.string_cast(logger=self.logger),
                    TextFeaturizers.count_vectorizer(tokenizer=self._wrap_in_lst, binary=True)],
                   {'alias': str(alias_column_name)})]

            return tr

    def _get_numeric_transforms(
            self,
            column: str,
            column_name: str) -> List[TransformerType]:
        """
        Create a list of transforms for numerical data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :return: Numerical transformations to use in a list.
        """
        # Add the transformations to be done and get the alias name
        # for the numerical transform
        numeric_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.Imputer,
            operator=_OperatorNames.Mean,
            feature_type=FeatureTypeRecognizer.Numeric,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers([numeric_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

        # Add the transformations to be done and get the alias name
        # for the imputation marker transform.
        # floats or ints go as they are, we only fix NaN
        tr = [([column], [GenericFeaturizers.imputer()], {'alias': str(alias_column_name)})]

        return cast(List[TransformerType], tr)

    def _get_imputation_marker_transforms(self, column, column_name):
        """
        Create a list of transforms for numerical data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :return: Numerical transformations to use in a list.
        """
        # Add the transformations to be done and get the alias name
        # for the imputation marker transform.
        imputation_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.ImputationMarker,
            operator=None, feature_type=FeatureTypeRecognizer.Numeric,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers([imputation_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

        # Add the transformations to be done and get the alias name
        # for the imputation marker transform.
        tr = [([column],
               [GenericFeaturizers.imputation_marker(logger=self.logger)],
               {'alias': str(alias_column_name)})]

        return tr

    def _wrap_in_lst(self, x):
        """
        Wrap an element in list.

        :param x: Element like string or integer.
        """
        return [x]

    def _get_transformations_str(
            self,
            columns: Index,
            transforms: List[TransformerType]) -> str:
        """
        Get the data transformations recorded for raw columns as strings.

        :param df: Input dataframe.
        :type df:numpy.ndarray or pandas.DataFrame or sparse matrix
        :param transforms: List of applied transformations for various raw
        columns as a string.
        :type transforms: List
        """
        transformation_str = 'Transforms:\n'
        list_of_transforms_as_list = []

        # Walk all columns in the input dataframe
        for column in columns:

            # Get all the indexes of transformations for the current column
            column_matches_transforms = \
                [i for i in range(0, len(transforms))
                 if transforms[i][0] == column]

            # If no matches for column name is found, then look for list having
            # this column name
            if len(column_matches_transforms) == 0:
                column_matches_transforms = \
                    [i for i in range(0, len(transforms))
                     if transforms[i][0] == [column]]

            # Walk all the transformations found for the current column and add
            # to a string
            for transform_index in column_matches_transforms:
                some_str = 'col {}, transformers: {}'.format(
                    columns.get_loc(column),
                    '\t'.join([tf.__class__.__name__ for tf
                               in transforms[transform_index][1]]))
                list_of_transforms_as_list.append(some_str)

        transformation_str += '\n'.join(list_of_transforms_as_list)

        # Return the string representation of all the transformations
        return transformation_str

    @classmethod
    def _generate_new_column_names(cls: Type["DataTransformer"], columns: List[str]) -> Tuple[List[str], List[str]]:
        # In case column names are not specified by the user,
        # append the prefix with a counter to generate a raw feature name
        generated_column_name_prefix = 'C'
        index_raw_columns = 0

        new_column_names = []  # type: List[str]
        raw_feature_names = []  # type: List[str]
        for column in columns:
            # If column name is not an integer, then record it in the raw feature name
            if not isinstance(column, (int, np.integer)):
                raw_feature_names.append(column)
                new_column_name = column
            else:
                # TODO When there is a string column name present, we should be re-using it rather
                # than generating a new one that is completely devoid of the name

                # If the column name is missing, create a new column name for the transformations
                index_raw_columns += 1
                new_column_name = '{prefix}{index}'.format(prefix=generated_column_name_prefix,
                                                           index=index_raw_columns)

            new_column_names.append(new_column_name)
        return raw_feature_names, new_column_names
