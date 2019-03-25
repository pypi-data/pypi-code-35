from nlpyper.base_module import BaseModule

class BatchSourceModule(BaseModule):

    def init(self, context, log):
        msg = "Source '{}' doesn't override 'init' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)
    
    def run(self, pipeline, data):
        msg = "Source '{}' doesn't override 'run' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)

    """
    return: result data
    """
    def on_success(self, doc):
        msg = "Source '{}' doesn't override 'on_success' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)

    def on_error(self, doc):
        msg = "Source '{}' doesn't override 'on_error' method".format(self.__class__.__name__)
        raise NotImplementedError(msg)
