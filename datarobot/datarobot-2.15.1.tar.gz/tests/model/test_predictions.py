import json
import pandas as pd
import pytest
import responses
from datarobot import Predictions


@pytest.fixture
def sample_prediction():
    return {
        u'positiveClass': None,
        u'task': u'Regression',
        u'predictions': [
            {u'positiveProbability': None, u'prediction': 32.0,
             u'rowId': 0},
            {u'positiveProbability': None, u'prediction': 100.0,
             u'rowId': 1},
            {u'positiveProbability': None, u'prediction': 212.0,
             u'rowId': 2}
        ]
    }


@pytest.fixture
def prediction_id():
    return '59d92fe8962d7464ca8c6bd6'


@pytest.fixture
def model_id():
    return "modelid"


@pytest.fixture
def dataset_id():
    return "datasetid"


@responses.activate
def test_get__no_requests_made(project_id, prediction_id):
    Predictions.get(project_id, prediction_id)
    assert len(responses.calls) == 0


@responses.activate
@pytest.mark.usefixtures('client')
def test_list__ok(project_id, model_id, prediction_id, dataset_id):
    url = 'http://localhost/api/v2/projects/{}/predictions/{}/'.format(project_id,
                                                                       prediction_id)
    prediction_stub = {
        'url': 'https://host_name.com/projects/{}/predictions/{}//'.format(
            project_id,
            prediction_id,
        ),
        'id': prediction_id,
        'modelId': model_id,
        'datasetId': dataset_id,
        'url': url
    }
    responses.add(
        responses.GET,
        'https://host_name.com/projects/{}/predictions/'.format(
            project_id,
        ),
        status=200,
        body=json.dumps({'data': [prediction_stub]}),
    )

    predictions_list = Predictions.list(project_id)

    assert len(predictions_list) == 1
    prediction = predictions_list[0]
    assert prediction.project_id == project_id
    assert prediction.model_id == model_id
    assert prediction.dataset_id == dataset_id
    assert prediction.prediction_id == prediction_id


@responses.activate
@pytest.mark.usefixtures('client')
def test_get_all_as_dataframe__ok(
        project_id, prediction_id,
        project_url, project_with_target_json, sample_prediction
):
    url = 'https://host_name.com/projects/{}/predictions/{}/'.format(
        project_id,
        prediction_id,
    )
    responses.add(
        responses.GET,
        url,
        body=json.dumps(sample_prediction),
        status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        project_url,
        body=project_with_target_json,
        status=200,
        content_type='application/json'
    )

    obj = Predictions.get(project_id, prediction_id)
    data_frame = obj.get_all_as_dataframe()

    assert isinstance(data_frame, pd.DataFrame)
    assert data_frame.shape == (len(sample_prediction['predictions']), 2)
    assert list(data_frame.columns) == [
        'prediction',
        'row_id',
    ]


def test_repr():
    preds = Predictions('project_id', 'prediction_id', 'model_id', 'dataset_id')

    assert repr(preds) == "Predictions(prediction_id='prediction_id', project_id='project_id', " \
                          "model_id='model_id', dataset_id='dataset_id')"
