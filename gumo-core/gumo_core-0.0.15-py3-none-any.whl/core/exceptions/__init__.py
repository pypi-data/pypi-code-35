class GumoBaseError(RuntimeError):
    pass


class ConfigurationError(GumoBaseError):
    pass


class ObjectNotoFoundError(GumoBaseError):
    pass
