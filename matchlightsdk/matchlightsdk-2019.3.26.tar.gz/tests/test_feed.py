"""Unit tests the feed methods of the Matchlight SDK."""
import csv
import datetime
import io
import json
import random
import time
import uuid

import mock
import pytest
import responses
import six.moves

import matchlight


@pytest.fixture(scope='function')
def start_time():
    """A feed start time fixture."""
    return datetime.datetime.now() - datetime.timedelta(days=5)


@pytest.fixture(scope='function')
def end_time():
    """A feed stop time fixture."""
    return datetime.datetime.now() + datetime.timedelta(days=1)


@pytest.fixture(scope='function')
def feed_name():
    """A feed name fixture."""
    return 'test'


@pytest.fixture(scope='function')
def feed_download_url():
    """A feed download URL."""
    return 'https://matchlight-reports.s3.amazonaws.com/{}.csv'.format(
        str(uuid.uuid4()))


@pytest.fixture(scope='function')
def feed_payload(feed_name, start_time, end_time):
    """A feed payload fixture."""
    return json.dumps({
        'name': feed_name,
        'description': '',
        'recent_alerts_count': 5,
        'start_timestamp': int(matchlight.utils.datetime_to_unix(start_time)),
        'stop_timestamp': int(matchlight.utils.datetime_to_unix(end_time)),
    })


@pytest.fixture(scope='function')
def feed_report_csv():
    """A CSV-formatted feed report fixture."""
    rows = []
    headers = ('ts', 'artifact_id', 'url', 'value', 'description')
    rows.append(','.join(headers))
    for i in six.moves.range(10):
        rows.append(','.join((
            datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            uuid.uuid4().hex,
            'http://pastebin.com/5ZLLE3jY',
            'Potato',
            '',
        )))
    return rows


@pytest.fixture(scope='function')
def feed(feed_payload):
    """A feed object fixture."""
    return matchlight.Feed(**json.loads(feed_payload))


def test_permanent_feed(feed_payload):
    """Verifies the end property of a permanent (non expiring) feed."""
    payload = json.loads(feed_payload)

    payload['stop_timestamp'] = None
    assert matchlight.Feed(**payload).end is None

    del payload['stop_timestamp']
    assert matchlight.Feed(**payload).end is None


def test_feed_details(feed):
    """Verifies the feed details mapping."""
    expected = {
        'name': feed.name,
        'description': feed.description,
        'recent_alerts_count': feed.recent_alerts_count,
        'start_timestamp': feed.start_timestamp,
        'stop_timestamp': feed.stop_timestamp,
    }
    assert expected == feed.details


def test_feed_timestamps(feed):
    """Verifies that feed timestamps are parsed correctly."""
    assert datetime.datetime.fromtimestamp(feed.start_timestamp) == feed.start
    assert datetime.datetime.fromtimestamp(feed.stop_timestamp) == feed.end


@responses.activate
def test_feed_counts(connection, feed, start_time, end_time):
    """Verifies requesting feed counts."""
    expected_response = {
        int(time.time()): random.randint(0, 1000),
        int(time.time()): random.randint(0, 1000),
        int(time.time()): random.randint(0, 1000),
        int(time.time()): random.randint(0, 1000),
    }
    responses.add(
        method=responses.POST,
        url='{}/feeds/{}'.format(matchlight.MATCHLIGHT_API_URL_V2, feed.name),
        json=expected_response,
        status=200
    )
    result = connection.feeds.counts(feed, start_time, end_time)
    assert len(responses.calls) == 1
    assert result == connection.feeds._format_count(expected_response)

    result = connection.feeds.counts(feed.name, start_time, end_time)
    assert len(responses.calls) == 2
    assert result == connection.feeds._format_count(expected_response)


