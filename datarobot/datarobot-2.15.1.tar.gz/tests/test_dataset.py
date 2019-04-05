# coding: utf-8
import json
import responses
import pytest

from datarobot import PredictionDataset, Project
from datarobot.utils import parse_time, datetime_to_string
from tests.test_helpers import fixture_file_path
from tests.utils import assert_equal_py2, assert_equal_py3, request_body_to_json


@pytest.fixture
def list_dataset_json():
    return """
    {"count": 1,
     "next": null,
     "previous": null,
     "data": [
         {
             "id": "ds-id",
             "projectId": "p-id",
             "name": "My PredictionDataset",
             "created": "2016-02-16T12:00:00.123456Z",
             "numRows": 100,
             "numColumns": 20,
             "forecastPoint": null,
             "relaxKnownInAdvanceFeaturesCheck": true,
             "dataQualityWarnings": {
             "has_kia_missing_values_in_forecast_window": false}
         }
     ]
    }
    """


@pytest.fixture
def dataset_json(list_dataset_json):
    data = json.loads(list_dataset_json)
    return json.dumps(data['data'][0])


@pytest.fixture
def dataset_with_relax_kia_check_server_data(dataset_json):
    dataset = dict(json.loads(dataset_json))
    dataset['relaxKnownInAdvanceFeaturesCheck'] = True
    return dataset


@pytest.fixture
def dataset_with_forecast_point_server_data(dataset_json):
    dataset = dict(json.loads(dataset_json))
    dataset['forecastPoint'] = '2017-01-01T15:00:00Z'
    return dataset


@pytest.fixture
def dataset_with_millis_forecast_point_server_data(dataset_json):
    dataset = dict(json.loads(dataset_json))
    dataset['forecastPoint'] = '2017-01-01T15:00:00.800000Z'
    return dataset


@pytest.fixture
def dataset_with_start_end_server_data(dataset_json):
    dataset = dict(json.loads(dataset_json))
    dataset['predictionsStartDate'] = '2017-01-01T15:00:00Z'
    dataset['predictionsEndDate'] = '2017-06-01T15:00:00Z'
    return dataset


@pytest.fixture
def dataset_with_millis_start_end_server_data(dataset_json):
    dataset = dict(json.loads(dataset_json))
    dataset['predictionsStartDate'] = '2017-01-01T15:00:00.800000Z'
    dataset['predictionsEndDate'] = '2017-06-01T15:00:00.800000Z'
    return dataset


dataset_response = {'id': 'ds-id',
                    'projectId': 'p-id',
                    'name': 'My PredictionDataset',
                    'created': '2016-02-16T12:00:00.123456Z',
                    'numRows': 100,
                    'numColumns': 20,
                    'forecastPoint': None,
                    'relax_known_in_advance_features_check': True,
                    'dataQualityWarnings': {'has_kia_missing_values_in_forecast_window': False}
                    }

datasets_list_response = {'count': 1,
                          'next': None,
                          'previous': None,
                          'data': [dataset_response]}


def prep_successful_upload_response(upload_type, body):
    responses.add(responses.POST,
                  'https://host_name.com/projects/p-id/predictionDatasets/{}/'.format(upload_type),
                  body='',
                  status=202,
                  content_type='application/json',
                  adding_headers={'Location': 'https://host_name.com/status/status-id/'}
                  )
    responses.add(responses.GET,
                  'https://host_name.com/status/status-id/',
                  status=303,
                  body='',
                  content_type='application/json',
                  adding_headers={
                      'Location': 'https://host_name.com/projects/p-id/predictionDatasets/ds-id/'}
                  )
    responses.add(responses.GET,
                  'https://host_name.com/projects/p-id/predictionDatasets/ds-id/',
                  status=200,
                  body=body,
                  content_type='application/json')


def assert_matches_expected_dataset(actual_dataset):
    assert actual_dataset.project_id == dataset_response['projectId']
    assert actual_dataset.id == dataset_response['id']
    assert actual_dataset.name == dataset_response['name']
    assert actual_dataset.created == dataset_response['created']
    assert actual_dataset.num_rows == dataset_response['numRows']
    assert actual_dataset.num_columns == dataset_response['numColumns']
    assert actual_dataset.relax_known_in_advance_features_check == dataset_response[
        'relax_known_in_advance_features_check'
    ]
    assert actual_dataset.forecast_point is None
    assert actual_dataset.data_quality_warnings == dataset_response['dataQualityWarnings']


