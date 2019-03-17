from mucho.comparison.comparator import EntityComparator

from examples.movies.comparators.dimension.titles import TitlesComparator
from examples.movies.comparators.dimension.years import YearsComparator


class AVWorkComparator(EntityComparator):
    titles = TitlesComparator(description="Titles")
    years = YearsComparator(description="Release years")
