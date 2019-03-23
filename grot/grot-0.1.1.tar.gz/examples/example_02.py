import os


def example_02a():
    """
        # Branches

        One call of `g.edge(node1, node2, node3, ...)` creates single chain of arrows.
        To make a branch, you need to call `g.edge` once again.
    """
    from grot import Grot

    this_dir_path = os.path.dirname(__file__)  # if run in console - remove 'directory' parameter below
    out_dir_path = os.path.join(this_dir_path, 'out')
    g = Grot(name='example_02a', format='png', directory=out_dir_path, graph_attrs={"rankdir": "LR"})

    one = g.node("One")
    two = g.node("Two")
    three = g.node("Three")
    four = g.node("Four")
    five = g.node("Five")
    six = g.node("Six")
    seven = g.node("Seven")

    g.edge(one, two, three, four, 'A')
    g.edge(two, five, six, 'B')
    g.edge(two, seven, 'C')

    g.render()

    # example ends here
    assert g.source == r"""digraph example_02a {
	graph [fontname=helvetica nodesep=0.5 rankdir=LR ranksep=0.5 sep=0.4]
	node [color="#13136c" fontname=helvetica penwidth=1.8 shape=box]
	edge [fontname=helvetica]
	n_b [label=One]
	n_1 [label=Two]
	n_f [label=Three]
	n_c [label=Four]
	n_f8 [label=Five]
	n_b1 [label=Six]
	n_6 [label=Seven]
	n_3 [label=A shape=none]
	n_b -> n_1
	n_1 -> n_f
	n_f -> n_c
	n_c -> n_3
	n_d [label=B shape=none]
	n_1 -> n_f8
	n_f8 -> n_b1
	n_b1 -> n_d
	n_a [label=C shape=none]
	n_1 -> n_6
	n_6 -> n_a
}"""


def example_02b():
    """
    # Branches - syntax variant
    You don't have to assign nodes to variables. However it's a good practice to do so.
    You can define nodes while `g.edge(...)` call.
    Here node `two` is assigned to a local variable, because we refer it several times.
    """
    from grot import Grot

    this_dir_path = os.path.dirname(__file__)  # if run in console - remove 'directory' parameter below
    out_dir_path = os.path.join(this_dir_path, 'out')

    g = Grot(name='example_02b', format='png', directory=out_dir_path, graph_attrs={"rankdir": "LR"})

    two = g.node("Two")
    g.edge(g.node("One"), two, g.node("Three"), g.node("Four"), 'A')
    g.edge(two, g.node("Five"), g.node("Six"), 'B')
    g.edge(two, g.node("Seven"), 'C')

    g.render()

    # example ends here
    assert g.source == r"""digraph example_02b {
	graph [fontname=helvetica nodesep=0.5 rankdir=LR ranksep=0.5 sep=0.4]
	node [color="#13136c" fontname=helvetica penwidth=1.8 shape=box]
	edge [fontname=helvetica]
	n_1 [label=Two]
	n_b [label=One]
	n_f [label=Three]
	n_c [label=Four]
	n_3 [label=A shape=none]
	n_b -> n_1
	n_1 -> n_f
	n_f -> n_c
	n_c -> n_3
	n_f8 [label=Five]
	n_b1 [label=Six]
	n_d [label=B shape=none]
	n_1 -> n_f8
	n_f8 -> n_b1
	n_b1 -> n_d
	n_6 [label=Seven]
	n_a [label=C shape=none]
	n_1 -> n_6
	n_6 -> n_a
}"""
