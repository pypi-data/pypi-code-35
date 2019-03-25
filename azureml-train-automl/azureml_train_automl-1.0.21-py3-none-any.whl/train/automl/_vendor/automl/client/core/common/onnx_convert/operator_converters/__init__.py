# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Init for the operator converters module."""


from automl.client.core.common.onnx_convert.operator_converters._abstract_operator_converter \
    import _AbstractOperatorConverter

from automl.client.core.common.onnx_convert.operator_converters._utilities \
    import OpConverterUtil

from automl.client.core.common.onnx_convert.operator_converters._cat_imputer_converter \
    import CatImputerConverter

from automl.client.core.common.onnx_convert.operator_converters._datetime_feature_trans_converter \
    import DatetimeTransformerConverter

from automl.client.core.common.onnx_convert.operator_converters._dt_feature_concat_converter \
    import _VirtualConcatenator, DataTransformerFeatureConcatenatorConverter

from automl.client.core.common.onnx_convert.operator_converters._hash_onehotvectorizer_converter \
    import HashOneHotVectorizerConverter

from automl.client.core.common.onnx_convert.operator_converters._imputation_marker_converter \
    import ImputationMarkerConverter

from automl.client.core.common.onnx_convert.operator_converters._lagging_transformer_converter \
    import LaggingTransformerConverter

from automl.client.core.common.onnx_convert.operator_converters._string_cast_trans_converter \
    import StringCastTransformerConverter


from automl.client.core.common.onnx_convert.operator_converters._y_trans_le_converter \
    import _YTransformLabelEncoder, YTransformerLabelEncoderConverter

from automl.client.core.common.onnx_convert.operator_converters._pre_fitted_vot_classifier_converter \
    import _VirtualPrefittedVotingClassifier, PrefittedVottingClassifierConverter

from automl.client.core.common.onnx_convert.operator_converters._pre_fitted_vot_regressor_converter \
    import _VirtualPrefittedVotingRegressor, PrefittedVottingRegressorConverter
