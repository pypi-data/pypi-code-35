from mucho.comparison.comparator import DimensionComparator, DimensionProperty

from examples.movies.entities.avwork import AVWork


class TitlesComparator(DimensionComparator):
    similarity = DimensionProperty(
        description="Similarity between titles, between 0 and 100")
    are_exact = DimensionProperty(description="Titles are exact")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._similarity = 0

    def _pre_resolve(self, src: AVWork, trg: AVWork):
        if src.title == trg.title:
            self._similarity = 100
        elif src.title in trg.title or trg.title in src.title:
            self._similarity = 85
        else:
            self._similarity = 0

    def resolve_similarity(self, src: AVWork, trg: AVWork) -> float:
        return self._similarity

    def resolve_are_exact(self, src: AVWork, trg: AVWork) -> bool:
        return self._similarity == 100
