from .engine import NodeBase


@NodeBase.make_attrs_float
class PYamlNode(NodeBase):
    _single_indent = '  '
    __slots__ = "value", "__weakref__"

    def __init__(self, parent_node_, value):
        super(PYamlNode, self).__init__(parent_node_)
        self.value = value

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.value)

    def string_items(self, tree_level):
        representation = "{} - {}".format(self._single_indent * tree_level, self.value)
        if self.children:
            representation += ":"
        yield representation

        for child in self.children:
            yield "\n"
            for item in child.string_items(tree_level + 1):
                yield item

    def node(self, value):
        return self._make_child(PYamlNode, value)


def yaml_plant():
    return PYamlNode(None, None)
