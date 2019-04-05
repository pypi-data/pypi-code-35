from importlib import import_module

from falcon_core.utils import flatten


class RouteError(ValueError):
    pass


class Route:
    def __init__(self, template_uri, resource, *args, **kwargs):
        if template_uri.startswith('/') and template_uri.endswith('/'):
            self.template_uri = template_uri
            self.resource = resource
            self.args = args
            self.kwargs = kwargs
        else:
            raise RouteError(f'Route template_uri \'{template_uri}\' is not valid.')


def route(*args, **kwargs):
    ri = Route(*args, **kwargs)
    if isinstance(ri.resource, list):
        ri.resource = flatten(ri.resource)
        for r in ri.resource:
            r.template_uri = f'{ri.template_uri[:-1]}{r.template_uri}'
        return ri.resource
    return ri


def include(routes):
    if isinstance(routes, str):
        return import_module(routes).routes
    return routes
