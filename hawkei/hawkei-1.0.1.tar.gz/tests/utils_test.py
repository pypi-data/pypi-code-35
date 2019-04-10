from hawkei.utils import merge, deep_obfuscate, deep_compact, url_obfuscate

def test_merge():
    dict1 = {'x': 1, 'y': 2}
    dict2 = {'x': 1, 'z': 3}

    result = merge(dict1, dict2)

    assert dict1 == {'x': 1, 'y': 2}
    assert dict2 == {'x': 1, 'z': 3}
    assert result == {'x': 1, 'y': 2, 'z': 3}


def test_deep_obfuscate():
    payload = {
        'password': 'test',
        'another_key': {
            'credit_card': '41111111',
            'valid_key': 'test',
        },
        'withArray': [{
            'credit_card': '41111111',
            'CREDIT_CARD': '41111111',
            'CReDIT_CaRD': '41111111',
            'valid_key': 'test',
        }],
    }

    expected = {
        'password': '[HIDDEN]',
        'another_key': {
            'credit_card': '[HIDDEN]',
            'valid_key': 'test',
        },
        'withArray': [{
            'credit_card': '[HIDDEN]',
            'CREDIT_CARD': '[HIDDEN]',
            'CReDIT_CaRD': '[HIDDEN]',
            'valid_key': 'test',
        }],
    }

    assert deep_obfuscate(payload, ['password', 'credit_card']) == expected

def test_deep_compact():
    payload = {
        'user_id': 'test',
        'another_key': None,
        'nested': {
            'user_id': 'test',
            'another_key': None,
            'host': False,
        },
        'with_array': [
            {},
            {'test': True, 'another_key': None},
        ],
    }

    expected = {
        'user_id': 'test',
        'nested': {
            'user_id': 'test',
            'host': False,
        },
        'with_array': [
            {},
            {'test': True},
        ],
    }

    assert deep_compact(payload) == expected

def test_url_obfuscate():
    url = 'http://test.com?password=1234&test=true'
    expected = 'http://test.com?password=HIDDEN&test=true'
    assert url_obfuscate(url, ['password', 'credit_card']) == expected

    url = 'http://test.com'
    expected = 'http://test.com'
    assert url_obfuscate(url, ['password', 'credit_card']) == expected

    url = 'http://test.com/test?test=true'
    expected = 'http://test.com/test?test=true'
    assert url_obfuscate(url, ['password', 'credit_card']) == expected
