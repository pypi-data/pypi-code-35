
from enum import Enum
from configpp.tree import Tree, Settings, DatabaseLeaf, PythonLoggerLeaf, NodeBase
from configpp.soil import Config
from voluptuous import Any

from .auth import backends

backend_names = [b.OAUTH_NAME for b in backends]

tree = Tree(Settings(convert_underscores_to_hypens = True, convert_camel_case_to_hypens = True))


class OAuthConfig(NodeBase):

    id = str
    secret = str

    def serialize(self):
        return self.__dict__

class Mode(Enum):

    DEVELOPMENT = 'development'
    PRODUCTION = 'production'

@tree.root()
class PabuConfig():

    database = DatabaseLeaf

    auth = tree.dict_node(Any(*backend_names), OAuthConfig)

    mode = Mode

    logger = dict

def load() -> PabuConfig:
    config_loader = Config('pabu.yaml')

    if not config_loader.load():
        return None

    return tree.load(config_loader.data)
