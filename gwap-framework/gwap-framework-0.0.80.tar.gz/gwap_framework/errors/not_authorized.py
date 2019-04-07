from gwap_framework.errors.base import BaseError


class NotAuthorizedError(BaseError):
    """
        NotAuthorizedException are dispatch when requests is not authenticated
    """

    def __init__(self, message='You are not authorized for this request.'):
        BaseError.__init__(self)
        self.code = 401
        self.message = message
        self.status = 'unauthorized'
