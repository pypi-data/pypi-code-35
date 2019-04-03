class NotSupportedException(Exception):
    pass


class RequestFailedException(Exception):

    def __init__(self, message, request):
        super().__init__(message)
        self.request = request


class JSONNotSupportedException(Exception):

    def __init__(self, result):
        super().__init__('{} did not return data in a JSON format.'.format(result.url))