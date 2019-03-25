from nlpyper.module import Module

class DocsByFieldModule(Module):

    def __init__(self, field):
        self.field = field
        self.docs = {}

    def run_prev(self, doc, context):
        key = doc[self.field]
        if key not in self.docs:
            self.docs[key] = []
        self.docs[key].append(doc)
        # run module if all docs already classified
        merged_docs = sum(self.docs.values(), [])
        if len(merged_docs) == context['n_docs']:
            for field, docs in self.docs.items():
                self.run(docs, context)

    """
    Override the following methods
    """
    
    def init(self):
        msg = "Module {} doesn't override 'init' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)
    
    def run(self, docs, context):
        msg = "Module {} doesn't override 'run' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)
