from . import BaseRest_RequestHandler, RegexpRestRouter

class RegexpRest_RequestHandler(BaseRest_RequestHandler):
    in_request_router_class = RegexpRestRouter
