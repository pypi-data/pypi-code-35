# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Global methods used during an AutoML fit method for pre-processing raw data into meaningful features."""

# Classes have been moved to Featurization, Column purpose detection, Stats computation modules.
# Referring are retained here for backward compatibility.

from automl.client.core.common.featurization import CatImputer, LabelEncoderTransformer, \
    HashOneHotVectorizerTransformer, DateTimeFeaturesTransformer, LaggingTransformer, ImputationMarker, \
    LambdaTransformer, BinTransformer, get_ngram_len, NaiveBayes, StringCastTransformer, max_ngram_len, \
    TimeSeriesTransformer, NumericalizeTransformer, MissingDummiesTransformer, DataTransformer, AutoMLTransformer
from automl.client.core.common.column_purpose_detection import ColumnPurposeDetector
from automl.client.core.common.stats_computation import RawFeatureStats, PreprocessingStatistics \
    as _PreprocessingStatistics
