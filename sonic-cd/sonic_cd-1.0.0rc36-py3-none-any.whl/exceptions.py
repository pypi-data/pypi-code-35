class SonicException(Exception):
    def exit_code(self):
        return 7


class NonZeroExitCodeException(SonicException):
    def exit_code(self):
        return 11


class PipeNotFoundException(SonicException):
    def exit_code(self):
        return 13

    def __init__(self, pipe_name):
        super(PipeNotFoundException, self).__init__("Pipe definition for %s not found." % pipe_name)
