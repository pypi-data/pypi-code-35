from gwap_framework.errors.base import BaseError


class NotFoundError(BaseError):
    """
        NotFoundException are dispatch when requests is not authenticated
    """

    def __init__(self, message='The resource could not be found.'):
        BaseError.__init__(self)
        self.code = 404
        self.message = message
        self.status = 'not_found'
