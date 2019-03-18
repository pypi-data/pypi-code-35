import json
from functools import wraps
from flask import request, jsonify

from .lever_jwt import jwt_decode_auth_token


def authenticate(f, redis=None):
    """

    :param f:
    :param redis: a reference to redis db
    :return:
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(response_object), 401
        auth_token = auth_header.split(" ")[1]
        resp = jwt_decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object['message'] = resp
            return jsonify(response_object), 403
        if redis:
            session_data = json.loads(redis.get(resp.get('id')))
            if session_data is None:
                response_object["message"] = "Authentication invalid"
                return jsonify(response_object), 401
            kwargs.update(dict(session_data=session_data))
        kwargs.update(dict(resp=resp))
        return f(*args, **kwargs)

    return decorated_function
