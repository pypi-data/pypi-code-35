from hawkei.config import Config

def test_base_config():
    config = Config()

    config.build({
        'api_key': 'xx42',
        'space_name': 'Example',
        'environment_name': 'test',
    })

    assert config.data['api_key'] == 'xx42'
    assert config.data['space_name'] == 'Example'
    assert config.data['environment_name'] == 'test'
    assert config.data['api_host'] == 'https://api.hawkei.io'
    assert config.data['api_version'] == 'v1'
    assert config.data['enabled']
    assert config.data['obfuscated_fields']
    assert config.data['metadata'] == {}
    assert config.data['domain'] is None

def test_override_config():
    config = Config()

    config.build({
        'api_key': 'xx42',
        'space_name': 'Example',
        'environment_name': 'test',
        'enabled': False,
        'api_host': 'http:/test.com'
    })

    assert config.data['api_key'] == 'xx42'
    assert config.data['space_name'] == 'Example'
    assert config.data['environment_name'] == 'test'
    assert config.data['api_host'] == 'http:/test.com'
    assert config.data['api_version'] == 'v1'
    assert not config.data['enabled']
    assert config.data['obfuscated_fields']
    assert config.data['metadata'] == {}
    assert config.data['domain'] is None

def test_invalid_config():
    config = Config()

    try:
        config.build({})
    except AssertionError:
        assert True
    else:
        assert False

def test_active():
    config = Config()

    assert not config.active()

    config.build({
        'api_key': 'xx42',
        'space_name': 'Example',
        'environment_name': 'test',
    })

    assert config.active()

    config.build({
        'api_key': 'xx42',
        'space_name': 'Example',
        'environment_name': 'test',
        'enabled': False,
    })

    assert not config.active()
