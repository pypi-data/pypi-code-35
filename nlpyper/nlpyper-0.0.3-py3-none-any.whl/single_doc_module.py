from nlpyper.module import Module

class SingleDocModule(Module):

    """
    Override the following methods
    """
    
    def init(self, context, log):
        msg = "Module {} doesn't override 'init' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)
    
    def run(self, doc):
        msg = "Module {} doesn't override 'run' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)
