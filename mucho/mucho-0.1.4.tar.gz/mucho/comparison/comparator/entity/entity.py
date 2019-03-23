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
        for name, instance in self._comparators.items():
            setattr(result, name, instance.compare(src, trg))
        return result
