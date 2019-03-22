import os
from environs import Env

env = Env()

# Package urls
PACKAGE_BASE = os.path.dirname(os.path.dirname(__file__))
DEFAULT_TOKEN_PATH = os.path.join(env('HOME'), '.tda_certs', 'auth-token.json')

# TDAmeritrade urls
AUTH_URL = 'https://auth.tdameritrade.com/auth'
AUTH_QUERIES = '?response_type=code&redirect_uri='
CLIENT_ID_QUERY = '&client_id='
BASE_URL = 'https://api.tdameritrade.com'
TOKEN_REQUEST = '/v1/oauth2/token'
ACCOUNT_URL = '/v1/accounts/'
FIELDS = '?fields='
REFRESH_FIELD = 'grant_type=refresh_token&refresh_token='
