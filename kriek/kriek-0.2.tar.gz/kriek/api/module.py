from collections import defaultdict

class Module:
    routes = defaultdict(dict)

    def __init__(self, api, name, prefix="/", doc=True):
        self.api = api
        self.name = name
        self.prefix = prefix

    def route(self, uri, methods=['GET']):
        def decorator(func):
            self.api.add_route(uri, func, methods=methods)
        return decorator

    def add_route(self, uri, func, methods=['GET']):
        for method in methods:
            self.api.routes[uri][method] = func
        