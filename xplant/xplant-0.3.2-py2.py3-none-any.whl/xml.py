from ._xml_attributes import XmlAttributes
from .engine import NodeBase, LeafNodeMixin


class _XmlElementNodeBase(NodeBase):
    _attribute_processor = XmlAttributes
    _indent_value = 2 * " "
    _force_inline = False
    __slots__ = "tag_name", "attributes"

    def __init__(self, parent_node_, tag_name, *xml_args, **xml_kwargs):
        super(_XmlElementNodeBase, self).__init__(parent_node_)
        self.tag_name = tag_name
        self.attributes = self._attribute_processor(*xml_args, **xml_kwargs)

    def __repr__(self):
        return "{}({}, **{})".format(self.__class__.__name__, self.tag_name, self.attributes)

    @classmethod
    def _root_head_items(cls):
        yield '<?xml version="1.0" encoding="utf-8"?>\n'


@NodeBase.make_attrs_float
class XmlElement(_XmlElementNodeBase):
    __slots__ = ("__weakref__",)

    def string_items(self, tree_level):
        yield "<{}{}>".format(self.tag_name, self.attributes)
        for item in self._children_markup(tree_level):
            yield item
        yield "</{}>".format(self.tag_name)

    @staticmethod
    def _replicant_leaf_type():
        return EmptyXmlElement

    def node(self, name, *xml_args, **xml_kwargs):
        xml_args = (name,) + xml_args
        return self._make_child(self.__class__, *xml_args, **xml_kwargs)

    def leaf(self, name, *xml_args, **xml_kwargs):
        xml_args = (name,) + xml_args
        return self._make_child(self._replicant_leaf_type(), *xml_args, **xml_kwargs)

    def line(self, tag_name, content, *xml_args, **xml_kwargs):
        """ Element containing just a text (single child). """
        with self.node(tag_name, *xml_args, **xml_kwargs) as node:
            node.text(content)

    def text(self, string_value):
        return self._make_child(XmlMarkup, "{}", string_value)

    def cdata(self, string_value):
        return self._make_child(XmlMarkup, "<![CDATA[{}]]>", string_value)

    def comment(self, string_value):
        return self._make_child(XmlMarkup, "<!-- {} -->", string_value)

    def _children_markup(self, tree_level):
        break_lines = self.degree > 1 and not self._force_inline
        child_indent = self._break_line(tree_level + 1)

        for child in self.children:
            if break_lines:
                yield child_indent

            for child_string in child.string_items(tree_level + 1):
                yield child_string

        if break_lines:
            yield self._break_line(tree_level)

    @classmethod
    def _break_line(cls, tree_level):
        indent = cls._indent_value
        return "\n" + indent * tree_level


class EmptyXmlElement(LeafNodeMixin, _XmlElementNodeBase):
    __slots__ = ()

    """ E.g.: <br />, <hr /> or <img src="#" alt="" /> """

    def string_items(self, tree_level):
        yield "<{}{} />".format(self.tag_name, self.attributes)


class XmlMarkup(LeafNodeMixin, NodeBase):
    __slots__ = "value", "_format",

    def __init__(self, parent_node_, format_, value):
        super(XmlMarkup, self).__init__(parent_node_)
        self.value = value
        self._format = format_

    def string_items(self, tree_level):
        yield self._format.format(self.value)


def xml_plant():
    return XmlElement(None, None)
