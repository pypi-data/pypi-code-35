from collections import OrderedDict

from mucho.comparison.comparator import DimensionComparator


class EntityComparatorMeta(type):
    def __new__(mcs, name, bases, attrs):
        """
        Adds a 'comparator' attribute to the created class, which is a dict
        with its DimensionComparator attributes.
        """
        instance = super().__new__(mcs, name, bases, attrs)
        comparators = OrderedDict()
        for attr, value in attrs.items():
            if isinstance(value, DimensionComparator):
                comparators[attr] = value
        instance._comparators = comparators
        return instance
