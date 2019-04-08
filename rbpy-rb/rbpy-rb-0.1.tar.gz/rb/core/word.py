from rb.core.text_element import TextElement
from rb.core.lang import Lang
from spacy.tokens.token import Token

class Word(TextElement):
    def __init__(self, lang: Lang, token: Token, container: TextElement):
        TextElement.__init__(self, lang, token.text, container)
        self.token = token
        self.lemma = token.lemma_
        self.pos = token.tag_