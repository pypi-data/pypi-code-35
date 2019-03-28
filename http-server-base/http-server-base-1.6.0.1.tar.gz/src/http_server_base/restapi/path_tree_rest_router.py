from . import BaseInRequestRouter
from http_server_base.tools import PrefixTreeMap, PathTreeMap

class PathTreeRestRouter(BaseInRequestRouter):
    mapper_type = PathTreeMap
