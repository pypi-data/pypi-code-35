import weakref

from ._attr_reg import AttributeFloater

_attr_registry = AttributeFloater()


@_attr_registry.all_attrs_fixed
class NodeBase(object):
    make_attrs_float = _attr_registry.all_attrs_float

    __slots__ = "children", "__parent"

    def __init__(self, parent_node_):
        self.__parent = weakref.ref(parent_node_) if parent_node_ else None
        self.children = []

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.__parent)

    def replant(self, other_plant):
        if not isinstance(other_plant, self.__class__):
            raise TypeError("Can replant only nodes of the same type, got {}.".format(type(other_plant)))
        _attr_registry.current_top_node.children.extend(other_plant.children)

    @property
    def degree(self):
        """ For a given node, its number of _children. A leaf is necessarily degree zero. """
        return len(self.children)

    @property
    def height(self):
        """ The height of a node is the number of edges on the longest path between that node and a leaf. """
        if not self.children:
            return 0
        else:
            return 1 + max(child.height for child in self.children)

    def __getattribute__(self, attribute_name):
        """ Try to expose interface of a node that is currently on top (whose context we are currently in). """

        top_node = _attr_registry.top_takes_it(attribute_name)
        if top_node:
            return object.__getattribute__(top_node, attribute_name)

        return super(NodeBase, self).__getattribute__(attribute_name)

    def _make_child(self, node_class, *args, **kwargs):
        if not issubclass(node_class, NodeBase):
            msg = "Node class has to be a subclass of NodeBase, got %s."
            raise TypeError(msg % node_class.__name__)
        new_node_instance = node_class(self, *args, **kwargs)
        self.children.append(new_node_instance)
        return new_node_instance

    def __enter__(self):
        _attr_registry.enter_(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _attr_registry.exit_()

    def __str__(self):
        is_root = self.__parent is None
        if is_root:
            return "".join(item for item in self.document_root_string_items())
        else:
            return "".join(item for item in self.string_items(0))

    def string_items(self, tree_level):
        msg = "\n".join([
            "NodeBase.string_items is an abstract method.", "",
            "It's supposed to:",
            " - be a generator yielding string items,",
            " - compose document representation of that node with ''.join(node.string_items(0)),",
            " - care for document's line breaks, markup and indentation.",
            "It needs to be implemented in derived class {name!r}.",
            ""
        ])
        raise NotImplementedError(msg.format(name=self.__class__.__name__))

    def document_root_string_items(self):
        """ Node being at zero level behaves a bit different. Has no own value, just it's header and its _children."""
        for item in self._root_head_items():
            yield item
        for child in self.children:
            for item in child.string_items(0):
                yield item
            yield "\n"

    @classmethod
    def _root_head_items(cls):
        return iter(())  # empty iterator


class LeafNodeMixin(object):
    __slots__ = ()

    def _make_child(self, *_, **__):
        msg = "{} is not allowed to have any children nodes."
        raise AttributeError(msg.format(self.__class__.__name__))

    def __enter__(self):
        msg = "Instance of {} cannot enter its scope, it's a leaf. Call it as a regular method (w/o 'with')."
        raise AttributeError(msg.format(self.__class__.__name__))
