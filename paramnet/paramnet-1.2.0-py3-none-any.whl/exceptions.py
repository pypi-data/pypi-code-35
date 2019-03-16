__all__ = []

__all__.extend([
    'ParametrizedNetworkError',
    'ParameterError',
    'NodeParameterError',
    'EdgeParameterError',
    'FieldConflictError'
])


class ParametrizedNetworkError(Exception):
    pass


class FieldConflictError(ParametrizedNetworkError):
    pass


class ParameterError(ParametrizedNetworkError):
    pass


class NodeParameterError(ParameterError):
    pass


class EdgeParameterError(ParameterError):
    pass
