from .LineParser import LineParser
# from .LineMap import LineMap
from .DocumentObjectManager import DocumentObjectManager

class Lex:

    def __init__(self, stream):
        self.stream = stream
        self.line_list = self.stream.split("\n")
        self.lines = {}
        idx = 0
        for line in self.line_list:
            idx += 1
            l = LineParser(idx, line)
            self.lines[idx] = l
        
        self.dom = DocumentObjectManager(self.lines)