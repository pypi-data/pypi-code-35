from rb.complexity.complexity_index import ComplexityIndex
from rb.complexity.index_category import IndexCategory
from rb.core.lang import Lang
from rb.core.text_element import TextElement
from rb.core.word import Word


class NoWordsIndex(ComplexityIndex):
    def __init__(self, lang: Lang):
        ComplexityIndex.__init__(self, lang, IndexCategory.SURFACE, "Wd")

    def process(self, element: TextElement) -> float:
        if isinstance(element, Word):
            return 1.
        count = sum(self.process(child) for child in element.components)
        element.indices[self] = count
        return count
        