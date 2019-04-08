from rb.core.lang import Lang
from rb.core.text_element import TextElement
from rb.core.block import Block


class Document(TextElement):
    def __init__(self, lang: Lang, text: str, container: TextElement):
        TextElement.__init__(self, lang, text, container)
        
        for block in text.split("\n"):
            self.components.append(Block(lang, block.strip(), self))
