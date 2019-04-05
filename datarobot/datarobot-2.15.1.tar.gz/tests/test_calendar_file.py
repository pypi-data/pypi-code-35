# coding: utf-8
import json
import pytest
import responses

from trafaret import DataError
from datarobot.errors import ClientError, IllegalFileName

from datarobot import CalendarFile, Project, SharingAccess, enums
from tests.test_helpers import fixture_file_path

_base_url = 'https://host_name.com/calendars/'
_valid_calendar_id = 'calId'
_invalid_calendar_id = 'badCalId'
_valid_calendar_url = '{0}{1}/'.format(_base_url, _valid_calendar_id)
_invalid_calendar_url = '{0}{1}/'.format(_base_url, _invalid_calendar_id)

calendar_dict = {
    'numEvents': 5,
    'name': 'calendar.csv',
    'calendarStartDate': '2018-01-01',
    'created': '2018-07-16T17:28:13.929687Z',
    'numEventTypes': 5,
    'source': 'calendar.csv',
    'calendarEndDate': '2018-07-04',
    'projectIds': [],
    'Id': 'calId',
    'role': 'OWNER'
}

calendar_dict_with_name = {
    'numEvents': 5,
    'name': 'My Calendar',
    'calendarStartDate': '2018-01-01',
    'created': '2018-07-16T17:28:13.929687Z',
    'numEventTypes': 5,
    'source': 'calendar.csv',
    'calendarEndDate': '2018-07-04',
    'projectIds': [],
    'Id': 'calId',
    'role': 'OWNER'
}


@pytest.fixture
def calendar_json():
    return json.dumps(calendar_dict)


@pytest.fixture
def calendar_with_name_json():
    return json.dumps(calendar_dict_with_name)


@pytest.fixture
def calendar_list_json():
    cal_list = []
    for i in range(1, 11):
        cal_copy = calendar_dict.copy()
        cal_copy['name'] = 'cal_name{0}'.format(i)
        cal_list.append(cal_copy)
    return json.dumps({
        'count': len(cal_list),
        'data': cal_list,
        'next': None,
        'previous': None
    })


@pytest.fixture
def calendar_access_control_list_json():
    ac_list = [{'userId': 'ac{0}'.format(i), 'username': 'user{0}'.format(i),
                'canShare': True, 'role': 'OWNER'} for i in range(1, 11)]
    return json.dumps({
        'count': len(ac_list),
        'data': ac_list,
        'next': None,
        'previous': None
    })


@pytest.fixture
def calendar_invalid_json():
    return json.dumps({"message": "Not Found"})


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_create(calendar_json):
    responses.add(
        responses.POST,
        _base_url + 'fileUpload/',
        body='',
        status=202,
        adding_headers={'Location': 'https://host_name.com/status/some-status/'},
        content_type='application_json'
    )
    responses.add(
        responses.GET,
        'https://host_name.com/status/some-status/',
        body='',
        status=303,
        adding_headers={'Location': _valid_calendar_url},
        content_type='application/json'
    )
    responses.add(
        responses.GET,
        _valid_calendar_url,
        body=calendar_json,
        status=200, content_type='application/json'
    )
    calendar = CalendarFile.create(fixture_file_path('calendar.csv'))
    assert isinstance(calendar, CalendarFile)
    assert calendar.id == 'calId'
    assert calendar.num_events == 5
    assert calendar.name == 'calendar.csv'
    assert calendar.calendar_start_date == '2018-01-01'
    assert calendar.calendar_end_date == '2018-07-04'
    assert calendar.created == '2018-07-16T17:28:13.929687Z'
    assert calendar.num_event_types == 5
    assert calendar.project_ids == []
    assert calendar.role == 'OWNER'


def test_calendar_create_non_existent_file():
    with pytest.raises(ValueError):
        CalendarFile.create('bad_file_path')


def test_calendar_create_not_a_string():
    with pytest.raises(ValueError):
        CalendarFile.create({'this definitely': 'isn"t a string'})


