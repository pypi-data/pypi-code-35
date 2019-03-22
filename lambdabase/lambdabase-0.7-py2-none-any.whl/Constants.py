"""
Key constants for the cued application. Constants contains values
used throughout the application Parameters represents keys for accessing
specific elements inside rest post, put and get data.
"""


class Constants(object):
    """
    Application constants
    """
    LOCAL_ENVIRONMENT_KEY = 'local'

    DATETIME_FORMAT_INTERNAL = '%Y%m%d%H%M%S%f'
    DATETIME_FORMAT_MS = '%Y-%m-%d %H:%M:%S.%f'
    DATETIME_FORMAT_ES = '%Y%m%dT%H%M%S.%f'
    DATETIME_FORMAT_DROPBOX = '%a, %d %b %Y %H:%M:%S'
    DATETIME_FORMAT_FACEBOOK = '%Y-%m-%dT%H:%M:%S.%f'

    UUIDREGEX = '[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}'
    DIGITREGEX = '[0-9]+'
    OBJECTIDREGEX = '[a-zA-Z0-9]{10}'

    supported_keys = [
        'levelname',
        'message',
        'module',
        'filename',
        'funcName',
        'lineno',
        'name'
    ]

    log_format = lambda x: ['%({0:s})'.format(i) for i in x]
    LOG_FORMAT = ' '.join(log_format(supported_keys))
