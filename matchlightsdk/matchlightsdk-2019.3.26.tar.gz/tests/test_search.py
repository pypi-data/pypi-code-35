"""Unit tests the alert methods of the Matchlight SDK."""
import datetime
import json

import responses

import matchlight


@responses.activate
def test_pii_search(connection, pii_search_email_only_results):
    """Verifies alert listing and filtering."""
    responses.add(
        method=responses.POST,
        url='{}/pii_search'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'results': pii_search_email_only_results},
        status=200
    )

    assert list(
        connection.pii_search(email='familybird@terbiumlabs.com')
    ) == [
        {
            'fields': ['email'],
            'ts': datetime.datetime(2018, 7, 25, 20, 0, 44),
            'source': 'Exactis Breach June 2018'
        },
        {
            'fields': ['email'],
            'ts': datetime.datetime(2017, 1, 25, 2, 35, 4),
            'source': 'https://pastebin.com/raw.php?i=1DgbtSZc'
        },
        {
            'fields': ['email'],
            'ts': datetime.datetime(2017, 2, 8, 7, 59, 39),
            'source': 'Zoosk Breach Nov 2016'
        },
        {
            'fields': ['email'],
            'ts': datetime.datetime(2016, 11, 24, 0, 18, 27),
            'source': 'https://www.reddit.com/r/AskReddit/comments/3oqj4a'
        }
    ]

    assert json.loads(responses.calls[0].request.body) == {
        'email_fingerprints': [['ff71225ace46c2b0'], ['293de73a18a5e063']],
        'limit': 50,
    }


@responses.activate
def test_pii_search_limit(connection, pii_search_email_only_results):
    """Verifies alert listing and filtering."""
    responses.add(
        method=responses.POST,
        url='{}/pii_search'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'results': pii_search_email_only_results[:2]},
        status=200
    )

    assert list(
        connection.pii_search(email='familybird@terbiumlabs.com', limit=2)
    ) == [
        {
            'fields': ['email'],
            'ts': datetime.datetime(2018, 7, 25, 20, 0, 44),
            'source': 'Exactis Breach June 2018'
        },
        {
            'fields': ['email'],
            'ts': datetime.datetime(2017, 1, 25, 2, 35, 4),
            'source': 'https://pastebin.com/raw.php?i=1DgbtSZc'
        }
    ]

    assert json.loads(responses.calls[0].request.body) == {
        'email_fingerprints': [['ff71225ace46c2b0'], ['293de73a18a5e063']],
        'limit': 2,
    }
