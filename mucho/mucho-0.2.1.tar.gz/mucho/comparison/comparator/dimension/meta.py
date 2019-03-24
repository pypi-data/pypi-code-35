from collections import OrderedDict

from .property import DimensionProperty


class DimensionComparatorMeta(type):
    def __new__(mcs, name, bases, attrs):
        """
        Add a 'properties' attribute to the created class, containing a dict
        with its DimensionProperty attributes.
        """
        instance = super().__new__(mcs, name, bases, attrs)
        properties = OrderedDict()
        for attr, value in attrs.items():
            if isinstance(value, DimensionProperty):
                if not value.resolver:
                    value.resolver = 'resolve_'+attr
                properties[attr] = value
        instance._properties = properties
        return instance
