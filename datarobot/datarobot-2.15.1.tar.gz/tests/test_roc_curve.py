import json

import pytest
import responses
from datarobot.errors import ClientError

from datarobot.utils import from_api

from datarobot import Model

from datarobot.models.roc_curve import RocCurve


@pytest.fixture
def roc_curve_data():
    return {
        'rocPoints': [
            {'matthewsCorrelationCoefficient': 0.0, 'liftNegative': 1.6580310880829014,
             'falseNegativeScore': 635, 'threshold': 1.0, 'positivePredictiveValue': 0.0,
             'falsePositiveScore': 0, 'truePositiveRate': 0.0, 'falsePositiveRate': 0.0,
             'trueNegativeScore': 965, 'fractionPredictedAsPositive': 0.396875,
             'truePositiveScore': 0, 'liftPositive': 0.0, 'trueNegativeRate': 1.0,
             'fractionPredictedAsNegative': 0.603125, 'negativePredictiveValue': 0.603125,
             'f1Score': 0.0, 'accuracy': 0.603125},
            {'matthewsCorrelationCoefficient': 0.2654644740095313,
             'liftNegative': 0.7027302746382453, 'falseNegativeScore': 108,
             'threshold': 0.3192387913454449,
             'positivePredictiveValue': 0.4866112650046168, 'falsePositiveScore': 556,
             'truePositiveRate': 0.8299212598425196,
             'falsePositiveRate': 0.5761658031088083, 'trueNegativeScore': 409,
             'fractionPredictedAsPositive': 0.396875, 'truePositiveScore': 527,
             'liftPositive': 2.0911401822803644, 'trueNegativeRate': 0.42383419689119173,
             'fractionPredictedAsNegative': 0.603125,
             'negativePredictiveValue': 0.7911025145067698, 'f1Score': 0.6135040745052387,
             'accuracy': 0.585},
            {'matthewsCorrelationCoefficient': 0.26949035662808024,
             'liftNegative': 0.6872667722623426,
             'falseNegativeScore': 101, 'threshold': 0.3159331104401148,
             'positivePredictiveValue': 0.4858962693357598, 'falsePositiveScore': 565,
             'truePositiveRate': 0.8409448818897638,
             'falsePositiveRate': 0.5854922279792746,
             'trueNegativeScore': 400, 'fractionPredictedAsPositive': 0.396875,
             'truePositiveScore': 534, 'liftPositive': 2.118916237832476,
             'trueNegativeRate': 0.41450777202072536,
             'fractionPredictedAsNegative': 0.603125,
             'negativePredictiveValue': 0.7984031936127745, 'f1Score': 0.615916955017301,
             'accuracy': 0.58375},
            {'matthewsCorrelationCoefficient': 0.26539544824735506,
             'liftNegative': 0.6666487690944723, 'falseNegativeScore': 97,
             'threshold': 0.31168680078090694,
             'positivePredictiveValue': 0.48251121076233183, 'falsePositiveScore': 577,
             'truePositiveRate': 0.8472440944881889,
             'falsePositiveRate': 0.5979274611398964, 'trueNegativeScore': 388,
             'fractionPredictedAsPositive': 0.396875, 'truePositiveScore': 538,
             'liftPositive': 2.134788269576539, 'trueNegativeRate': 0.40207253886010363,
             'fractionPredictedAsNegative': 0.603125, 'negativePredictiveValue': 0.8,
             'f1Score': 0.6148571428571429, 'accuracy': 0.57875},
            {'matthewsCorrelationCoefficient': 0.0, 'liftNegative': 0.0,
             'falseNegativeScore': 0, 'threshold': 0.040378634122377174,
             'positivePredictiveValue': 0.396875, 'falsePositiveScore': 965,
             'truePositiveRate': 1.0, 'falsePositiveRate': 1.0, 'trueNegativeScore': 0,
             'fractionPredictedAsPositive': 0.396875, 'truePositiveScore': 635,
             'liftPositive': 2.5196850393700787, 'trueNegativeRate': 0.0,
             'fractionPredictedAsNegative': 0.603125, 'negativePredictiveValue': 0.0,
             'f1Score': 0.5682326621923938, 'accuracy': 0.396875}],
        'negativeClassPredictions': [0.3089065297896129, 0.2192436274291769, 0.2741881940220157,
                                     0.45359061567051495, 0.33373525837036394, 0.2022848622576362,
                                     0.37657493994960095, 0.3446332343090306],
        'positiveClassPredictions': [0.31066443626142176, 0.3335789706639738, 0.41265286028960974,
                                     0.5962910547142551, 0.6729667252356237, 0.4358587761356483,
                                     0.7175456320809883, 0.6880904423192126]
    }


