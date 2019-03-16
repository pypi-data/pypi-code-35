from paramnet.view import NodeParamView, EdgeParamView

__all__ = []

__all__.extend([
    'node_param_property',
    'edge_param_property'
])


def node_param_property(param_name, default=None):
    def get(self):
        return NodeParamView(self, param_name, default=default)

    return property(get)


def edge_param_property(param_name, default=None):
    def get(self):
        return EdgeParamView(self, param_name, default=default)

    return property(get)
