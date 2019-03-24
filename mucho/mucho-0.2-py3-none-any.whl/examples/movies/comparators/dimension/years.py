from mucho.comparison.comparator import DimensionComparator, DimensionProperty

from examples.movies.entities.avwork import AVWork


class YearsComparator(DimensionComparator):
    difference = DimensionProperty(
        description="Difference in years",
        resolver='get_difference')
    are_same = DimensionProperty(
        description="Tells whether the years are same or not")

    def get_difference(self, src: AVWork, trg: AVWork) -> int:
        if src.year is None or trg.year is None:
            return 85
        return abs(src.year-trg.year)

    def resolve_are_same(self, src: AVWork, trg: AVWork) -> bool:
        if src.year is None or trg.year is None:
            return False
        else:
            return src.year == trg.year