@pytest.fixture
def project_without_partition(project_without_target_data):
    project_without_target_data['partition'] = None
    return Project(**project_without_target_data)


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_create_with_name(calendar_with_name_json):
    responses.add(
        responses.POST,
        _base_url + 'fileUpload/',
        body='',
        status=202,
        adding_headers={'Location': 'https://host_name.com/status/some-status/'},
        content_type='application_json'
    )
    responses.add(
        responses.GET,
        'https://host_name.com/status/some-status/',
        body='',
        status=303,
        adding_headers={'Location': _valid_calendar_url},
        content_type='application/json'
    )
    responses.add(
        responses.GET,
        _valid_calendar_url,
        body=calendar_with_name_json,
        status=200, content_type='application/json'
    )
    calendar = CalendarFile.create(fixture_file_path('calendar.csv'),
                                   calendar_name='My Calendar')
    assert isinstance(calendar, CalendarFile)
    assert calendar.id == 'calId'
    assert calendar.num_events == 5
    assert calendar.name == 'My Calendar'
    assert calendar.calendar_start_date == '2018-01-01'
    assert calendar.calendar_end_date == '2018-07-04'
    assert calendar.created == '2018-07-16T17:28:13.929687Z'
    assert calendar.num_event_types == 5
    assert calendar.project_ids == []
    assert calendar.role == 'OWNER'


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_get(calendar_json):
    responses.add(
        responses.GET,
        _valid_calendar_url,
        body=calendar_json,
        status=200,
        content_type='application/json'
    )
    calendar = CalendarFile.get(_valid_calendar_id)
    assert isinstance(calendar, CalendarFile)
    assert calendar.id == 'calId'
    assert calendar.num_events == 5
    assert calendar.name == 'calendar.csv'
    assert calendar.calendar_start_date == '2018-01-01'
    assert calendar.calendar_end_date == '2018-07-04'
    assert calendar.created == '2018-07-16T17:28:13.929687Z'
    assert calendar.num_event_types == 5
    assert calendar.project_ids == []
    assert calendar.role == 'OWNER'


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_invalid_get(calendar_invalid_json):
    responses.add(responses.GET,
                  _invalid_calendar_url,
                  body=calendar_invalid_json)
    with pytest.raises(DataError):
        CalendarFile.get(_invalid_calendar_id)


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_list(calendar_list_json):
    responses.add(responses.GET,
                  _base_url,
                  body=calendar_list_json)
    cal_list = CalendarFile.list()
    assert len(cal_list) == 10
    for item in cal_list:
        assert isinstance(item, CalendarFile)


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_delete_valid():
    responses.add(responses.DELETE,
                  _valid_calendar_url,
                  status=204)
    assert CalendarFile.delete('calId') is None


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_delete_invalid():
    responses.add(responses.DELETE,
                  _invalid_calendar_url,
                  status=404)
    with pytest.raises(ClientError):
        CalendarFile.delete(_invalid_calendar_id)


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_update_name_valid():
    responses.add(responses.PATCH,
                  _valid_calendar_url,
                  status=200)
    assert CalendarFile.update_name(_valid_calendar_id, 'new name') == 200


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_update_name_invalid_calendar():
    responses.add(responses.PATCH,
                  _invalid_calendar_url,
                  status=404)
    with pytest.raises(ClientError):
        CalendarFile.update_name(_invalid_calendar_id, 'new name')


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_update_name_invalid_name():
    with pytest.raises(IllegalFileName):
        CalendarFile.update_name(_valid_calendar_id, '£ ¥\n§ ¾')


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_sharing_valid():
    responses.add(responses.PATCH,
                  _valid_calendar_url + 'accessControl/',
                  status=200)
    payload = [SharingAccess('valid_username@datarobot.com', enums.SHARING_ROLE.READ_WRITE)]
    assert CalendarFile.share(_valid_calendar_id, payload) == 200


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_sharing_invalid_username():
    responses.add(responses.PATCH,
                  _invalid_calendar_url + 'accessControl/',
                  status=422)
    payload = [SharingAccess('invalid_valid_username@datarobot.com', enums.SHARING_ROLE.READ_WRITE)]
    with pytest.raises(ClientError):
        CalendarFile.share(_invalid_calendar_id, payload)


def test_calendar_sharing_invalid_access_list():
    # invalid access_list
    payload = {"look at me, I'm a": 'dict'}
    with pytest.raises(AssertionError):
        CalendarFile.share(_valid_calendar_id, payload)
    # invalid items in access_list
    payload = [i for i in range(10)]
    with pytest.raises(AssertionError):
        CalendarFile.share(_valid_calendar_id, payload)


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_sharing_access_list(calendar_access_control_list_json):
    responses.add(
        responses.GET,
        _valid_calendar_url + 'accessControl/',
        body=calendar_access_control_list_json,
    )
    access_control_list = CalendarFile.get_access_list(_valid_calendar_id)
    assert len(access_control_list) == 10
    for item in access_control_list:
        assert isinstance(item, SharingAccess)


@responses.activate
@pytest.mark.usefixtures('client')
def test_calendar_sharing_access_list_user_no_access():
    responses.add(
        responses.GET,
        _valid_calendar_url + 'accessControl/',
        status=404
    )
    with pytest.raises(ClientError):
        CalendarFile.get_access_list(_valid_calendar_id)


def test_retrieve_calendar_id_project_pre_aim(project_without_partition):
    assert project_without_partition.calendar_id is None
