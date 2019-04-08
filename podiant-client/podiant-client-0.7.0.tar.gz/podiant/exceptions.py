class ConfigurationError(Exception):
    pass


class ClientError(Exception):
    pass


class UnauthorizedError(ClientError):
    pass


class UnprocessableEntityError(ClientError):
    pass


class BadRequestError(ClientError):
    pass


class ForbiddenError(ClientError):
    pass


class NotFoundError(ClientError):
    pass


class MethodNotAllowedError(ClientError):
    pass


class NotAcceptableError(ClientError):
    pass


class ConflictError(ClientError):
    pass


class UnsupportedMediaTypeError(ClientError):
    pass


class ServerError(Exception):
    pass


class InternalServerError(ServerError):
    pass


class BadResponseError(ServerError):
    pass


class UnknownError(ServerError):
    pass
