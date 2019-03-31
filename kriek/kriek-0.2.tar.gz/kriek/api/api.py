import json
from .response import Response, JSON
from .module import Module
from .abort import abort
from .exceptions import AbortException
from collections import defaultdict
from .constants import HTTP_CODE_MEANING

class Api:
    modules = {}
    routes = defaultdict(dict)

    def __init__(self, version="0.1"):
        self.version = version

    def module(self, name, prefix='/', doc=True):
        existing = self.modules.get(name)
        if existing:
            return existing
        else:
            new_module = Module(self, name, prefix, doc=doc)
            self.modules[name] = new_module
            return new_module

    def route(self, uri, methods=['GET']):
        def decorator(func):
            self.add_route(uri, func, methods=methods)
        return decorator

    def add_route(self, uri, func, methods=['GET']):
        for method in methods:
            print(uri, func, methods)
            self.routes[uri][method] = func

    def __call__(self, environ, start_response):
        # make response
        try:
            resource = self.routes.get(environ['RAW_URI'])
            if resource:
                function = resource.get(environ['REQUEST_METHOD'])
                if function:
                    result = function()
                    resp = result if issubclass(type(result), Response) else (
                        JSON(*result) if type(result)==tuple else JSON(result)
                    )
                else:
                    abort(405)
            else:
                abort(404)
        except AbortException as e:
            resp = e.response
        # send result
        start_response("%s %s"%(resp.status_code, HTTP_CODE_MEANING[resp.status_code]), resp.headers)
        yield resp.data

    def run(self, host='localhost', port=5000, debug=False):
        from werkzeug import run_simple
        run_simple(host, port, self, use_reloader=debug)
