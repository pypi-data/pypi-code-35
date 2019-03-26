class WebhookError(Exception):
    pass


class DoesNotExist(WebhookError):
    pass


class RequestError(WebhookError):
    pass


class ConfigurationError(Exception):
    pass


class AlreadyRegistered(ConfigurationError):
    pass
