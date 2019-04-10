from datetime import datetime, timezone
import json
from requests import sessions

from hawkei.config import config
from hawkei.utils import deep_obfuscate

_session = sessions.Session()

def create(resource, payload):
    payload['sent_at'] = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    payload = deep_obfuscate(payload, config.data['obfuscated_fields'])

    data = json.dumps(payload).encode()
    url = '{0}/{1}'.format(config.data['api_host'], _path(resource))

    request = _session.post(url, data=data, headers=_headers(), timeout=5)

    if request.status_code >= 200 and request.status_code < 300: return request
    if request.status_code == 400: raise ApiError(request.status_code, 'Bad response from server')
    if request.status_code == 401: raise ApiError(request.status_code, 'Unauthorized, please check your api key')
    if request.status_code == 404: raise ApiError(request.status_code, 'Requested Resource not found')
    if request.status_code == 408: raise ApiError(request.status_code, 'Server timeout, verify status of the server')
    if request.status_code == 422: raise ApiError(request.status_code, 'Invalid parameters')
    if request.status_code in [449, 444, 501, 502]: raise ApiError(request.status_code, 'Server Error, please check with Hawkei')

    raise ApiError(request.status_code, request.reason)

def _path(resource):
    return 'api/{0}/{1}'.format(config.data['api_version'], resource.name())

def _headers():
    return ({
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Api-Key': config.data['api_key'],
        'X-Space-Name': config.data['space_name'],
        'X-Environment-Name': config.data['environment_name'],
    })


class ApiError(Exception):

    def __init__(self, status_code, message):
        super(ApiError, self).__init__(message)
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return "{0}: {1}".format(self.status_code, self.message)
