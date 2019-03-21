""" this is the line parser module for the DAC lexer. """
# This module is responsible for parsing each line in a 
# dac file, and routing the line to the appropriate handler
# based on the DAC spec.

# Based on the rules in the DAC spec, this parser can then
# pass the neccessary line data to the appropriate handler
# to build up the document object model to then be rendered
# by the JitR class.

import uuid

class LineParser():
    
    def __init__(self, idx, line):
        self.uuid = str(uuid.uuid4())
        self.number = idx
        self.content = line
        self.whitespace_index = len(line) - len(line.lstrip())
        self.type = "undefined"
        self.parse()
    
    def parse(self):
        self._is_empty()
        self._is_comment()
        self._is_str_cont()
        self._is_metadata()
        self._is_tpl_pointer()
        self._is_var_block()
        self._is_kvp()
        self._is_key()
        self._is_list_item()
        
    
    def _is_empty(self):
        self.is_empty = False
        if len(self.content.lstrip()) == 0:
            self.is_empty = True
            self.type = "empty"

    def _is_comment(self):
        self.is_comment = False
        if not self.is_empty:
            if self.content[0] == "#":
                self.is_comment = True
                self.type = "comment"
    
    def _is_str_cont(self):
        self.is_str_cont = False
        if not self.is_empty:
            if self.whitespace_index > 0:
                self.type = "str_cont"
    
    def _is_metadata(self):
        self.is_metadata = False
        if not self.is_empty:
            if self.whitespace_index > 0:
                if self.content.lstrip()[0] == "@":
                    if ':' in self.content:
                        self.is_metadata = True
                        self.type = "metadata"
                        self.data = self.content.split(':')
                        self.key = self.data[0][1:].replace('@', '').lstrip()
                        self.val = self.data[1].lstrip()
    
    def _is_tpl_pointer(self):
        self.is_tpl_pointer = False
        if not self.is_empty:
            if self.whitespace_index == 0:
                if ":" in self.content:
                    self.is_tpl_pointer = True
                    self.type = "tpl_pointer"
                    self.key = self.content[:-1]
    
    def _is_var_block(self):
        self.is_var_block = False
        if not self.is_empty:
            if self.whitespace_index == 0:
                if self.content[0] == "!":
                    if self.content.lstrip()[-1:] == ":":
                        self.type = "varblock"
                        self.is_var_block = True
                        self.varblock_key = self.content[1:-1]
    
    def _is_key(self):
        self.is_key = False
        if not self.is_empty:
            if self.whitespace_index > 0:
                if ':' in self.content:
                    data = self.content.split(':')
                    if len(data[1].lstrip()) == 0:
                        self.type = "key"
                        self.is_key = True
                        self.key = data[0]

    def _is_kvp(self):
        self.is_kvp = False
        if not self.is_empty:
            if not self.is_metadata:
                if self.whitespace_index > 0:
                    if ':' in self.content:
                        data = self.content.split(':')
                        if len(data[1].lstrip()) > 0:
                            self.type = "kvp"
                            self.is_kvp = True
                            self.key = data[0]
                            self.val = data[1]
    
    def _is_list_item(self):
        self.is_list_item = False
        if not self.is_empty:
            if self.whitespace_index > 0:
                if self.content.lstrip()[0] == "-":
                    self.is_list_item = True
                    self.type = "list_item"