@pytest.fixture
def roc_curve_validation_data(model_id, roc_curve_data):
    return {
        'source': 'validation',
        'sourceModelId': model_id,
        'rocPoints': roc_curve_data['rocPoints'],
        'negativeClassPredictions': roc_curve_data['negativeClassPredictions'],
        'positiveClassPredictions': roc_curve_data['positiveClassPredictions']
    }


@pytest.fixture
def roc_curve_parent_model_validation_data(parent_model_id, roc_curve_data):
    return {
        'source': 'validation',
        'sourceModelId': parent_model_id,
        'rocPoints': roc_curve_data['rocPoints'],
        'negativeClassPredictions': roc_curve_data['negativeClassPredictions'],
        'positiveClassPredictions': roc_curve_data['positiveClassPredictions']
    }


@pytest.fixture
def roc_curve_parent_model_holdout_data(parent_model_id, roc_curve_data):
    return {
        'source': 'holdout',
        'sourceModelId': parent_model_id,
        'rocPoints': roc_curve_data['rocPoints'],
        'negativeClassPredictions': roc_curve_data['negativeClassPredictions'],
        'positiveClassPredictions': roc_curve_data['positiveClassPredictions']
    }


def test_instantiation(roc_curve_validation_data):
    roc = RocCurve.from_server_data(roc_curve_validation_data)

    assert roc.source == roc_curve_validation_data['source']
    assert roc.negative_class_predictions == roc_curve_validation_data['negativeClassPredictions']
    assert roc.positive_class_predictions == roc_curve_validation_data['positiveClassPredictions']
    assert roc.roc_points == from_api(roc_curve_validation_data['rocPoints'])
    assert roc.source_model_id == roc_curve_validation_data['sourceModelId']


def test_future_proof(roc_curve_validation_data):
    data_with_future_keys = dict(roc_curve_validation_data, new_key='some future roc data')
    data_with_future_keys['rocPoints'][0]['new_key'] = 'some future bin data'
    RocCurve.from_server_data(data_with_future_keys)


@pytest.fixture
def roc_curve_validation_data_url(project_id, model_id):
    return 'https://host_name.com/projects/{}/models/{}/rocCurve/validation/'.format(
        project_id,
        model_id
    )


@pytest.fixture
def roc_curve_parent_model_validation_data_url(project_id, parent_model_id):
    return 'https://host_name.com/projects/{}/models/{}/rocCurve/validation/'.format(
        project_id,
        parent_model_id
    )


@pytest.fixture
def roc_curve_list_url(project_id, model_id):
    return 'https://host_name.com/projects/{}/models/{}/rocCurve/'.format(
        project_id,
        model_id
    )


@pytest.fixture
def roc_curve_parent_list_url(project_id, parent_model_id):
    return 'https://host_name.com/projects/{}/models/{}/rocCurve/'.format(
        project_id,
        parent_model_id
    )


@pytest.fixture
def frozen_model_url(project_id, model_id):
    return 'https://host_name.com/projects/{}/frozenModels/{}/'.format(
        project_id,
        model_id
    )


