class Error(Exception):
    """
    Base class for all exceptions
    """
    pass


class NoCompSelectException(Error):
    """
    Raised when the user doesn't select any comparison
    """
    pass


class NoSeedEqualException(Error):
    """
    Raised when the algorithm found no matching string
    """
    pass


class NoSpeciesSelectException(Error):
    """
    Raised when the user doesn't select any species
    """
    pass


class ErrorInFileException(Error):
    """
    Raised when the user use parameter with errors
    """
    pass
