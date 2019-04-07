import json
from typing import Union, Tuple, List

from flask import Blueprint
from schematics.exceptions import DataError

from gwap_framework.app import GwapApp
from gwap_framework.errors.base import BaseError
from gwap_framework.errors.not_authorized import NotAuthorizedError
from gwap_framework.errors.not_found import NotFoundError
from gwap_framework.errors.server_error import ServerError
from gwap_framework.errors.service_unavailable import ServiceUnavailableError
from gwap_framework.errors.validation_error import ValidationError
from sqlalchemy.exc import IntegrityError


def error_handler(error: BaseError):
    """Returns Internal server error"""
    return json.dumps(error.to_dict()), getattr(error, 'code'), {'Content-Type': 'application/json'}


def data_error_handler(error: DataError):
    """Returns Internal server error"""
    return json.dumps({
            'code': 422,
            'message': error.to_primitive(),
            'status': 'invalid_payload'
        }), 422, {'Content-Type': 'application/json'}


def integrity_error_handler(error: IntegrityError):
    """Returns Internal server error"""
    return json.dumps({
            'code': 500,
            'message': str(error.orig),
            'status': 'integrity_error'
        }), 500, {'Content-Type': 'application/json'}


class GwapErrorHandlerConfig:
    """
        GwapExceptionHandlerConfig is a middleware which register the errors handlers.
    """
    app = None

    def __init__(self, app: Union[GwapApp, Blueprint], handlers: List[Tuple] = []):
        if app:
            self.init_app(app, handlers)

    def init_app(self, app: GwapApp, handlers: List[Tuple]) -> None:
        self.app = app
        self.app.register_error_handler(BaseError, error_handler)
        self.app.register_error_handler(DataError, data_error_handler)
        self.app.register_error_handler(IntegrityError, integrity_error_handler)
        for error, handler in handlers:
            self.app.register_error_handler(error, handler)
