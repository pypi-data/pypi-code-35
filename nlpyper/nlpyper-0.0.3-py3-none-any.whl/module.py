from nlpyper.base_module import BaseModule

class Module(BaseModule):

    def run_prev(self, doc, context):
        self.run(doc)
    
    """
    Override the following methods
    """
    
    def init(self, context, log):
        msg = "Module {} doesn't override 'init' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)
    
    def run(self, doc):
        msg = "Module {} doesn't override 'run' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)
