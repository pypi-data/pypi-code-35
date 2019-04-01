class InstallationNotFoundError(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


__all__ = ['InstallationNotFoundError']