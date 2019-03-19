from aioroku.core import AioRoku
import os

from aiohttp import ClientSession, ClientTimeout
from asynctest import patch, CoroutineMock
import pytest

TO = ClientTimeout(total=5)
TESTS_PATH = os.path.abspath(os.path.dirname(__file__))


@patch('aiohttp.ClientSession._request')
async def test_power_state(mock_req):
    """Ensures returns the power state from power-mode node of device-info."""
    mock_req.return_value.read = CoroutineMock()
    mock_req.return_value.read.return_value = '''<?xml version="1.0" encoding=
    "UTF-8" ?><device-info><power-mode>Headless</power-mode></device-info>'''
    async with ClientSession(timeout=TO) as sesh:
        fauxku = AioRoku('6.6.6', session=sesh)
        power = await fauxku.power_state
        assert power == 'Headless'
    assert mock_req.assert_awaited


@patch('aiohttp.ClientSession._request')
async def test_active_app(mock_req):
    """Tests the correct app returned on three calls to active_app method."""
    mock_req.return_value.read = CoroutineMock()
    mock_req.return_value.read.side_effect = ['''<?xml version="1.0" encoding=
    "UTF-8" ?>
    <active-app>
    <app id="12" subtype="ndka" type="appl" version="4.2.81179021">Netflix</app>
    </active-app>''', '''<?xml version="1.0" encoding="UTF-8" ?>
    <active-app>
    <app>Roku</app>
    <screensaver id="72728" subtype="sdka" type="ssvr"
    version="2.3.47">Photo Collage</screensaver>
    </active-app>''', '''<?xml version="1.0" encoding="UTF-8" ?>
    <active-app>
    <app>Roku</app>
    </active-app>''']
    async with ClientSession(timeout=TO) as sesh:
        fauxku = AioRoku('6.6.6', session=sesh)
        app = await fauxku.active_app
        assert app.name == 'Netflix'
        next_app = await fauxku.active_app
        assert next_app.is_screensaver is True
        third_app = await fauxku.active_app
        assert third_app.name == 'Roku'
        assert third_app.is_screensaver is False
        assert mock_req.await_count == 3


@patch('aiohttp.ClientSession._request')
async def test_bad_command(mock_req):
    """Tests to ensure bad keypresses raise AttributeError exception."""
    mock_req.return_value.read = CoroutineMock()
    async with ClientSession(timeout=TO) as sesh:
        fauxku = AioRoku('6.6.6', session=sesh)
        with pytest.raises(AttributeError):
            await fauxku.bad_request


@patch('aiohttp.ClientSession._request')
async def test_sw_info(mock_req):
    """Tests the sw_info attribute show the version and build number."""
    xml_path = os.path.join(TESTS_PATH, 'responses', 'device-info.xml')
    mock_req.return_value.read = CoroutineMock()
    with open(xml_path) as xml_data_response:
        xml_data = xml_data_response.read().encode('utf-8')
    mock_req.return_value.read.return_value = xml_data
    async with ClientSession(timeout=TO) as sesh:
        fauxku = AioRoku('6.6.6', session=sesh)
        assert await fauxku.sw_info == ('7.00', '09044')
