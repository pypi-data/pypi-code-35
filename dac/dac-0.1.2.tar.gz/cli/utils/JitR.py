""" Just in Time - Renderer """
import os
from jinja2 import Environment, BaseLoader
import glob

class JitR:

    def __init__(self, tpldir = None):
        self.use_default_tpl_dir = False
        self.tpldir = tpldir
        self.output = []
        if self.tpldir is None:
            self.use_default_tpl_dir = True
            self.tpldir = "%s/templates" % (os.getcwd())
            
        if not os.path.isdir(self.tpldir):
            raise Exception("Invalid Template Directory: %s\nDirectory Not Found" % (self.tpldir))
        
        self._load_all_tpls()

    def _load_tpl_file(self, tplpath):
        """ this method will return the string value of a tpl
        provided the tpl file name (aka: key) """
        if os.path.isfile(tplpath):
            with open(tplpath) as tplfile:
                return tplfile.read()
        return None

    def _load_all_tpls(self):
        self.tpls = {}
        for tpl in glob.glob("%s/*.j2" % (self.tpldir)):
            tplcontent = self._load_tpl_file(tpl)
            if tplcontent is not None:
                key = tpl.split("/")[-1].split('.')[0]
                self.tpls[key] = tplcontent
            
    def _compile_tpl(self, tplkey, data):
        """ this method will compile a template """
        tpl = Environment(loader=BaseLoader()).from_string(self.tpls[tplkey])
        return tpl.render(data)
    
    def render(self, block):
        tpl = block.tpl
        data = block.data
        data['metadata'] = block.metadata
        self.output.append(self._compile_tpl(tpl, data))