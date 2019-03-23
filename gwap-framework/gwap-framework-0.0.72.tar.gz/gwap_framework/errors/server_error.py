from gwap_framework.errors.base import BaseError


class ServerError(BaseError):

    def __init__(self, message='Internal server error'):
        BaseError.__init__(self)
        self.code = 500
        self.message = message
        self.status = 'server_error'
