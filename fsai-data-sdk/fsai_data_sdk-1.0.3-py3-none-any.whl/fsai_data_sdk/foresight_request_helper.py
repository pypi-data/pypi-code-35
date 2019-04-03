import hmac
import hashlib
import six
import time
import requests
import json

DEFAULT_ENCODING = "utf-8"


def _sign(secret, signing_string):
    secret_as_bytes = bytes(secret) if six.PY2 else bytes(secret, DEFAULT_ENCODING)
    return hmac.new(secret_as_bytes, signing_string.encode(DEFAULT_ENCODING), digestmod=hashlib.sha256).hexdigest()


def build_get_request(secret, given_params):
    parameters = dict(given_params)
    parameters['timestamp'] = int(round(time.time() * 1000))
    query_string = '&'.join(['%s=%s' % (key, value) for (key, value) in parameters.items()])
    signature = _sign(secret, query_string)
    return query_string + '&signature=' + signature


def get(api_key, secret, endpoint, given_params):
    response = requests.get(endpoint + "?" + build_get_request(secret, given_params),
                 headers ={"X-API-KEY": api_key})
    if response.ok:
        return json.loads(response.content)
    else:
        # If response code is not ok (200), print the resulting http error code with description
        print("REMOTE error: " + str(response.content).encode(DEFAULT_ENCODING))
        response.raise_for_status()

