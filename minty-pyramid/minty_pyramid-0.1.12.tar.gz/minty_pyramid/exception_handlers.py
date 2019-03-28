import logging

from jsonschema.exceptions import ValidationError
from minty.exceptions import Conflict, Forbidden, NotFound
from pyramid.view import exception_view_config


@exception_view_config(NotFound, renderer="json")
def exception_cqrs_not_found(exc, request):
    """Raised when an item not found.

    :param exc: raised exception
    :type exc: NotFound
    :param request: request
    :type request: request
    :return: error message
    :rtype: dict
    """
    errors = [{"title": f"{exc}"}]
    body = {"errors": errors}
    request.response.status = 404
    return body


@exception_view_config(Forbidden, renderer="json")
def exception_cqrs_forbidden(exc, request):
    """Raised when the user doesn't have permission.

    :param exc: raised exception
    :type exc: Forbidden
    :param request: request
    :type request: request
    :return: error message
    :rtype: dict
    """
    errors = [{"title": f"{exc}"}]
    body = {"errors": errors}
    request.response.status = 403
    return body


@exception_view_config(Conflict, renderer="json")
def exception_cqrs_conflict(exc, request):
    """Raised when a command's parameters conflict with current state.

    :param exc: raised exception
    :type exc: Conflict
    :param request: request
    :type request: request
    :return: error message
    :rtype: dict
    """
    errors = [{"title": f"{exc}"}]
    body = {"errors": errors}
    request.response.status = 409
    return body


@exception_view_config(ValidationError, renderer="json")
def exception_cqrs_validation(exc, request):
    """Raised when validation of JSON schema encounters errors.

    :param exc: raised exception
    :type exc: ValidationError
    :param request: request
    :type request: request
    :return: error message
    :rtype: dict
    """
    errors = [{"title": f"{exc.message}"}]
    body = {"errors": errors}
    request.response.status = 400
    return body


@exception_view_config(Exception, renderer="json")
def exception_cqrs_catch_all(exc, request):
    """Catch-all exceptions and show user friendly message.

    Safegaurds the service from leaking technical details.

    :param exc: raised exception
    :type exc: Exception
    :param request: request
    :type request: request
    :return: error message
    :rtype: dict
    """
    logging.getLogger(__name__).error(exc, exc_info=True)

    errors = [
        {
            "title": "The server encountered an internal error and was unable to complete your request."
        }
    ]
    body = {"errors": errors}

    request.response.status = 500
    return body