@responses.activate
def test_feed_download(connection, feed, start_time, end_time,
                       feed_download_url, feed_report_csv):
    """Verifies feed downloads."""
    responses.add(
        method=responses.POST,
        url='{}/feed/{}/prepare'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            feed.name
        ),
        json={'feed_response_id': 1},
        status=200
    )
    responses.add(
        method=responses.POST,
        url='{}/feed/{}/link'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            feed.name
        ),
        json={'status': 'pending'},
        status=200
    )
    responses.add(
        method=responses.POST,
        url='{}/feed/{}/link'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            feed.name
        ),
        json={'status': 'ready', 'url': feed_download_url},
        status=200
    )
    responses.add(
        method=responses.GET,
        url=feed_download_url,
        content_type='text/csv',
        body='\n'.join(feed_report_csv),
        status=200
    )

    rows = connection.feeds.download(feed, start_time, end_time)
    assert len(responses.calls) == 4
    feed_rows = [
        connection.feeds._format_feed(row)
        for row in csv.DictReader(feed_report_csv)
    ]
    assert rows == feed_rows

    rows = connection.feeds.download(feed.name, start_time, end_time)
    assert len(responses.calls) == 7
    feed_rows = [
        connection.feeds._format_feed(row)
        for row in csv.DictReader(feed_report_csv)
    ]
    assert rows == feed_rows


@responses.activate
def test_feed_download_failed(connection, feed, start_time, end_time):
    """Verifies that feed download failures throw an SDK exception."""
    prepare_url = '{}/feed/{}/prepare'.format(
        matchlight.MATCHLIGHT_API_URL_V2,
        feed.name
    )
    responses.add(
        method=responses.POST,
        url=prepare_url,
        json={'feed_response_id': 1},
        status=200
    )

    link_url = '{}/feed/{}/link'.format(
        matchlight.MATCHLIGHT_API_URL_V2,
        feed.name
    )
    responses.add(
        method=responses.POST,
        url=link_url,
        json={'status': 'pending'},
        status=200
    )
    responses.add(
        method=responses.POST,
        url=link_url,
        json={'status': 'failed', 'message': ''},
        status=200
    )

    with pytest.raises(matchlight.error.SDKError):
        connection.feeds.download(feed, start_time, end_time)
    assert len(responses.calls) == 3

    responses.add(
        method=responses.POST,
        url=prepare_url,
        json='{}',
        status=400
    )
    with pytest.raises(matchlight.error.SDKError):
        connection.feeds.download(feed, start_time, end_time)
    assert len(responses.calls) == 5

    responses.add(
        method=responses.POST,
        url=link_url,
        json={'status': 'potato'},
        status=200
    ),
    with pytest.raises(matchlight.error.SDKError):
        connection.feeds.download(feed, start_time, end_time)
    assert len(responses.calls) == 6


@responses.activate
@mock.patch('io.open', create=True)
def test_feed_download_output(mock_open, connection, feed, start_time,
                              end_time, feed_download_url, feed_report_csv):
    """Verifies feed download writing to a file."""
    mock_open.return_value = mock.MagicMock(spec=io.IOBase)
    responses.add(
        method=responses.POST,
        url='{}/feed/{}/prepare'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            feed.name
        ),
        json={'feed_response_id': 1},
        status=200
    )
    responses.add(
        method=responses.POST,
        url='{}/feed/{}/link'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            feed.name
        ),
        json={'status': 'pending'},
        status=200
    )
    responses.add(
        method=responses.POST,
        url='{}/feed/{}/link'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            feed.name
        ),
        json={'status': 'ready', 'url': feed_download_url},
        status=200
    )

    body = '\n'.join(feed_report_csv).encode('utf-8')
    responses.add(
        method=responses.GET,
        url=feed_download_url,
        content_type='text/csv',
        body=body,
        status=200
    )

    connection.feeds.download(
        feed, start_time, end_time, save_path='/tmp/output')
    assert len(responses.calls) == 4
    file_handle = mock_open.return_value.__enter__.return_value
    file_handle.write.assert_called_once_with(body)


@responses.activate
def test_feed_iteration(connection, feed):
    """Verifies feed iteration."""
    responses.add(
        method=responses.GET,
        url='{}/feeds'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'feeds': [feed.details]},
        status=200,
    )
    feeds_iterable = iter(connection.feeds)
    assert next(feeds_iterable).details == feed.details
    with pytest.raises(StopIteration):
        next(feeds_iterable)
    assert len(responses.calls) == 1


@responses.activate
def test_feed_list(connection, feed):
    """Verifies feed listing."""
    responses.add(
        method=responses.GET,
        url='{}/feeds'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'feeds': [feed.details]},
        status=200,
    )
    feeds = connection.feeds.all()
    assert len(feeds) == 1
    assert feeds[0].details == feed.details
    assert len(responses.calls) == 1
