"""Unit tests the alert methods of the Matchlight SDK."""
import datetime
import time
import uuid

import responses

import matchlight


@responses.activate
def test_alert_dates(connection, alert, alert_payload):
    """Verifies alert date objects are converted correctly."""
    responses.add(
        method=responses.GET,
        url='{}/alerts?limit=50'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'alerts': [alert_payload]},
        status=200
    )
    alerts = connection.alerts.filter(limit=50)
    assert isinstance(alerts[0].date, datetime.datetime)
    assert isinstance(alerts[0].last_modified, datetime.datetime)
    assert len(responses.calls) == 1


@responses.activate
def test_alert_filter(connection, alert, alert_payload):
    """Verifies alert listing and filtering."""
    responses.add(
        method=responses.GET,
        url='{}/alerts?limit=50'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'alerts': [alert_payload]},
        status=200
    )
    alerts = connection.alerts.filter(limit=50)
    assert len(alerts) == 1
    assert alerts[0].id == alert.id
    assert len(responses.calls) == 1


@responses.activate
def test_alert_filter_seen(connection, alert, alert_payload):
    """Verifies alert filtering on 'seen'."""
    # Create opposite alert
    unseen_payload = alert_payload.copy()
    unseen_payload['seen'] = 'false'
    unseen_payload['id'] = str(uuid.uuid4())

    # Get seen alerts
    responses.add(
        method=responses.GET,
        url='{}/alerts?seen=1&limit=50'.format(
            matchlight.MATCHLIGHT_API_URL_V2
        ),
        json={'alerts': [alert_payload]},
        status=200
    )
    alerts = connection.alerts.filter(limit=50, seen=True)
    assert len(alerts) == 1
    assert alerts[0].id == alert_payload['id']
    assert len(responses.calls) == 1

    # Get unseen alerts
    responses.add(
        method=responses.GET,
        url='{}/alerts?seen=0&limit=50'.format(
            matchlight.MATCHLIGHT_API_URL_V2
        ),
        json={'alerts': [unseen_payload]},
        status=200
    )
    alerts = connection.alerts.filter(limit=50, seen=False)
    assert len(alerts) == 1
    assert alerts[0].id == unseen_payload['id']
    assert len(responses.calls) == 2


@responses.activate
def test_alert_filter_archived(connection, alert, alert_payload):
    """Verifies alert filtering on 'archived'."""
    # Create opposite alert
    unarchived_payload = alert_payload.copy()
    unarchived_payload['archived'] = 'false'
    unarchived_payload['id'] = str(uuid.uuid4())

    # Get archived alerts
    responses.add(
        method=responses.GET,
        url='{}/alerts?archived=1&limit=50'.format(
            matchlight.MATCHLIGHT_API_URL_V2
        ),
        json={'alerts': [alert_payload]},
        status=200
    )
    alerts = connection.alerts.filter(limit=50, archived=True)
    assert len(alerts) == 1
    assert alerts[0].id == alert_payload['id']
    assert len(responses.calls) == 1

    # Get unarchived alerts
    responses.add(
        method=responses.GET,
        url='{}/alerts?archived=0&limit=50'.format(
            matchlight.MATCHLIGHT_API_URL_V2
        ),
        json={'alerts': [unarchived_payload]},
        status=200
    )
    alerts = connection.alerts.filter(limit=50, archived=False)
    assert len(alerts) == 1
    assert alerts[0].id == unarchived_payload['id']
    assert len(responses.calls) == 2


@responses.activate
def test_alert_filter_project(connection, alert, alert_payload, project):
    """Verifies alert filtering on 'upload_token'."""
    responses.add(
        method=responses.GET,
        url='{}/alerts?upload_token_filter={}&limit=50'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            project.upload_token
        ),
        json={'alerts': [alert_payload]},
        status=200
    )

    alerts = connection.alerts.filter(limit=50, project=project)
    assert len(alerts) == 1
    assert alerts[0].id == alert_payload['id']
    assert len(responses.calls) == 1


