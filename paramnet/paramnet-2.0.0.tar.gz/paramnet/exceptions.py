__all__ = []

__all__.extend([
    'ParametrizedNetworkError',
    'FieldConflictError'
])


class ParametrizedNetworkError(Exception):
    pass


class FieldConflictError(ParametrizedNetworkError):
    pass
