"""
To be implemented.
"""
from __future__ import absolute_import
from __future__ import print_function
from unittest.mock import patch
from lotame.lotame import Lotame
import pytest
import requests

try:
    from unittest.mock import MagicMock
except:
    from mock import MagicMock


@patch('lotame.lotame.requests.get')
@patch('lotame.lotame.Lotame._authenticate')
@patch('lotame.lotame.Lotame._get_service_ticket_token')
def test_get(
        mock_get_service_ticket_token, mock_authenticate, mock_requests_get):
    mock_get_service_ticket_token.return_value = 'token'
    mock_authenticate.return_value.__enter__.return_value = 'token'
    get_res = MagicMock()
    get_res.status_code = 200
    mock_requests_get.return_value = get_res

    l = Lotame()
    l.get('some_end_point', param1=1, param2=2)

    mock_requests_get.assert_any_call(
        'https://api.lotame.com/2/some_end_point?param1=1&param2=2&'
        'ticket=token')


@patch('lotame.lotame.requests.post')
@patch('lotame.lotame.Lotame._authenticate')
@patch('lotame.lotame.Lotame._get_service_ticket_token')
def test_post(
        mock_get_service_ticket_token, mock_authenticate, mock_requests_post):
    mock_get_service_ticket_token.return_value = 'token'
    mock_authenticate.return_value.__enter__.return_value = 'token'
    post_res = MagicMock()
    post_res.status_code = 200
    mock_requests_post.return_value = post_res

    l = Lotame()
    l.post('post_end_point', dict(param1=1, param2=3))

    mock_requests_post.assert_any_call(
        'https://api.lotame.com/2/post_end_point?ticket=token',
        json=dict(param1=1, param2=3))


@patch('lotame.lotame.requests.delete')
@patch('lotame.lotame.Lotame._authenticate')
@patch('lotame.lotame.Lotame._get_service_ticket_token')
def test_delete(
        mock_get_service_ticket_token, mock_authenticate, mock_requests_delete):
    mock_get_service_ticket_token.return_value = 'token'
    mock_authenticate.return_value.__enter__.return_value = 'token'
    delete_res = MagicMock()
    delete_res.status_code = 200
    mock_requests_delete.return_value = delete_res

    l = Lotame()
    l.delete('delete_end_point')

    mock_requests_delete.assert_any_call(
        'https://api.lotame.com/2/delete_end_point?ticket=token')
