class LogMessage(object):
    """
    Log message container class
    """
    KEY_REFERENCE = 'logref'
    KEY_MESSAGE = 'message'

    def __init__(self, reference):
        """
        Initialise the log object
        """
        self.params = {}
        self.message = 'No message specified'
        self.add(LogMessage.KEY_REFERENCE, reference)

    def add(self, key, value):

        if key in self.params:
            raise ValueError('Log key {0} already exists in this message'.format(key))
        self.params[key] = value

    def write(self, logger):
        logger(self.message, extra=self.params)


class LogTypeException(Exception):
    def __init__(self):
        self.message = 'Only log messages of type LogMessage are valid'

