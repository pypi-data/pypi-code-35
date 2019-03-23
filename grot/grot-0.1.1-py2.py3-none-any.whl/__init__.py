import os
from contextlib import contextmanager

import graphviz

from ._id_vault import IdVault
from ._tools import escape_string, string_types, pairwise


class Grot(object):
    graph_attributes = {}
    _default_graph_attrs = {
        'fontname': 'helvetica',
        'nodesep': '0.5',
        'ranksep': '0.5',
        'sep': '0.4',
    }
    node_attributes = {}
    _default_node_attrs = {
        'color': '#13136c',
        'shape': 'box',
        'fontname': 'helvetica',
        'penwidth': '1.8',
    }
    edge_attributes = {}
    _default_edge_attrs = {
        'fontname': 'helvetica',
    }

    def __init__(self, py_file_path=None, graph_attrs=None, node_attrs=None, edge_attrs=None, id_vault=None,
                 directed=True, **native_dot_kwargs):
        # the vault has to be shared between parent and child graphs
        self._id_vault = id_vault or IdVault()

        if isinstance(py_file_path, str) and os.path.exists(os.path.dirname(py_file_path)):
            auto_directory, py_file_name = os.path.split(py_file_path)
            auto_name = os.path.splitext(py_file_name)[0]

            native_dot_kwargs['directory'] = native_dot_kwargs.get('directory', auto_directory)
            native_dot_kwargs['name'] = native_dot_kwargs.get('name', auto_name)
            native_dot_kwargs['filename'] = native_dot_kwargs.get('filename', auto_name + ".dot")

        if directed:
            self.g = graphviz.Digraph(**native_dot_kwargs)
        else:
            self.g = graphviz.Graph(**native_dot_kwargs)

        attributes_sections = [
            ("graph", graph_attrs or {}, self.graph_attributes, self._default_graph_attrs),
            ("node", node_attrs or {}, self.node_attributes, self._default_node_attrs),
            ("edge", edge_attrs or {}, self.edge_attributes, self._default_edge_attrs),
        ]

        for section_name, instance_attributes, class_attributes, default_attributes in attributes_sections:
            used_attributes = default_attributes.copy()
            used_attributes.update(class_attributes)
            used_attributes.update(instance_attributes)
            # setting an attribute to None cancels default value
            used_attributes = {k: v for k, v in used_attributes.items() if v is not None}
            if used_attributes:
                self.g.attr(section_name, **used_attributes)

    def attr(self, *p, **k):
        return self.g.attr(*p, **k)

    @property
    def source(self):
        return self.g.source

    def render(self, *p, **k):
        if 'view' not in k:
            k['view'] = False
        return self.g.render(*p, **k)

    def same_rank(self, first, second, *others):
        self.g.body.append("{{rank=same; {}; {};{}}}".format(first, second, "".join(" %s;" % n for n in others)))

    def __str__(self):
        return str(self.g)

    @contextmanager
    def subgraph(self, graph_attrs=None, node_attrs=None, edge_attrs=None, label=None, **dot_attrs):
        graph_attrs = graph_attrs or {}
        if label:
            graph_attrs['label'] = label

        name = self._id_vault.eval_sub_graph_name(dot_attrs)
        sub_graph = self.__class__(name=name, graph_attrs=graph_attrs, node_attrs=node_attrs, edge_attrs=edge_attrs,
                                   id_vault=self._id_vault, **dot_attrs)

        yield sub_graph
        self.g.subgraph(graph=sub_graph.g)
        # after this moment this sub_graph instance becomes useless.
        # Creation of any object via this instance will be not attached to parent graph / will be not rendered.
        # In order to avoid enormous confusion - it's better to raise instantly:
        sub_graph.edge = sub_graph._raise_finalized
        sub_graph.node = sub_graph._raise_finalized
        sub_graph.subgraph = sub_graph._raise_finalized

    def _raise_finalized(self, *_, **__):
        msg = "This graph object named '{}' ('{}' type) has been finalized already.\n" \
              "You have to either use it within its 'with' subgraph scope\n" \
              "or use main graph's handle to create objects."
        raise ValueError(msg.format(self.g.name, self.__class__.__name__))

    def edge(self, start_node, target_node, *next_targets, **edge_attributes):
        edge_chain = self._chain(start_node, target_node, *next_targets)
        nodes = list(self._supplement_missing_nodes(edge_chain))
        if nodes and nodes[0][0] is not None:
            raise ValueError("First edge in a chain cannot have a transition label.")
        for (_, a), (edge_label, b) in pairwise(nodes):
            if edge_label is not None:
                current_edge_attrs = edge_attributes.copy()
                current_edge_attrs['label'] = escape_string(edge_label)
            else:
                current_edge_attrs = edge_attributes

            self.g.edge(str(a), str(b), **current_edge_attrs)

    def __getitem__(self, keys):
        if not isinstance(keys, tuple):
            keys = (keys,)
        if len(keys) < 2:
            raise ValueError("Expecting at least two points to make an edge.")

        return self.edge(*keys)

    def node(self, content_text, **attrs):
        yet_known, short_identifier = self._id_vault(content_text, attrs)
        if not yet_known:
            # register a new node in Dot instance
            self.g.node(short_identifier, label=escape_string(content_text), **attrs)

        return Node(self, short_identifier)

    @staticmethod
    def _chain(*elements):
        return elements

    def _supplement_missing_nodes(self, nodes_chain):
        for node_or_tuple in nodes_chain:
            if isinstance(node_or_tuple, tuple):
                if not len(node_or_tuple) == 2:
                    msg = "Expecting pairs, got {} elements in {}."
                    raise TypeError(msg.format(len(node_or_tuple), type(node_or_tuple).__name__))

                edge_label, node = node_or_tuple
            else:
                node = node_or_tuple
                edge_label = None

            if edge_label and not isinstance(edge_label, string_types):
                msg = "Expecting edge label given in string, got '{}' in '{}' node."
                raise TypeError(msg.format(type(edge_label).__name__, node))

            if not isinstance(node, Node):
                assert isinstance(node, string_types), "expecting node object or string, got " + str(type(node))
                yield edge_label, self.node(node, shape="none")
            else:
                yield edge_label, node


class Node(object):
    def __init__(self, parent_graph, unique_id):
        self.parent_graph = parent_graph
        self.unique_id = unique_id

    def __str__(self):
        return self.unique_id

    def edge(self, target_node, *next_targets, **edge_attributes):
        self.parent_graph.edge(self, target_node, *next_targets, **edge_attributes)
