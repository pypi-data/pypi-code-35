""" A Block is an atomic unit of data that is passed to the JitR """ 

import uuid

class Block:
    def __init__(self):
        self.metadata = {}
        self.metadata['uuid'] = str(uuid.uuid4())
        self.tpl = "undefined"
        self.current_key = "undefined"
        self.data = {}
        self.lines = {}
    
    def _get_num_lines_in_block(self):
        return len(self.lines)
    
    def _get_first_line_num_in_block(self):
        return self.lines[0].number

    def _get_prev_line_by_uuid(self, uuid):
        """ this method will return the previous line obj based
        on a provided line uuid. """
        # return self.lines[]
        c = list(self.lines.keys()).index(uuid)-1
        try:
            uuid = list(self.lines.keys())[c]
            if uuid in self.lines:
                return self.lines[uuid]
            return None
        except IndexError as err:
            return None

    def _get_next_line_by_uuid(self, uuid):
        """ this method will return the next line obj based on
        a provided line uuid. """
        c = list(self.lines.keys()).index(uuid)+1
        try:
            uuid = list(self.lines.keys())[c]
            if uuid in self.lines:
                return self.lines[uuid]
            return None
        except IndexError as err:
            return None
        
    def _serialize(self):
        """ will convert line data into an actual data structure
        that can be passed to JitR """
        for uuid, line in self.lines.items():
    
            if line.type == "metadata":
                self.metadata[line.key] = line.val

            if line.type == "kvp":
                self.current_key = line.key.lstrip()
                self.data[self.current_key] = line.val.lstrip()
            
            if line.type == "str_cont":
                prev_line = self._get_prev_line_by_uuid(line.uuid)
                if prev_line is not None:
                    if prev_line.type == "empty":
                        self.data[self.current_key] = "%s\n\n%s" % (self.data[self.current_key], line.content.lstrip())
                    else:
                        self.data[self.current_key] = "%s\n%s" % (self.data[self.current_key], line.content.lstrip())