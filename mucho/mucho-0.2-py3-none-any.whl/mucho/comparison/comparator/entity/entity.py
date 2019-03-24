from typing import Set

from .meta import EntityComparatorMeta
from mucho.comparison import ComparisonResult


class EntityComparator(metaclass=EntityComparatorMeta):
    """Compares two entities by comparing their dimensions"""

    @property
    def comparators(self):
        return self._comparators

    def compare(self, src, trg):
        """Compares two entities by comparing their dimensions and returns the
        result of the comparison codified as dimension properties.

        :param src: source entity of the comparison
        :param trg: target entity of the comparison
        :return: result of the comparison
        """
        result = ComparisonResult()
        for name, instance in self.comparators.items():
            setattr(result, name, instance.compare(src, trg))
        return result

    @property
    def variable_names(self) -> Set[str]:
        names = set()
        for dimension, dimension_comparator in self.comparators.items():
            for property in dimension_comparator.properties:
                names.add(
                    "{dimension}.{property}".format(
                        dimension=dimension, property=property))
        return names
