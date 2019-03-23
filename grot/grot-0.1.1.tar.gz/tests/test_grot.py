import pytest

from grot import Grot


@pytest.fixture
def default_graph():
    class PG(Grot):
        pass

    return PG


@pytest.fixture
def plain_graph_class():
    class Plain(Grot):
        _default_graph_attrs = {}
        _default_node_attrs = {}
        _default_edge_attrs = {}

    return Plain


@pytest.fixture
def gph(plain_graph_class):
    return plain_graph_class(__file__)


def test_plain_with_attributes(plain_graph_class):
    g = plain_graph_class(__file__, graph_attrs={'color': '#caffee'}, edge_attrs={'penwidth': '1.1'})
    assert g.source == r"""digraph test_grot {
	graph [color="#caffee"]
	edge [penwidth=1.1]
}"""


def test_default_attribute_canceling(default_graph):
    g = default_graph(
        __file__,
        graph_attrs={'color': '#caffee'},
        node_attrs={'color': None, 'shape': None},
        edge_attrs={'fontname': None, 'penwidth': '1.1'}
    )
    assert g.source == r"""digraph test_grot {
	graph [color="#caffee" fontname=helvetica nodesep=0.5 ranksep=0.5 sep=0.4]
	node [fontname=helvetica penwidth=1.8]
	edge [penwidth=1.1]
}"""


def test_basic(default_graph):
    g = default_graph(__file__)
    phy_br = g.node("node\nwith\nlinebreaks", shape="note")
    phy_br.edge("a target")
    target_2 = g.node("explicit target", shape="box3d")
    phy_br.edge(target_2, "plain\nnode", color="#123456")

    assert g.source == r"""digraph test_grot {
	graph [fontname=helvetica nodesep=0.5 ranksep=0.5 sep=0.4]
	node [color="#13136c" fontname=helvetica penwidth=1.8 shape=box]
	edge [fontname=helvetica]
	n_5 [label="node\nwith\nlinebreaks" shape=note]
	n_a [label="a target" shape=none]
	n_5 -> n_a
	n_0 [label="explicit target" shape=box3d]
	n_4 [label="plain\nnode" shape=none]
	n_5 -> n_0 [color="#123456"]
	n_0 -> n_4 [color="#123456"]
}"""


def test_empty_subgraph(gph):
    with gph.subgraph(name="thing"):
        pass

    assert gph.source == """\
digraph test_grot {
	subgraph cluster_thing {
	}
}"""


def test_subgraph_node(gph):
    with gph.subgraph() as c0:
        c0.node('one')
        c0.node('two')
    gph.node('three')

    assert gph.source == """\
digraph test_grot {
	subgraph cluster_0 {
		n_f [label=one]
		n_a [label=two]
	}
	n_b [label=three]
}"""


def test_subgraph_edge_inside_host(gph):
    with gph.subgraph() as c0:
        one = c0.node('one')
        two = c0.node('two')
        one.edge(two)

    assert str(gph) == """\
digraph test_grot {
	subgraph cluster_0 {
		n_f [label=one]
		n_a [label=two]
		n_f -> n_a
	}
}"""


def test_subgraph_aux_edge(gph):
    with gph.subgraph() as c0:
        one = c0.node('one')
        two = c0.node('two', shape="box")
    gph.edge(one, two, 'three', 'four', penwidth='1.2')

    assert gph.source == """\
digraph test_grot {
	subgraph cluster_0 {
		n_f [label=one]
		n_e [label=two shape=box]
	}
	n_c [label=three shape=none]
	n_b [label=four shape=none]
	n_f -> n_e [penwidth=1.2]
	n_e -> n_c [penwidth=1.2]
	n_c -> n_b [penwidth=1.2]
}"""


@pytest.mark.parametrize("option", ['node', 'edge', 'subgraph'])
def test_subgraph_forbidden_making_edges(gph, option):
    with gph.subgraph() as c0:
        one = c0.node('one')

    message = r"This graph object named 'cluster_0' \('Plain' type\) has been finalized already."
    with pytest.raises(ValueError, match=message):
        if option == 'node':
            c0.node('one')
        elif option == 'edge':
            one.edge('two')
        else:
            with c0.subgraph():
                pass


@pytest.mark.parametrize("option", ["in", "aux"])
def test_edges_with_labels(option, gph):
    one = gph.node("one")
    two = gph.node("two")
    five = gph.node("five")

    if option == "aux":
        one.edge(("1-2", two), "three", ('2-3', "four"), five)
    else:
        gph.edge(one, ("1-2", two), "three", ('2-3', "four"), five)

    expected_result = r"""digraph test_grot {
	n_f [label=one]
	n_a [label=two]
	n_4 [label=five]
	n_c [label=three shape=none]
	n_b [label=four shape=none]
	n_f -> n_a [label="1-2"]
	n_a -> n_c
	n_c -> n_b [label="2-3"]
	n_b -> n_4
}"""

    assert str(gph) == expected_result


def test_first_node_in_edge_cannot_have_label(gph):
    with pytest.raises(ValueError, match="First edge in a chain cannot have a transition label."):
        gph.edge(("forbidden label", 'one'), 'two')
