
class KriekException(Exception):
    pass

class AbortException(KriekException):
    def __init__(self, resp):
        self.response = resp