def test_future_proof():
    PredictionDataset.from_server_data(dict(dataset_response, new_key='future'))


@responses.activate
@pytest.mark.usefixtures('client')
def test_list_datasets(list_dataset_json):
    responses.add(responses.GET,
                  'https://host_name.com/projects/p-id/predictionDatasets/',
                  body=list_dataset_json)
    project = Project('p-id')
    datasets = project.get_datasets()
    assert len(datasets) == 1
    dataset = datasets[0]
    assert_matches_expected_dataset(dataset)


@responses.activate
@pytest.mark.usefixtures('client')
def test_retrieve_dataset():
    responses.add(responses.GET,
                  'https://host_name.com/projects/p-id/predictionDatasets/ds-id/',
                  body=json.dumps(dataset_response))
    dataset = PredictionDataset.get('p-id', 'ds-id')
    assert_matches_expected_dataset(dataset)


@responses.activate
@pytest.mark.usefixtures('client')
def test_dataset_repr():
    responses.add(responses.GET,
                  'https://host_name.com/projects/p-id/predictionDatasets/ds-id/',
                  body=json.dumps(dataset_response))
    dataset = PredictionDataset.get('p-id', 'ds-id')
    assert_equal_py2(repr(dataset), "PredictionDataset(u\'My PredictionDataset\')")
    assert_equal_py3(repr(dataset), "PredictionDataset('My PredictionDataset')")


