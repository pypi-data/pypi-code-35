import hmac
import hashlib
import urllib
import time
import requests
import json


def _sign(secret, signing_string):
    return hmac.new(bytes(secret, "utf-8"), signing_string.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()


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
        print("REMOTE error: " + str(response.content, "utf-8"))
        response.raise_for_status()

