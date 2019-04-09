"""Settings for HealthChecker."""

import logging.config
import os


_loglevel_raw = os.getenv('HEALTHCHECKER_LOG_LEVEL', 'INFO').upper()
LOGLEVEL = _loglevel_raw \
    if _loglevel_raw in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL') \
    else 'INFO'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} p:{process:d} t:{thread:d} '
                      '[{name}.{funcName}:{lineno:d}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # 'file': {
        #     'class': 'logging.FileHandler',
        #     'formatter': 'simple',
        #     'filename': 'healthchecker.log',
        # },
    },
    'loggers': {
        'healthchecker': {
            'handlers': ['console'],
            'level': LOGLEVEL,
        },
    },
}
logging.config.dictConfig(LOGGING)

# See https://github.com/settings/developers
GITHUB_API_TOKEN = os.getenv('HEALTHCHECKER_GITHUB_API_TOKEN')
GITHUB_REPO = os.getenv('HEALTHCHECKER_GITHUB_REPO')
GITHUB_FILENAME = os.getenv('HEALTHCHECKER_GITHUB_FILENAME')
GITHUB_BRANCH = os.getenv('HEALTHCHECKER_GITHUB_BRANCH', 'master')
GITHUB_COMMITTER_EMAIL = os.getenv('HEALTHCHECKER_GITHUB_COMMITTER_EMAIL',
                                   'hackan+healthchecker@rlab.be')

# Comma-separated URLs list
URLS = os.getenv('HEALTHCHECKER_URLS', '').split(',')

# Comma-separated list of validations to run on given URLs
URLS_VALIDATION = os.getenv('HEALTHCHECKER_URLS_VALIDATION', '').split(',')

# Requests timeout in seconds
REQUESTS_TIMEOUT = os.getenv('HEALTHCHECKER_REQUESTS_TIMEOUT', 10)

# URL to send failed checks via POST as notification
NOTIFY_URL = os.getenv('HEALTHCHECKER_NOTIFY_URL')

# Optional payload to send to the notify URL
# It prepends this payload to the comma-separated list of URLs that failed
# validation, unless that it contains the string HEALTHCHECKER_FAILED_URLS
# (case sensitive), where it will replace that string by the comma-separated
# list of URLs, and send the entire payload.
# Example 1: HEALTHCHECKER_NOTIFY_PAYLOAD=here comes the failed urls...
# Example 2: HEALTHCHECKER_NOTIFY_PAYLOAD={"data": "HEALTHCHECKER_FAILED_URLS"}
NOTIFY_PAYLOAD = os.getenv('HEALTHCHECKER_NOTIFY_PAYLOAD')

# Optional comma-separated list of headers to send to the notify URL
# The headers must be specified as name and value separated by a space:
# <header name> <header value>, and successive headers separated by comma.
# Example 1: HEALTHCHECKER_NOTIFY_HEADERS=X-Auth:4c18a291d7d8e7946cb9db9cbb3e1f49
# Example 2: HEALTHCHECKER_NOTIFY_HEADERS=Content-Type:application/json,X-MyVal:1
NOTIFY_HEADERS = os.getenv('HEALTHCHECKER_NOTIFY_HEADERS', '').split(',')

# Settings override
try:
    from .local_settings import *  # noqa
except ImportError:
    pass
