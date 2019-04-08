from rb.complexity.complexity_index import ComplexityIndex
from rb.complexity.index_category import IndexCategory
from rb.complexity.syntax.dep_enum import DepEnum
from rb.core.lang import Lang
from rb.core.sentence import Sentence
from rb.core.text_element import TextElement


class DepIndex(ComplexityIndex):
    def __init__(self, lang: Lang, dep_type: DepEnum):
        ComplexityIndex.__init__(self, lang, IndexCategory.SYNTAX, "Dep")
        self.dep_type = dep_type

    def process(self, element: TextElement) -> float:
        if isinstance(element, Sentence):
            count = sum(1 for token in element.doc if token.dep_ == self.dep_type.value.lower())
        else:
            count = sum(self.process(child) for child in element.components)
        element.indices[self] = count
        return count