def test_dataset_repr_unicode():
    dataset = PredictionDataset('projectId', 'datasetId', name=u'赤木',
                                created='2016-02-16T12:00:00.123456Z',
                                num_rows=100, num_columns=20)
    assert_equal_py2(repr(dataset), "PredictionDataset(u'\\u8d64\\u6728')")
    assert_equal_py3(repr(dataset), "PredictionDataset('赤木')")


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_url(dataset_json):
    prep_successful_upload_response('urlUploads', dataset_json)
    project = Project('p-id')
    file_url = 'https://my_files.com/my_dataset.csv'
    new_dataset = project.upload_dataset(file_url)
    assert_matches_expected_dataset(new_dataset)
    request_body = request_body_to_json(responses.calls[0].request)
    assert request_body == {'url': file_url}


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_url_with_forecast(dataset_with_forecast_point_server_data):
    prep_successful_upload_response('urlUploads',
                                    json.dumps(dataset_with_forecast_point_server_data))
    project = Project('p-id')
    file_url = 'https://my_files.com/my_dataset.csv'
    forecast_point = parse_time(dataset_with_forecast_point_server_data['forecastPoint'])
    new_dataset = project.upload_dataset(file_url, forecast_point=forecast_point)

    assert new_dataset.forecast_point == forecast_point
    request = request_body_to_json(responses.calls[0].request)
    assert parse_time(request['forecastPoint']) == forecast_point


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_url_with_forecast_millis(
        dataset_with_millis_forecast_point_server_data):
    prep_successful_upload_response('urlUploads',
                                    json.dumps(dataset_with_millis_forecast_point_server_data))
    project = Project('p-id')
    file_url = 'https://my_files.com/my_dataset.csv'
    forecast_point = parse_time(dataset_with_millis_forecast_point_server_data['forecastPoint'])
    new_dataset = project.upload_dataset(file_url, forecast_point=forecast_point)

    assert new_dataset.forecast_point == forecast_point
    assert new_dataset.forecast_point.microsecond == 800000
    request = request_body_to_json(responses.calls[0].request)
    assert parse_time(request['forecastPoint']) == forecast_point


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_file(dataset_json):
    prep_successful_upload_response('fileUploads', dataset_json)
    filepath = fixture_file_path('onehundredrows.csv')
    project = Project('p-id')
    new_dataset = project.upload_dataset(filepath)
    assert_matches_expected_dataset(new_dataset)
    assert 'file' in responses.calls[0].request.body.fields


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_with_dataset_filename(dataset_json):
    prep_successful_upload_response('fileUploads', dataset_json)
    project = Project('p-id')
    dataset_filename = 'my_test_dataset'
    content = b'a,b,c\n' + b'1,2,3\n' * 100
    # Make a call to the API and provide a dataset_filename, rather than using default value.
    project.upload_dataset(content, dataset_filename=dataset_filename)
    fields = responses.calls[0].request.body.fields
    # Test that the provided dataset_filename was used in the request to api
    assert 'file' in fields
    assert fields['file'][0] == dataset_filename


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_file_with_forecast(dataset_with_forecast_point_server_data):
    prep_successful_upload_response('fileUploads',
                                    json.dumps(dataset_with_forecast_point_server_data))
    filepath = fixture_file_path('onehundredrows.csv')
    project = Project('p-id')
    forecast_point = parse_time(dataset_with_forecast_point_server_data['forecastPoint'])
    new_dataset = project.upload_dataset(filepath, forecast_point=forecast_point)

    assert new_dataset.forecast_point == forecast_point
    assert 'forecastPoint' in responses.calls[0].request.body.fields


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_file_with_forecast_millis(
        dataset_with_millis_forecast_point_server_data):
    prep_successful_upload_response('fileUploads',
                                    json.dumps(dataset_with_millis_forecast_point_server_data))
    filepath = fixture_file_path('onehundredrows.csv')
    project = Project('p-id')
    forecast_point = parse_time(dataset_with_millis_forecast_point_server_data['forecastPoint'])
    new_dataset = project.upload_dataset(filepath, forecast_point=forecast_point)

    assert new_dataset.forecast_point == forecast_point
    assert 'forecastPoint' in responses.calls[0].request.body.fields


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_url_with_start_end(dataset_with_start_end_server_data):
    prep_successful_upload_response('urlUploads',
                                    json.dumps(dataset_with_start_end_server_data))
    project = Project('p-id')
    file_url = 'https://my_files.com/my_dataset.csv'
    predictions_start_date = parse_time(dataset_with_start_end_server_data['predictionsStartDate'])
    predictions_end_date = parse_time(dataset_with_start_end_server_data['predictionsEndDate'])

    new_dataset = project.upload_dataset(file_url,
                                         predictions_start_date=predictions_start_date,
                                         predictions_end_date=predictions_end_date)
    assert new_dataset.predictions_start_date == predictions_start_date
    assert new_dataset.predictions_end_date == predictions_end_date
    request = request_body_to_json(responses.calls[0].request)
    assert parse_time(request['predictionsStartDate']) == predictions_start_date
    assert parse_time(request['predictionsEndDate']) == predictions_end_date


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_url_with_start_end_millis(dataset_with_millis_start_end_server_data):
    prep_successful_upload_response('urlUploads',
                                    json.dumps(dataset_with_millis_start_end_server_data))
    project = Project('p-id')
    file_url = 'https://my_files.com/my_dataset.csv'
    predictions_start_date = parse_time(
        dataset_with_millis_start_end_server_data['predictionsStartDate'])
    predictions_end_date = parse_time(
        dataset_with_millis_start_end_server_data['predictionsEndDate'])

    new_dataset = project.upload_dataset(file_url,
                                         predictions_start_date=predictions_start_date,
                                         predictions_end_date=predictions_end_date)
    assert new_dataset.predictions_start_date == predictions_start_date
    assert new_dataset.predictions_end_date == predictions_end_date
    request = request_body_to_json(responses.calls[0].request)
    assert parse_time(request['predictionsStartDate']) == predictions_start_date
    assert parse_time(request['predictionsEndDate']) == predictions_end_date


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_url_fails_when_one_date_provided(dataset_with_start_end_server_data):
    project = Project('p-id')
    file_url = 'https://my_files.com/my_dataset.csv'
    predictions_start_date = parse_time(dataset_with_start_end_server_data['predictionsStartDate'])
    msg = 'Both prediction_start_date and prediction_end_date must be provided at the same time'
    with pytest.raises(ValueError, message=msg):
        project.upload_dataset(file_url, predictions_start_date=predictions_start_date)


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_url_fails_when_fp_and_dates_provided(
        dataset_with_start_end_server_data):
    project = Project('p-id')
    file_url = 'https://my_files.com/my_dataset.csv'
    dataset_with_start_end_server_data['forecastPoint'] = '2017-01-01T15:00:00Z'
    forecast_point = parse_time(dataset_with_start_end_server_data['forecastPoint'])
    predictions_start_date = parse_time(dataset_with_start_end_server_data['predictionsStartDate'])
    predictions_end_date = parse_time(dataset_with_start_end_server_data['predictionsStartDate'])
    msg = ('forecast_point can not be provided together with predictions_start_date or '
           'predictions_end_date')
    with pytest.raises(ValueError, message=msg):
        project.upload_dataset(file_url, forecast_point=forecast_point,
                               predictions_start_date=predictions_start_date,
                               predictions_end_date=predictions_end_date)


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_file_with_start_end(dataset_with_start_end_server_data):
    prep_successful_upload_response('fileUploads',
                                    json.dumps(dataset_with_start_end_server_data))
    filepath = fixture_file_path('onehundredrows.csv')
    project = Project('p-id')
    predictions_start_date = parse_time(dataset_with_start_end_server_data['predictionsStartDate'])
    predictions_end_date = parse_time(dataset_with_start_end_server_data['predictionsEndDate'])

    new_dataset = project.upload_dataset(filepath,
                                         predictions_start_date=predictions_start_date,
                                         predictions_end_date=predictions_end_date)
    assert new_dataset.predictions_start_date == predictions_start_date
    assert new_dataset.predictions_end_date == predictions_end_date
    assert 'predictionsStartDate' in responses.calls[0].request.body.fields
    assert 'predictionsEndDate' in responses.calls[0].request.body.fields


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_file_with_start_end_millis(dataset_with_millis_start_end_server_data):
    prep_successful_upload_response('fileUploads',
                                    json.dumps(dataset_with_millis_start_end_server_data))
    filepath = fixture_file_path('onehundredrows.csv')
    project = Project('p-id')
    predictions_start_date = parse_time(
        dataset_with_millis_start_end_server_data['predictionsStartDate'])
    predictions_end_date = parse_time(
        dataset_with_millis_start_end_server_data['predictionsEndDate'])

    new_dataset = project.upload_dataset(filepath,
                                         predictions_start_date=predictions_start_date,
                                         predictions_end_date=predictions_end_date)
    assert new_dataset.predictions_start_date == predictions_start_date
    assert new_dataset.predictions_end_date == predictions_end_date
    assert 'predictionsStartDate' in responses.calls[0].request.body.fields
    assert 'predictionsEndDate' in responses.calls[0].request.body.fields


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_file_fails_when_one_date_provided(dataset_with_start_end_server_data):
    filepath = fixture_file_path('onehundredrows.csv')
    project = Project('p-id')
    predictions_start_date = parse_time(dataset_with_start_end_server_data['predictionsStartDate'])
    msg = 'Both prediction_start_date and prediction_end_date must be provided at the same time'
    with pytest.raises(ValueError, message=msg):
        project.upload_dataset(filepath, predictions_start_date=predictions_start_date)


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_file_fails_when_fp_and_dates_provided(
        dataset_with_start_end_server_data):
    filepath = fixture_file_path('onehundredrows.csv')
    project = Project('p-id')
    dataset_with_start_end_server_data['forecastPoint'] = '2017-01-01T15:00:00Z'
    forecast_point = parse_time(dataset_with_start_end_server_data['forecastPoint'])
    predictions_end_date = parse_time(dataset_with_start_end_server_data['predictionsStartDate'])
    msg = ('forecast_point can not be provided together with predictions_start_date or '
           'predictions_end_date')
    with pytest.raises(ValueError, message=msg):
        project.upload_dataset(filepath, forecast_point=forecast_point,
                               predictions_end_date=predictions_end_date)


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_data_source(data_sources_endpoint, data_sources_list_server_resp,
                                         airlines10mb_data_source_server_resp, dataset_json):
    data_source_id = airlines10mb_data_source_server_resp['id']
    username = 'my_username'
    password = 'my_password'

    prep_successful_upload_response('dataSourceUploads', dataset_json)
    responses.add(responses.GET, data_sources_endpoint, json=data_sources_list_server_resp)
    project = Project('p-id')

    project.upload_dataset_from_data_source(data_source_id, username=username, password=password)

    assert responses.calls[0].request.method == 'POST'
    request_body = request_body_to_json(responses.calls[0].request)
    assert request_body == {
        'dataSourceId': data_source_id,
        'user': username,
        'password': password
    }


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_data_source_with_forecast(
    data_sources_endpoint, data_sources_list_server_resp, airlines10mb_data_source_server_resp,
    dataset_with_forecast_point_server_data
):
    data_source_id = airlines10mb_data_source_server_resp['id']
    forecast_point = parse_time(dataset_with_forecast_point_server_data['forecastPoint'])
    username = 'my_username'
    password = 'my_password'
    prep_successful_upload_response('dataSourceUploads',
                                    json.dumps(dataset_with_forecast_point_server_data))
    responses.add(responses.GET, data_sources_endpoint, json=data_sources_list_server_resp)
    project = Project('p-id')

    project.upload_dataset_from_data_source(data_source_id, username, password,
                                            forecast_point=forecast_point)

    assert responses.calls[0].request.method == 'POST'
    request_body = request_body_to_json(responses.calls[0].request)
    assert request_body == {
        'dataSourceId': data_source_id,
        'forecastPoint': datetime_to_string(forecast_point),
        'user': username,
        'password': password,
    }


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_data_source_with_forecast_millis(
    data_sources_endpoint, data_sources_list_server_resp, airlines10mb_data_source_server_resp,
    dataset_with_millis_forecast_point_server_data
):
    data_source_id = airlines10mb_data_source_server_resp['id']
    forecast_point = parse_time(dataset_with_millis_forecast_point_server_data['forecastPoint'])
    username = 'my_username'
    password = 'my_password'
    prep_successful_upload_response('dataSourceUploads',
                                    json.dumps(dataset_with_millis_forecast_point_server_data))
    responses.add(responses.GET, data_sources_endpoint, json=data_sources_list_server_resp)
    project = Project('p-id')

    project.upload_dataset_from_data_source(data_source_id, username, password,
                                            forecast_point=forecast_point)

    assert responses.calls[0].request.method == 'POST'
    request_body = request_body_to_json(responses.calls[0].request)
    assert request_body == {
        'dataSourceId': data_source_id,
        'forecastPoint': datetime_to_string(forecast_point),
        'user': username,
        'password': password,
    }


