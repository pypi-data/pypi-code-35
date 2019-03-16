import networkx as nx
import numpy as np
import pytest

from paramnet import Parametrized
from paramnet.exceptions import NodeParameterError, EdgeParameterError, \
    FieldConflictError

all_graph_types = [nx.Graph, nx.DiGraph]


@pytest.mark.parametrize("graph_cls", all_graph_types)
def test_add_node(graph_cls):
    class A(Parametrized, graph_cls, node_params=['a', 'b']):
        pass

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
    class A(Parametrized, graph_cls,
            node_params=['a'], edge_params=['x', 'y']):
        pass

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
        class A(Parametrized, graph_cls,
                node_params=['add_node']):
            pass

    with pytest.raises(FieldConflictError):
        class A(Parametrized, graph_cls,
                edge_params=['__dict__']):
            pass

    with pytest.raises(FieldConflictError):
        class A(Parametrized, graph_cls,
                node_params=['x'],
                edge_params=['x']):
            pass

    class A(Parametrized, graph_cls,
            node_params=['r'],
            edge_params=['w']):
        pass

    G = A()

    assert hasattr(G, 'r')
    assert hasattr(G, 'w')

    G.add_node("a", r=300.0)
    G.add_node("b", r=49.0)
    G.add_node("c", r=15.0)

    assert G.r["a"] == 300.0
    assert G.r["b"] == 49.0
    assert G.r["c"] == 15.0

    # assignment
    G.r["a"] = 299.0

    assert np.allclose(G.r, np.array([299.0, 49.0, 15.0]))
    assert len(G.r) == 3
    assert G.r.shape == (3,)
    assert np.allclose(G.r + np.ones(3), np.array([300, 50, 16]))
    assert np.allclose(G.r * np.ones(3), G.r)
    assert np.allclose(G.r - G.r, np.zeros(3))

    G.add_edge("a", "b", w=1)
    G.add_edge("c", "a", w=-10)
    G.add_edge("b", "b", w=2.0)

    assert len(G.w) == 3
    assert G.w.shape == (3, 3)
    if G.is_directed():
        assert np.allclose(G.w, np.array([[0, 1, 0],
                                          [0, 2.0, 0],
                                          [-10, 0, 0]]))
    else:
        assert np.allclose(G.w, np.array([[0, 1, -10],
                                          [1, 2.0, 0],
                                          [-10, 0, 0]]))

    assert np.allclose(G.w @ np.ones(3), np.sum(G.w, axis=1))
    if G.is_directed():
        assert np.sum(G.w != 0) == 3
    else:
        assert np.sum(G.w != 0) == 5
    assert np.allclose(G.w - G.w, np.zeros(G.w.shape))

    # assignment
    G.w["c", "a"] = 100.0
    assert G.w["c", "a"] == 100.0
    if not G.is_directed():
        assert G.w["a", "c"] == 100.0


@pytest.mark.parametrize("graph_cls", all_graph_types)
def test_adj(graph_cls):
    class A(Parametrized, graph_cls):
        pass

    G = A()
    G.add_nodes_from(range(3))

    G.add_edge(0, 1)
    G.add_edge(1, 2, weight=-2.0)
    G.add_edge(2, 0, weight=0.001)

    assert G.A[0, 1] == 1
    assert G.A[1, 2] == -2
    assert G.A[2, 0] == 0.001

    # test full matrix and inverse
    if G.is_directed():
        assert np.allclose(G.A, np.array([[0, 1, 0],
                                          [0, 0, -2],
                                          [0.001, 0, 0]]))
    else:
        assert np.allclose(G.A, np.array([[0, 1, 0.001],
                                          [1, 0, -2],
                                          [0.001, -2, 0]]))

    assert np.allclose(G.A, nx.adjacency_matrix(G).todense())

    G = A()
    G.add_star(range(10))
    one = np.ones_like(G)

    if G.is_directed():
        d_out = [G.out_degree(x) for x in G]
        d_in = [G.in_degree(x) for x in G]
        assert np.allclose(d_out, np.dot(G.A, one))
        assert np.allclose(d_in, one.T @ G.A)
    else:
        d = [G.degree(x) for x in G]
        assert np.allclose(d, G.A @ one)
