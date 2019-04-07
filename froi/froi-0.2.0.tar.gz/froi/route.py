from flask import request

class MethodSwitch:
    def __init__(self):
        self.get = False
        self.post = False
        self.put = False
        self.delete = False
        self.options = False
        self.header = False

class Route:
    """
    Consolidate all route logic into one logic.

    The goal is to be able to define an object :Route: that will
    handle endpoints on multiple methods.
    """

    isblank = MethodSwitch()
    def __init__(self):
        pass

    def _setmethod(self, methods, method):
        if not getattr(self.isblank, method.lower()):
            methods += [method]

    def getmethods(self):
        methods = []
        for m in ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEADER']:
            self._setmethod(methods, m)
        return methods

    def get(self):
        self.isblank.get = True
        pass

    def post(self):
        self.isblank.post = True
        pass

    def put(self):
        self.isblank.put = True
        pass

    def delete(self):
        self.isblank.delete = True
        pass

    def options(self):
        self.isblank.options = True
        pass

    def header(self):
        self.isblank.header = True
        pass

    def sethttp(self):
        method = request.method
        if method and not getattr(self.isblank, method):
            outbound_fxn = getattr(self, method)
            outbound_fxn()
