import networkx as nx
import numpy as np
import pytest

from paramnet import Parametrized
from paramnet.exceptions import NodeParameterError, EdgeParameterError, \
    FieldConflictError

all_graph_types = [nx.Graph, nx.DiGraph]


def test_mixin_standalone():
    class A(Parametrized):
        pass

    with pytest.raises(TypeError):
        A()


@pytest.mark.parametrize("graph_cls", all_graph_types)
def test_add_node(graph_cls):
    class A(Parametrized, graph_cls):
        _node_params = ['a', 'b']

    G = A()
    with pytest.raises(NodeParameterError):
        G.add_node(0)

    with pytest.raises(NodeParameterError):
        G.add_node(0, a=1)

    with pytest.raises(NodeParameterError):
        G.add_node(0, b=2)

    G.add_node(0, a=1, b=2)

    with pytest.raises(NodeParameterError):
        G.add_nodes_from(range(1, 5))

    with pytest.raises(NodeParameterError):
        G.add_nodes_from(range(1, 5), a=10)

    with pytest.raises(NodeParameterError):
        G.add_nodes_from(range(1, 5), b=20)

    G.add_nodes_from(range(1, 5), a=10, b=20)


@pytest.mark.parametrize("graph_cls", all_graph_types)
def test_add_edge(graph_cls):
    class A(Parametrized, graph_cls):
        _node_params = ['a']
        _edge_params = ['x', 'y']

    G = A()
    with pytest.raises(NodeParameterError):
        G.add_edge(0, 1, x=2, y=3)

    assert G.size() == 0
    assert len(G) == 0

    G.add_nodes_from(range(5), a=1)

    with pytest.raises(EdgeParameterError):
        G.add_edge(0, 1)

    with pytest.raises(EdgeParameterError):
        G.add_edge(0, 1, x=2)

    with pytest.raises(EdgeParameterError):
        G.add_edge(0, 1, y=3)

    G.add_edge(0, 1, x=2, y=3)
    G.remove_edge(0, 1)

    with pytest.raises(EdgeParameterError):
        G.add_edges_from([(0, 1), (1, 2)])

    with pytest.raises(EdgeParameterError):
        G.add_edges_from([(0, 1), (1, 2)], x=2)

    with pytest.raises(EdgeParameterError):
        G.add_edges_from([(0, 1), (1, 2)], y=3)

    G.add_edges_from([(0, 1), (1, 2)], x=2, y=3)

    with pytest.raises(EdgeParameterError):
        G.add_cycle(range(5))

    with pytest.raises(EdgeParameterError):
        G.add_cycle(range(5), x=2)

    with pytest.raises(EdgeParameterError):
        G.add_cycle(range(5), y=3)

    G.add_cycle(range(5), x=2, y=3)


@pytest.mark.parametrize("graph_cls", all_graph_types)
def test_node_order_and_index(graph_cls):
    class A(Parametrized, graph_cls):
        pass

    G = A()
    nodes = ['z', 1, (2, 3)]
    G.add_nodes_from(nodes)
    for i, node in enumerate(nodes):
        assert G.index(node) == i

    node = nodes.pop(1)
    G.remove_node(node)
    for i, node in enumerate(nodes):
        assert G.index(node) == i

    with pytest.raises(nx.NetworkXError):
        G.index('non-existent-node')


@pytest.mark.parametrize("graph_cls", all_graph_types)
def test_fields(graph_cls):
    with pytest.raises(FieldConflictError):
        class A(Parametrized, graph_cls):
            _node_params = ['add_node']

    with pytest.raises(FieldConflictError):
        class A(Parametrized, graph_cls):
            _edge_params = ['__dict__']

    with pytest.raises(FieldConflictError):
        class A(Parametrized, graph_cls):
            _edge_params = ['x']
            _node_params = ['x']

    class A(Parametrized, graph_cls):
        _node_params = ['r']
        _edge_params = ['w']

    G = A()

    assert hasattr(G, 'r')
    assert hasattr(G, 'w')

    G.add_node(0, r=300.0)
    G.add_node(1, r=49.0)
    G.add_node(2, r=15.0)

    assert np.allclose(G.r, np.array([300.0, 49.0, 15.0]))

    G.add_edge(0, 1, w=1)
    G.add_edge(2, 0, w=-10)
    G.add_edge(1, 1, w=2.0)
    w = G.w
    if G.is_directed():
        assert np.allclose(w, np.array([[0, 1, 0],
                                        [0, 2.0, 0],
                                        [-10, 0, 0]]))
    else:
        assert np.allclose(w, np.array([[0, 1, -10],
                                        [1, 2.0, 0],
                                        [-10, 0, 0]]))


@pytest.mark.parametrize("graph_cls", all_graph_types)
def test_adj(graph_cls):
    class A(Parametrized, graph_cls):
        pass

    G = A()
    G.add_nodes_from(range(3))

    G.add_edge(0, 1, weight=1.0)
    G.add_edge(1, 2, weight=-2.0)
    G.add_edge(2, 0, weight=0.001)

    if G.is_directed():
        assert np.allclose(G.A, np.array([[0, 1, 0],
                                          [0, 0, -2],
                                          [0.001, 0, 0]]))
    else:
        assert np.allclose(G.A, np.array([[0, 1, 0.001],
                                          [1, 0, -2],
                                          [0.001, -2, 0]]))
