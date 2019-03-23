"""Helpers class file."""

try:
    from builtins import xrange as range
except ImportError:
    from builtins import range


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