@responses.activate
@pytest.mark.usefixtures('client')
def test_get_validation_roc_curve(roc_curve_validation_data,
                                  roc_curve_validation_data_url,
                                  project_id, model_id):
    responses.add(
        responses.GET,
        roc_curve_validation_data_url,
        status=200,
        content_type='application/json',
        body=json.dumps(roc_curve_validation_data)
    )
    model = Model(id=model_id, project_id=project_id)
    roc = model.get_roc_curve('validation')

    assert roc.source == roc_curve_validation_data['source']
    assert roc.negative_class_predictions == roc_curve_validation_data['negativeClassPredictions']
    assert roc.positive_class_predictions == roc_curve_validation_data['positiveClassPredictions']
    assert roc.roc_points == from_api(roc_curve_validation_data['rocPoints'])
    assert roc.source_model_id == model_id


@responses.activate
@pytest.mark.usefixtures('client')
def test_get_frozen_validation_roc_curve_no_fallback(roc_curve_validation_data_url,
                                                     project_id, model_id):
    responses.add(
        responses.GET,
        roc_curve_validation_data_url,
        status=404
    )
    model = Model(id=model_id, project_id=project_id, is_frozen=True)
    with pytest.raises(ClientError):
        model.get_roc_curve('validation')


@responses.activate
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('known_warning')
def test_get_frozen_validation_roc_curve_with_fallback(
        roc_curve_parent_model_validation_data,
        roc_curve_validation_data_url,
        roc_curve_parent_model_validation_data_url,
        frozen_model_url,
        project_id, model_id, parent_model_id,
        frozen_json):
    responses.add(
        responses.GET,
        roc_curve_validation_data_url,
        status=404
    )
    responses.add(
        responses.GET,
        frozen_model_url,
        body=frozen_json,
        status=200,
        content_type='application/json'
    )
    responses.add(
        responses.GET,
        roc_curve_parent_model_validation_data_url,
        status=200,
        content_type='application/json',
        body=json.dumps(roc_curve_parent_model_validation_data)
    )
    model = Model(id=model_id, project_id=project_id, is_frozen=True)
    roc = model.get_roc_curve('validation', fallback_to_parent_insights=True)

    assert roc.source == roc_curve_parent_model_validation_data['source']
    assert roc.negative_class_predictions == \
        roc_curve_parent_model_validation_data['negativeClassPredictions']
    assert roc.positive_class_predictions == \
        roc_curve_parent_model_validation_data['positiveClassPredictions']
    assert roc.roc_points == from_api(roc_curve_parent_model_validation_data['rocPoints'])
    assert roc.source_model_id == parent_model_id


@responses.activate
@pytest.mark.usefixtures('client')
def test_get_all_roc_curves(roc_curve_validation_data,
                            roc_curve_list_url,
                            project_id, model_id):
    responses.add(
        responses.GET,
        roc_curve_list_url,
        status=200,
        content_type='application/json',
        body=json.dumps({'charts': [roc_curve_validation_data]})
    )
    model = Model(id=model_id, project_id=project_id)
    roc_list = model.get_all_roc_curves()

    assert len(roc_list) == 1
    assert roc_list[0].source == roc_curve_validation_data['source']
    assert roc_list[0].negative_class_predictions == roc_curve_validation_data[
        'negativeClassPredictions']
    assert roc_list[0].positive_class_predictions == roc_curve_validation_data[
        'positiveClassPredictions']
    assert roc_list[0].roc_points == from_api(roc_curve_validation_data['rocPoints'])
    assert roc_list[0].source_model_id == model_id


@responses.activate
@pytest.mark.usefixtures('client')
def test_get_frozen_all_roc_curves_no_fallback(roc_curve_validation_data,
                                               roc_curve_list_url,
                                               project_id, model_id):
    responses.add(
        responses.GET,
        roc_curve_list_url,
        status=200,
        content_type='application/json',
        body=json.dumps({'charts': [roc_curve_validation_data]})
    )
    model = Model(id=model_id, project_id=project_id, is_frozen=True)
    roc_list = model.get_all_roc_curves()

    assert len(roc_list) == 1
    assert roc_list[0].source == roc_curve_validation_data['source']
    assert roc_list[0].negative_class_predictions == roc_curve_validation_data[
        'negativeClassPredictions']
    assert roc_list[0].positive_class_predictions == roc_curve_validation_data[
        'positiveClassPredictions']
    assert roc_list[0].roc_points == from_api(roc_curve_validation_data['rocPoints'])
    assert roc_list[0].source_model_id == model_id


