class AppSecurityControllerError(Exception):
    message = None

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class StandardControllerError(Exception):
    code_error = None
    message = None

    def __init__(self, message, code_error):
        self.message = str(message)
        self.code_error = code_error
        super().__init__(message, code_error)


class AttributeControllerError(Exception):
    code_error = None
    message = None

    def __init__(self, message, code_error):
        self.message = str(message)
        self.code_error = code_error
        super().__init__(message, code_error)
