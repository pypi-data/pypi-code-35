from collections import OrderedDict

import networkx as nx

from paramnet.exceptions import ParametrizedNetworkError, FieldConflictError, \
    NodeParameterError, EdgeParameterError
from paramnet.view import NodeParamView, EdgeParamView

__all__ = []
__all__.extend([
    'ParametrizedMeta'
])

_add_methods = ['add_node', 'add_nodes_from', 'add_edge', 'add_edges_from',
                'add_weighted_edges_from']


def verify_add(method):
    """ wrapper to check all node/edge additions have required parameters and
    rollback if not

    Checking is done by casting the attr dicts for any new nodes/edges as
    the appropriate AttrDict subclass in this module, which enforces required
    keys. Cleanest general solution, since (i) nx.add_node/edge* methods accept
    different input types and (ii) they don't consistently use
    node(edge)_attr_dict_factory to create new attr dicts. """

    def wrapped(self, *args, **kwargs):
        old_nodes = set(self.nodes())
        old_edges = set(self.edges())

        method(self, *args, **kwargs)

        new_nodes = self.nodes() - old_nodes
        new_edges = self.edges() - old_edges
        try:
            for new_node in new_nodes:
                if not self._node[new_node].has_all_attrs():
                    raise NodeParameterError(
                        f"Tried to add node {new_node} without all required "
                        f"parameters: {self._node_params}"
                    )
            for new_edge in new_edges:
                u, v = new_edge
                if not self._adj[u][v].has_all_attrs():
                    raise EdgeParameterError(
                        f"Tried to add edge {(u, v)} "
                        f"without all required parameters: {self._edge_params}"
                    )
        except ParametrizedNetworkError as err:
            # rollback
            self.remove_nodes_from(new_nodes)
            self.remove_edges_from(new_edges)
            raise err

    return wrapped


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

        if not issubclass(cls, nx.DiGraph) and hasattr(cls, '_pred'):
            del cls._pred

        # wrap node/edge addition methods to enforce parameters
        if issubclass(cls, nx.Graph):
            for method in _add_methods:
                setattr(cls, method, verify_add(getattr(cls, method)))

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
