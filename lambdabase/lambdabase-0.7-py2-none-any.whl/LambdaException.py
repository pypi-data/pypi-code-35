from lambdabase.Response import Response


class LambdaException(StandardError, Response):
    def __init__(self, message, code):
        super(LambdaException, self).__init__(message)
        self.code = code

    def build(self):
        self.body.update({"message": self.message})
        response = super(LambdaException, self).build()
        return response


class ResourceNotFound(LambdaException):
    def __init__(self, message):
        super(ResourceNotFound, self).__init__(message, 404)


class BadRequestException(LambdaException):
    def __init__(self, message):
        super(BadRequestException, self).__init__(message, 400)


class RemoteCallException(LambdaException):
    def __init__(self, message):
        super(RemoteCallException, self).__init__(message, 500)


class UnauthorisedException(LambdaException):
    def __init__(self, message):
        super(UnauthorisedException, self).__init__(message, 401)


class ForbiddenException(LambdaException):
    def __init__(self, message):
        super(ForbiddenException, self).__init__(message, 403)


class OptimisticLockException(StandardError):
    def __init__(self, expected, actual):
        super(OptimisticLockException, self).__init__('Lock version error. Expected: {}, Actual: {}'
                                                      .format(expected, actual))
        self.expected = expected
        self.actual = actual