@responses.activate
@pytest.mark.usefixtures('client')
def test_delete_dataset():
    responses.add(responses.DELETE,
                  'https://host_name.com/projects/p-id/predictionDatasets/ds-id/',
                  body='')
    dataset = PredictionDataset.from_server_data(dataset_response)
    dataset.delete()
    assert responses.calls[0].request.method == 'DELETE'
    assert len(responses.calls) == 1


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_url_with_relax_kia_check(dataset_with_relax_kia_check_server_data):
    prep_successful_upload_response('urlUploads',
                                    json.dumps(dataset_with_relax_kia_check_server_data))
    project = Project('p-id')
    file_url = 'https://my_files.com/my_dataset.csv'
    relax_kia_check = parse_time(dataset_with_relax_kia_check_server_data[
                                    'relaxKnownInAdvanceFeaturesCheck'])
    new_dataset = project.upload_dataset(file_url,
                                         relax_known_in_advance_features_check=relax_kia_check)

    assert new_dataset.relax_known_in_advance_features_check == relax_kia_check
    request = request_body_to_json(responses.calls[0].request)
    assert request['relaxKnownInAdvanceFeaturesCheck'] == str(relax_kia_check)


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_file_with_relax_kia_check(dataset_with_relax_kia_check_server_data):
    prep_successful_upload_response('fileUploads',
                                    json.dumps(dataset_with_relax_kia_check_server_data))
    filepath = fixture_file_path('onehundredrows.csv')
    project = Project('p-id')
    relax_kia_check = parse_time(dataset_with_relax_kia_check_server_data[
                                     'relaxKnownInAdvanceFeaturesCheck'])
    new_dataset = project.upload_dataset(filepath,
                                         relax_known_in_advance_features_check=relax_kia_check)

    assert new_dataset.relax_known_in_advance_features_check == relax_kia_check
    assert 'relaxKnownInAdvanceFeaturesCheck' in responses.calls[0].request.body.fields


@responses.activate
@pytest.mark.usefixtures('client')
def test_upload_dataset_from_data_source_with_relax_kia_check(
    data_sources_endpoint, data_sources_list_server_resp, airlines10mb_data_source_server_resp,
        dataset_with_relax_kia_check_server_data
):
    data_source_id = airlines10mb_data_source_server_resp['id']
    relax_kia_check = parse_time(dataset_with_relax_kia_check_server_data[
                                     'relaxKnownInAdvanceFeaturesCheck'])
    username = 'my_username'
    password = 'my_password'
    prep_successful_upload_response('dataSourceUploads',
                                    json.dumps(dataset_with_relax_kia_check_server_data))
    responses.add(responses.GET, data_sources_endpoint, json=data_sources_list_server_resp)
    project = Project('p-id')

    project.upload_dataset_from_data_source(data_source_id, username, password,
                                            relax_known_in_advance_features_check=relax_kia_check)

    assert responses.calls[0].request.method == 'POST'
    request_body = request_body_to_json(responses.calls[0].request)
    assert request_body == {
        'dataSourceId': data_source_id,
        'relaxKnownInAdvanceFeaturesCheck': relax_kia_check,
        'user': username,
        'password': password,
    }
