class AppNotDefined(Exception):
    """All routes will fail if app is not defined"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class HttpMethodConflict(Exception):
    """Defined HTTP methods with defined function once"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