@responses.activate
def test_alert_filter_record(connection, alert, alert_payload,
                             document_record):
    """Verifies alert filtering on 'record_id'."""
    responses.add(
        method=responses.GET,
        url='{}/alerts?record_id_filter={}&limit=50'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            document_record.id
        ),
        json={'alerts': [alert_payload]},
        status=200
    )

    alerts = connection.alerts.filter(limit=50, record=document_record)
    assert len(alerts) == 1
    assert alerts[0].id == alert_payload['id']
    assert len(responses.calls) == 1


@responses.activate
def test_alert_filter_mtime(connection, alert, alert_payload):
    """Verifies alert filtering on 'seen'."""
    now = int(time.time())
    # Two days ago
    old_payload = alert_payload.copy()
    old_payload['mtime'] = now - 172800
    old_payload['id'] = str(uuid.uuid4())

    # Get all alerts
    responses.add(
        method=responses.GET,
        url='{}/alerts?mtime={}&limit=50'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            now - 259200
        ),
        json={'alerts': [alert_payload, old_payload]},
        status=200
    )

    alerts = connection.alerts.filter(
        limit=50,
        last_modified=datetime.datetime.utcfromtimestamp(now - 259200)
    )
    assert len(alerts) == 2
    assert len(responses.calls) == 1

    # Get new alerts
    responses.add(
        method=responses.GET,
        url='{}/alerts?mtime={}&limit=50'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            now - 86400
        ),
        json={'alerts': [alert_payload]},
        status=200
    )

    alerts = connection.alerts.filter(
        limit=50,
        last_modified=datetime.datetime.utcfromtimestamp(now - 86400)
    )
    assert len(alerts) == 1
    assert alerts[0].id == alert_payload['id']
    assert len(responses.calls) == 2


@responses.activate
def test_alert_edit(connection, alert, alert_payload):
    """Verifies alert editing."""
    # Do nothing
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=rsps.POST,
            url='{}/alert/{}/edit'.format(
                matchlight.MATCHLIGHT_API_URL_V2,
                alert.id,
            ),
            json={
                'archived': True,
                'seen': True
            },
            status=200
        )

        response = connection.alerts.edit(alert.id)
        assert response['seen'] is True
        assert response['archived'] is True

    # Un-archive
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=rsps.POST,
            url='{}/alert/{}/edit'.format(
                matchlight.MATCHLIGHT_API_URL_V2,
                alert.id,
            ),
            json={
                'archived': False,
                'seen': True
            },
            status=200
        )
        response = connection.alerts.edit(alert.id, archived=False)

        assert response['seen'] is True
        assert response['archived'] is False

    # Un-see
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=rsps.POST,
            url='{}/alert/{}/edit'.format(
                matchlight.MATCHLIGHT_API_URL_V2,
                alert.id,
            ),
            json={
                'archived': False,
                'seen': False
            },
            status=200
        )
        response = connection.alerts.edit(alert.id, seen=False)
        assert response['seen'] is False
        assert response['archived'] is False

    # Both
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=rsps.POST,
            url='{}/alert/{}/edit'.format(
                matchlight.MATCHLIGHT_API_URL_V2,
                alert.id,
            ),
            json={
                'archived': True,
                'seen': True
            },
            status=200
        )
        response = connection.alerts.edit(alert.id, seen=True, archived=True)
        assert response['seen'] is True
        assert response['archived'] is True


@responses.activate
def test_alert_details(connection, alert, alert_details_pii_payload):
    """Verifies alert get details responses."""
    responses.add(
        method=responses.GET,
        url='{}/alert/{}/details'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            alert.id
        ),
        json=alert_details_pii_payload,
        status=200
    )

    details_ = connection.alerts.get_details(alert)
    assert details_ == alert_details_pii_payload
    assert len(responses.calls) == 1

    details_ = connection.alerts.get_details(alert.id)
    assert details_ == alert_details_pii_payload
    assert len(responses.calls) == 2
