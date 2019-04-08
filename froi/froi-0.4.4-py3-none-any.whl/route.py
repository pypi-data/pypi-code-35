from flask import request

class Route:
    """
    Consolidate all route logic into one logic.

    The goal is to be able to define an object :Route: that will
    handle endpoints on multiple methods.
    """

    def __init__(self):
        pass

    def _setmethod(self, methods, method):
        if hasattr(self, method.lower()):
            methods += [method]

    def getmethods(self):
        if self.method is not None and self.method != []:
            return self.method

        methods = []
        for m in ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEADER']:
            self._setmethod(methods, m)
        return methods

    def sethttp(self):
        method = request.method
        if method and hasattr(self, method.lower()):
            outbound_fxn = getattr(self, method.lower())
            return outbound_fxn()
