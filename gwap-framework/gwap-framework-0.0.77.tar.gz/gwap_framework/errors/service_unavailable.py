from gwap_framework.errors.base import BaseError


class ServiceUnavailableError(BaseError):
    """
        ServiceUnavailableException are dispatch when requests is not completed by any reason
    """

    def __init__(self, message='Sttempt to communicate with service failed'):
        BaseError.__init__(self)
        self.code = 503
        self.message = message
        self.status = 'service_unavailable'
