import os


def env_to_bool(name, default=False):
    var = os.environ.get(name, '')
    res = default
    if default == True:
        if var in ['false', 'False', '0', 0]:
            res = False
    else:
        if var in ['true', 'True', '1', 1]:
            res = True
    return res

DEBUG = env_to_bool('PESCATORE_CLI_DEBUG', True)

REQUEST_TIMEOUT = 10  # s

PESCATORE_BASE_URL = os.getenv('PESCATORE_BASE_URL', 'http://pescatore.pescatore:9002/pescatore')

PESCATORE_CLI_JWT_HEADER = os.getenv('PESCATORE_CLI_JWT_HEADER', 'Bearer')
PESCATORE_CLI_JWT = os.getenv('PESCATORE_CLI_JWT', None)

PESCATORE_CLI_API_KEY_HEADER = os.getenv('PESCATORE_CLI_API_KEY_HEADER', 'apikey')
PESCATORE_CLI_API_KEY = os.getenv('PESCATORE_CLI_API_KEY', None)

PESCATORE_CLI_CONSUMER_HEADER = os.getenv('PESCATORE_CLI_CONSUMER_HEADER', None)
PESCATORE_CLI_CONSUMER_GROUPS_HEADER = os.getenv('PESCATORE_CLI_CONSUMER_GROUPS_HEADER', None)

PESCATORE_CLI_DOMAIN = os.getenv('PESCATORE_CLI_DOMAIN', 'pescatore.pescatore')
