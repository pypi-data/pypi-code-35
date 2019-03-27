class ConfigParserCryptException(Exception):
    def __init__(self, message, Errors=[]):
        Exception.__init__(self, message)
        self.Errors = Errors

class ReadOnlyConfigError(ConfigParserCryptException):
    pass
