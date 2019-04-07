import os
from environs import Env

env = Env()

# Package urls
PACKAGE_BASE = os.path.dirname(os.path.dirname(__file__))
DEFAULT_TOKEN_PATH = os.path.join(env('HOME'), '.tda_certs', 'auth-token.json')

# TDAmeritrade base urls
AUTH_URL = 'https://auth.tdameritrade.com/auth'
BASE_URL = 'https://api.tdameritrade.com'

# Resource URLs
TOKEN_URL = '/v1/oauth2/token'
ACCOUNT_URL = '/v1/accounts/'
INSTRUMENTS_URL = '/v1/instruments/'
QUOTES_URL = '/v1/marketdata/quotes'

# Params
AUTH_PARAMS = '?response_type=code&redirect_uri='
APIKEY_PARAM = '?apikey='