@responses.activate
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('known_warning')
def test_get_forzen_all_roc_curves_with_fallback(roc_curve_validation_data,
                                                 roc_curve_parent_model_validation_data,
                                                 roc_curve_parent_model_holdout_data,
                                                 roc_curve_list_url,
                                                 roc_curve_parent_list_url,
                                                 frozen_model_url,
                                                 project_id, model_id,
                                                 parent_model_id,
                                                 frozen_json):
    responses.add(
        responses.GET,
        roc_curve_list_url,
        status=200,
        content_type='application/json',
        body=json.dumps({'charts': [roc_curve_validation_data]})
    )
    responses.add(
        responses.GET,
        frozen_model_url,
        body=frozen_json,
        status=200,
        content_type='application/json'
    )
    responses.add(
        responses.GET,
        roc_curve_parent_list_url,
        status=200,
        content_type='application/json',
        body=json.dumps({'charts': [roc_curve_parent_model_validation_data,
                                    roc_curve_parent_model_holdout_data]})
    )
    model = Model(id=model_id, project_id=project_id, is_frozen=True)
    roc_list = model.get_all_roc_curves(fallback_to_parent_insights=True)

    assert len(roc_list) == 2
    assert roc_list[0].source == roc_curve_validation_data['source']
    assert roc_list[0].negative_class_predictions == roc_curve_validation_data[
        'negativeClassPredictions']
    assert roc_list[0].positive_class_predictions == roc_curve_validation_data[
        'positiveClassPredictions']
    assert roc_list[0].roc_points == from_api(roc_curve_validation_data['rocPoints'])
    assert roc_list[0].source_model_id == model_id

    assert roc_list[1].source == roc_curve_parent_model_holdout_data['source']
    assert roc_list[1].negative_class_predictions == roc_curve_parent_model_holdout_data[
        'negativeClassPredictions']
    assert roc_list[1].positive_class_predictions == roc_curve_parent_model_holdout_data[
        'positiveClassPredictions']
    assert roc_list[1].roc_points == from_api(roc_curve_parent_model_holdout_data['rocPoints'])
    assert roc_list[1].source_model_id == parent_model_id


def test_get_best_f1_threshold(roc_curve_validation_data):
    # Given ROC curve data
    roc = RocCurve.from_server_data(roc_curve_validation_data)
    # When calculate recommended threshold
    best_threshold = roc.get_best_f1_threshold()
    # Then f1 score for that threshold maximal from all ROC curve points
    best_f1 = roc.estimate_threshold(best_threshold)['f1_score']
    assert all(best_f1 >= roc_point['f1_score'] for roc_point in roc.roc_points)


def test_estimate_threshold_equal(roc_curve_validation_data):
    # Given ROC curve data
    roc = RocCurve.from_server_data(roc_curve_validation_data)
    # When estimating threshold equal to one of precalculated
    threshold = roc_curve_validation_data['rocPoints'][1]['threshold']
    # Then estimate_threshold return valid data
    assert roc.estimate_threshold(threshold)['threshold'] == threshold


def test_estimate_threshold_new(roc_curve_validation_data):
    # Given ROC curve data
    roc = RocCurve.from_server_data(roc_curve_validation_data)
    # When estimating threshold from outside of precalculated
    threshold = roc_curve_validation_data['rocPoints'][1]['threshold'] + 0.1
    # Then estimate_threshold return data for next threshold bigger then requested
    assert roc.estimate_threshold(threshold)['threshold'] > threshold
