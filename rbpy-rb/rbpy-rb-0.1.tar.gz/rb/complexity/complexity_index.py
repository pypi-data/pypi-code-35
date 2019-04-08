from rb.complexity.index_category import IndexCategory
from rb.core.lang import Lang
from rb.core.text_element import TextElement

class ComplexityIndex:

    def __init__(self, lang: Lang, category: IndexCategory, abbr: str):
        self.lang = lang
        self.category = category
        self.abbr = abbr

    def process(self, element: TextElement) -> float:
        pass

    