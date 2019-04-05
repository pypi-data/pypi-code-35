from importlib import import_module

from falcon import API

from falcon_core.config import settings

from falcon_core.utils import load_middleware, flatten


def get_wsgi_application():

    middleware = [load_middleware(m) for m in settings.MIDDLEWARE]

    application = API(middleware=middleware)

    for k, v in settings.ROUTER_CONVERTERS:
        application.router_options.converters[k] = v

    for route in flatten(import_module(settings.ROUTES).routes):
        application.add_route(route.template_uri, route.resource, *route.args, **route.kwargs)

    return application
