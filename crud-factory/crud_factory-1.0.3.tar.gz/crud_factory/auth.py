"""
auth.py

@Author: Olukunle Ogunmokun
@Date: 10th Dec, 2018

This module handles authentication with JWT
"""

import jwt
from flask import request, g, make_response, url_for, current_app

from werkzeug.exceptions import HTTPException

# custom status codes
VALIDATION_FAILED = 409


class ValidationFailed(HTTPException):
    """
    *34* `Further Action Exception`
    Custom exception thrown when further action is required by the user.
    This is only useful when making REST api calls
    """

    name = "Further Action Required"
    code = VALIDATION_FAILED
    description = (
        '<p>Further Action Required</p>'
    )

    def __init__(self, data):
        super(ValidationFailed, self).__init__()
        self.data = data
        self.status = 409


class StewJWT:
    """the custom JWT object to be used by all apps for authentication and authorization
    within the stew eco-system"""

    def __init__(self, app, ref=None, model=None):
        self.app = app if app else current_app
        self.ref = ref if ref else self.app.config.get("JWT_REF", None)
        # self.model = model if model else self.app.config.get("JWT_MODEL", None)
        # self.check_permission = self.app.config.get("CHECK_PERMISSION", None)
        self.permission = self.app.config.get("JWT_PERMISSION", None)

    def encode(self, data, algorithm='HS256'):
        """ wrapper for the encode function in JWT package"""
        key = self.app.config.get('JWT_KEY')
        token = jwt.encode(data, key, algorithm=algorithm)

        return token

    def decode(self, token, algorithm=None):
        """ wrapper for the decode function in JWT package"""
        key = self.app.config.get('JWT_KEY')
        data = jwt.decode(token, key, algorithm=algorithm)

        return data

    def require_jwt(self):
        token = request.headers.get("authorization", None)
        print(token)
        try:
            data = jwt.decode(token, self.app.config.get("JWT_KEY"))
            print(data, "==data==")
        except Exception as e:
            print(e.message)
            raise ValidationFailed({"status": "Failed", "message": e.message})

        return data

    def check_permission(self, permisson_name, permissions, **kwargs):
        """verify if a user has a required permission"""

        permission = permissions.get(permisson_name, None)

        if permission:
            return True
        return False
