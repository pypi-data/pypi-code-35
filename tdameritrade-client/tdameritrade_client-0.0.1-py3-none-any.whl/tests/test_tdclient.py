import pytest

from tdameritrade_client.client import TDClient

CONFIG = {'acct_number': 422058925}


def test_tdclient_from_dict():
    td_client = TDClient.from_dict({**CONFIG})



def test__build_headers_fails_without_auth():
    td_client = TDClient.from_dict(CONFIG)
    with pytest.raises(AssertionError):
        _ = td_client._build_header()
