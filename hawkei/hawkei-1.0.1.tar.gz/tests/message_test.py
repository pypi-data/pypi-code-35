from hawkei.config import config
from hawkei.store import Store
from hawkei.message import message_base, message_extended

def test_message_base():
    message = message_base()

    assert message['message_id']
    assert message['timestamp']
    assert message['session_tracker_id']

def test_message_extended():
    config.build({
        'api_key': 'xx42',
        'space_name': 'Example',
        'environment_name': 'test',
    })

    message = message_extended()

    assert message['message_id']
    assert message['timestamp']
    assert message['session_tracker_id']
    assert message['environment'] == 'test'

    assert message['library']['name'] == 'hawkei'
    assert message['library']['language'] == 'python'
    assert message['library']['version']

    assert message['server']['host']
    assert message['server']['pid']
    assert message['server']['software']

    assert not message.get('request')

def test_message_extended_with_metadata():
    config.build({
        'api_key': 'xx42',
        'space_name': 'Example',
        'environment_name': 'test',
        'metadata': {
            'version': '1.0'
        }
    })

    message = message_extended()

    assert message['metadata'] == {'version': '1.0'}

def test_message_extended_with_store():
    Store.init()
    Store.add({
        'session_tracker_id': 't-1234',
        'request': {'id': '1234'},
    })

    config.build({
        'api_key': 'xx42',
        'space_name': 'Example',
        'environment_name': 'test',
    })

    message = message_extended()

    assert message['session_tracker_id'] == 't-1234'
    assert message['request'] == {'id': '1234'}
