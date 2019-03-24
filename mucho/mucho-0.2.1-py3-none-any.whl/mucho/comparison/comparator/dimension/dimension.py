from .meta import DimensionComparatorMeta
from mucho.comparison import ComparisonResult


class DimensionComparator(metaclass=DimensionComparatorMeta):
    """Compares a specific dimension of two entities."""

    def __init__(self, description=None):
        self.description = description

    @property
    def properties(self):
        return self._properties

    def compare(self, src, trg) -> ComparisonResult:
        """Compares the dimension of the two entities and returns the result of
        the comparison codified as dimension properties.

        :param src: source entity of the comparison
        :param trg: target entity of the comparison
        :return: result of the comparison
        """
        self._pre_resolve(src, trg)
        values = dict()
        for property_name, property in self.properties.items():
            try:
                resolver = getattr(self, property.resolver)
            except AttributeError:
                raise NotImplementedError(
                    "Resolver not implemented for property '{0}'".format(
                        property_name))
            values[property_name] = resolver(src, trg)
        return ComparisonResult(**values)

    def _pre_resolve(self, src, trg):
        pass
