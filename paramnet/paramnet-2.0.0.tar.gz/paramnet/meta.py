from collections import OrderedDict

import networkx as nx

from paramnet.exceptions import FieldConflictError
from paramnet.view import NodeParamView, EdgeParamView

__all__ = []
__all__.extend([
    'ParametrizedMeta'
])


class ParametrizedMeta(type):

    def __new__(mcs, name, bases, attrs, node_params=None, edge_params=None,
                *args, **kwargs):
        return super().__new__(mcs, name, bases, attrs, *args, **kwargs)

    def __init__(cls, name, bases, attrs, node_params=None, edge_params=None,
                 *args, **kwargs):
        super().__init__(name, bases, attrs, *args, **kwargs)

        if node_params is None:
            node_params = []
        if edge_params is None:
            edge_params = []

        cls._node_params = tuple(node_params)
        cls._edge_params = tuple(edge_params)

        cls.node_dict_factory = OrderedDict

    def __call__(cls, *args, **kwargs):
        if not issubclass(cls, nx.Graph):
            raise TypeError("Can't parametrize a non-graph class.")

        obj = super().__call__(*args, **kwargs)

        # add descriptors for param access

        # adjacency matrix
        setattr(obj, "A", EdgeParamView("weight", obj, default=1.0))

        for field in obj._node_params:
            if hasattr(obj, field):
                raise FieldConflictError(
                    f"Trying to overwrite existing field {field} for class "
                    f"{cls.__name__}.")
            setattr(obj, field, NodeParamView(field, obj))

        for field in obj._edge_params:
            if field == 'weight':
                continue
            if hasattr(obj, field):
                raise FieldConflictError(
                    f"Trying to overwrite existing field {field} for class "
                    f"{cls.__name__}.")
            setattr(obj, field, EdgeParamView(field, obj))

        return obj
