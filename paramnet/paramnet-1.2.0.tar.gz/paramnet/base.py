from collections import OrderedDict

import networkx as nx

from paramnet.dict import NodeDict, AdjlistOuterDict
from paramnet.exceptions import ParametrizedNetworkError, FieldConflictError, \
    NodeParameterError, EdgeParameterError
from paramnet.util import node_param_property, edge_param_property

__all__ = []
__all__.extend([
    'Parametrized'
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


class Parametrized(object):
    _node_params = []
    _edge_params = []

    node_dict_factory = OrderedDict

    _node = NodeDict()
    _adj = AdjlistOuterDict()
    _pred = AdjlistOuterDict()

    def __init_subclass__(cls, node_params=None, edge_params=None,
                          is_abstract=False, **kwargs):
        super().__init_subclass__(**kwargs)

        if is_abstract:
            return

        if node_params is None:
            node_params = []
        if edge_params is None:
            edge_params = []
        cls._node_params = list(node_params)
        cls._edge_params = list(edge_params)

        if issubclass(cls, nx.Graph):
            Parametrized._wrap_adders(cls)
            Parametrized._add_param_fields(cls)

        if not issubclass(cls, nx.DiGraph):
            cls._pred = None

    @staticmethod
    def _wrap_adders(cls):
        for method in _add_methods:
            setattr(cls, method, verify_add(getattr(cls, method)))

    @staticmethod
    def _add_param_fields(cls):
        # adjacency matrix
        setattr(cls, "A", edge_param_property("weight", default=1.0))
        for field in cls._node_params:
            if hasattr(cls, field):
                raise FieldConflictError(
                    f"Trying to overwrite existing field {field} for class "
                    f"{cls.__name__}.")
            setattr(cls, field, node_param_property(field))
        for field in cls._edge_params:
            if field == 'weight':
                continue
            if hasattr(cls, field):
                raise FieldConflictError(
                    f"Trying to overwrite existing field {field} for class "
                    f"{cls.__name__}.")
            setattr(cls, field, edge_param_property(field))

    def index(self, node):
        try:
            return list(self._node.keys()).index(node)
        except ValueError:
            raise nx.NetworkXError(f"The node {node} is not in the graph.")

    @property
    def node_params(self):
        return self._node_params

    @property
    def edge_params(self):
        return self._edge_params
