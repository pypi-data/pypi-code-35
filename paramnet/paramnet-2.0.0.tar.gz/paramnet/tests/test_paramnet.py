import networkx as nx
import numpy as np
import pytest

from paramnet import Parametrized
from paramnet.exceptions import FieldConflictError

all_graph_types = [nx.Graph, nx.DiGraph]


def test_abc():
    class A(Parametrized):
        pass

    with pytest.raises(TypeError):
        A()


@pytest.mark.parametrize("graph_cls", all_graph_types)
def test_missing_params(graph_cls):
    class A(Parametrized, graph_cls, node_params=['x'], edge_params=['y']):
        pass

    G = A()
    G.add_node(0)
    G.add_node(1, x=2)

    assert G.x.dtype == np.dtype('float64')
    assert np.isnan(G.x[0])
    assert G.x[1] == 2.0

    G.add_edge(0, 0, y=0.78)
    G.add_edge(0, 1)

    assert G.y.dtype == np.dtype('float64')
    assert np.isnan(G.y[0, 1])
    assert G.y[0, 0] == 0.78


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

        A()

    with pytest.raises(FieldConflictError):
        class A(Parametrized, graph_cls,
                edge_params=['__dict__']):
            pass

        A()

    with pytest.raises(FieldConflictError):
        class A(Parametrized, graph_cls,
                node_params=['x'],
                edge_params=['x']):
            pass

        A()

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

    # fancy indexing
    assert np.allclose(G.r[["b", "a"]], np.array([49.0, 299.0]))

    G.add_edge("a", "b", w=1.0)
    G.add_edge("c", "a", w=-10.0)
    G.add_edge("b", "b", w=2.0)

    assert len(G.w) == 3
    assert G.w.shape == (3, 3)
    if G.is_directed():
        assert np.allclose(G.w, np.array([[0, 1.0, 0],
                                          [0, 2.0, 0],
                                          [-10, 0, 0]]))
    else:
        assert np.allclose(G.w, np.array([[0, 1.0, -10.0],
                                          [1.0, 2.0, 0],
                                          [-10.0, 0, 0]]))

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

    # fancy indexing
    assert np.allclose(G.w[[("c", "a"), ("a", "b")]], np.array([100.0, 1.0]))


@pytest.mark.parametrize("graph_cls", all_graph_types)
def test_vector_assignment(graph_cls):
    class A(Parametrized, graph_cls,
            node_params=['r'],
            edge_params=['w']):
        pass

    G = A()
    G.add_node(0, r=1.0)
    G.add_node(1, r=2.0)
    G.add_node(2, r=3.0)
    G.add_edge(0, 1, w=10.0)
    G.add_edge(2, 0, w=20.0)

    # scalar assignment
    G.r = 3.0
    assert G.r[0] == 3.0
    assert G.r[1] == 3.0

    # vector assignment
    G.r = [4.0, 5.0, 6.0]
    assert np.allclose(G.r, np.array([4.0, 5.0, 6.0]))

    # scalar assignment
    G.w = 100.0
    assert G.w[0, 1] == 100.0
    assert G.w[2, 0] == 100.0

    # array assignment
    if G.is_directed():
        G.w = np.array([[0.0, 5.0, 0.0],
                        [0.0, 0.0, 0.0],
                        [-0.1, 0.0, 0.0]])
        assert G.w[0, 1] == 5.0
        assert G.w[2, 0] == -0.1
    else:
        with pytest.raises(ValueError):
            G.w = np.array([[0.0, 5.0, -0.1],
                            [5.0, 0.0, 0.0],
                            [-0.1, 3.0, 0.0]])

        G.w = np.array([[0.0, 5.0, -0.1],
                        [5.0, 0.0, 0.0],
                        [-0.1, 0.0, 0.0]])
        assert G.w[0, 1] == 5.0
        assert G.w[1, 0] == 5.0
        assert G.w[0, 2] == -0.1
        assert G.w[2, 0] == -0.1


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
