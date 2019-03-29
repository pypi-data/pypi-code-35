"""Provide custom errors with additional detail"""

class ErrorBase(Exception):
    """Base Exception for common errors"""

    default_message = 'Unspecified error'

    def __init__(self, msg=None):
        self._msg = msg or self.default_message

    def __str__(self):
        return self._msg.format(**self.__dict__)


class ResourceError(ErrorBase):
    """Base class for errors that refer to a specific resource"""

    default_message = 'Resource error on "{path}"'

    def __init__(self, path, msg=None, exc=None):
        super(ResourceError, self).__init__(msg)
        self.path = path
        self.exc = exc


class ResourceNotFound(ResourceError):
    """Indicates that a resource or file could not be found"""

    default_message = 'Could not find resource "{path}"'


class PermissionError(ResourceError):
    """Indicates that caller has insufficient permissions for this resource"""

    default_message = 'Insufficient permissions for "{path}"'


class OperationFailed(ErrorBase):
    """Indicates that an operation failed"""

    default_message = 'Operation failed, {details}'

    def __init__(self, msg=None, exc=None):
        super(OperationFailed, self).__init__(msg)
        self.exc = exc
        self.details = '' if exc is None else str(exc)


class RemoteConnectionError(OperationFailed):
    """Indicates that a connection error occurred."""

    default_message = 'Remote connection error, {details}'
