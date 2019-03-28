from . import BaseRest_RequestHandler, PathTreeRestRouter

class PathTreeRest_RequestHandler(BaseRest_RequestHandler):
    in_request_router_class = PathTreeRestRouter
