from parser.spacy_parser import SpacyParser

from rb.core.lang import Lang
from rb.core.text_element import TextElement
from rb.core.sentence import Sentence


class Block(TextElement):
    def __init__(self, lang: Lang, text: str, container: TextElement):
        TextElement.__init__(self, lang, text, container)
        
        for sentence in SpacyParser.get_instance().tokenize_sentences(text):
            self.components.append(Sentence(lang, sentence, self))
