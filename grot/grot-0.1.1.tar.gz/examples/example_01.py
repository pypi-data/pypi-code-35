import os


def example_01():
    """
        # Hello Grot
        To generate a graph you need to import Grot class, create its instance and
        define nodes and edges. While `g.edge()` call, you can pass unlimited
        number of nodes or plain strings (creates implicit node).

        If you don't connect given node (as `unconnected`) it's going to float somewhere around.
    """
    from grot import Grot

    this_dir_path = os.path.dirname(__file__)  # if run in console - remove 'directory' parameter below
    out_dir_path = os.path.join(this_dir_path, 'out')

    g = Grot(name='example_01', format='png', directory=out_dir_path, graph_attrs={"rankdir": "LR"})

    one = g.node("It is\neaiser")
    two = g.node("graphs", color="#8a9bac")
    ignored = g.node("Node floats when\nunconnected", color="#da3080")

    g.edge(one, "to define", two)
    g.render()

    # example ends here
    assert g.source == r"""digraph example_01 {
	graph [fontname=helvetica nodesep=0.5 rankdir=LR ranksep=0.5 sep=0.4]
	node [color="#13136c" fontname=helvetica penwidth=1.8 shape=box]
	edge [fontname=helvetica]
	n_a [label="It is\neaiser"]
	n_f [label=graphs color="#8a9bac"]
	n_3 [label="Node floats when\nunconnected" color="#da3080"]
	n_d [label="to define" shape=none]
	n_a -> n_d
	n_d -> n_f
}"""
