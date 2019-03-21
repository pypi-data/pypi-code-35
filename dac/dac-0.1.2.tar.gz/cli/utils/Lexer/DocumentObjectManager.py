""" the document object manager will compile the lines into datastructures that are compatible with the JitR """
import sys

from .Document import Document
from .Block import Block

class DocumentObjectManager:
    def __init__(self, lines):
        self.lines = lines
        self.process()

    def process(self):
        self.document = Document()
        for idx, line in self.lines.items():

            if line.type == "tpl_pointer":
                self.current_block = Block()
                self.current_block.tpl = line.key
                self.document.blocks.append(self.current_block)

            else:
                self.document.blocks[-1].lines[line.uuid] = line
                    
        for block in self.document.blocks:
            block._serialize()