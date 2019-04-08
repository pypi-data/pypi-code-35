from rb.parser.spacy_parser import SpacyParser

from spacy.tokens.doc import Doc

from rb.core.lang import Lang
from rb.core.text_element import TextElement
from rb.core.word import Word


class Sentence(TextElement):
    def __init__(self, lang: Lang, text: str, container: TextElement):
        TextElement.__init__(self, lang, text, container)
        self.doc = SpacyParser.get_instance().parse(text, lang.value)
        for token in self.doc:
            word = Word(lang, token, self)
            self.components.append(word)
