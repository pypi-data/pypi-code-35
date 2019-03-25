from nlpyper.module import Module

class MultiDocModule(Module):

    def __init__(self, n = -1):
        self.n = n
        self.docs = []

    def run_prev(self, doc, context):
        self.docs.append(doc)
        if (self.n > 0 and len(self.docs) == self.n) or (len(self.docs) == context['n_docs']):
            self.run(self.docs)
            self.docs.clear()

    """
    Override the following methods
    """
    
    def init(self, context, log):
        msg = "Module {} doesn't override 'init' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)
    
    def run(self, docs):
        msg = "Module {} doesn't override 'run' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)
