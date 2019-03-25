from collections import defaultdict


class AttributeFloater(object):
    """
        It's a helper that tells us whether we would like
        to get given attribute from given instance or redirect
        getattribute call to the most top instance in current
        tree model branch.
    """

    def __init__(self, *args, **kwargs):
        super(AttributeFloater, self).__init__(*args, **kwargs)
        self.fixed = defaultdict(set)
        self._registry = defaultdict(set)
        self._node_stack = []

    @staticmethod
    def is_public(attribute_name):
        return not attribute_name.startswith("_")

    @property
    def current_top_node(self):
        """ The node whose context we are currently in. """
        if self._node_stack:
            return self._node_stack[-1]

    def top_takes_it(self, attribute_name):
        top = self.current_top_node
        if top and attribute_name in self._registry[type(top).__name__]:
            return top

    def all_attrs_float(self, cls):
        """ Makes each attribute floating unless it has been already marked as fixed e.g. in base class. """
        for base in reversed(cls.mro()):
            if base.__name__ in self.fixed:
                self.fixed[cls.__name__].update(self.fixed[base.__name__])

            if base.__name__ in self._registry:
                self._registry[cls.__name__] = set(n for n in self._registry[base.__name__]
                                                   if n not in self.fixed[cls.__name__])

        for attribute_name in cls.__dict__:
            if self.is_public(attribute_name) and attribute_name not in self.fixed[cls.__name__]:
                self._registry[cls.__name__].add(attribute_name)

        return cls

    def all_attrs_fixed(self, cls):
        for attribute_name in cls.__dict__:
            if self.is_public(attribute_name):
                self.fixed[cls.__name__].add(attribute_name)
        return cls

    def enter_(self, obj):
        self._node_stack.append(obj)

    def exit_(self):
        self._node_stack.pop()
