import uuid
from pprint import pprint

class Document:

    def __init__(self):
        self.statements = []
    
    def _rem(self, id):
        for s in self.statements:
            if s.id == id:
                self.statements.pop(self.statements.index(s))
    
    def _clean(self):
        rm = []
        for statement in self.statements:
            if statement.white_space_index > 0:
                rm.append(statement.id)
        for id in rm:
            self._rem(id)

class Statement:
    """ a statement object contains the k/v pairs of a document.
    the key by convention must be associated to a template of that
    key's string value. Where the value (aka content) will be the
    data passed to the given template. """

    def __init__(self, ldata):
        self.id = str(uuid.uuid4())
        self.white_space_index = ''
        self.key = ldata[0]
        self.content = ldata[1].strip()

class Lex:

    def __init__(self, stream):
        self.stream = stream
        self.document = Document()
        

        self.lines = self.stream.split("\n")
        
        idx = 0
        for line in self.lines:
            idx += 1
            self._parse_line_into_statement(idx, line)
        self._handle_nested_struct()
        self.document._clean()
    
    # TODO: offset some of the logic with clearer
    # function definitions.
    def _parse_line_into_statement(self, idx, content):
        if '#' in content:
            print("ignoring comment on line %s" % (idx))
            return
        else:
            print("processing line %s" % (idx))
    
    def _get_whitespace_index(self, string):
        whitespace_index = len(string) - len(string.lstrip())
        return whitespace_index

    def _handle_nested_struct(self):
        for statement in self.document.statements:
            statement.white_space_index = self._get_whitespace_index(statement.key)
            if statement.white_space_index == 0:
                if statement.content == '':
                    statement.content = {}
                    self.current_parent = statement
            else:
                self.current_parent.content[statement.key.strip()] = statement.content
    
    def parse(self):
        for statement in self.document.statements:
            yield statement