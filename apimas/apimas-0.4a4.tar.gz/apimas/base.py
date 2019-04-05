class ProcessorFactory(object):
    Constructors = {}

    def __init__(self, collection_loc, action_name):
        self.collection_loc = collection_loc
        self.action_name = action_name

    def process(self, runtime_data):
        raise NotImplementedError('process() must be implemented')

    def cleanup(self, name, exc, data):
        return {}
