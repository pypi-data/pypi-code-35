import os

"""
Verbosity level as set by the environment variable, VPRINTV
"""
VPRINT_KEYWORD = 'VPRINTV'


def get_vprint_level():
    # type: () -> int
    """
    Get the current vprint level from the environment. This is the primary
    control of the logging level.
    Returns:
        vprint log level
    """
    vprint_level = os.environ.get(VPRINT_KEYWORD, 0)
    try:
        # todo: parsers for other levels
        vprint_level = int(vprint_level)
    except ValueError:
        vprint_level = 0

    return vprint_level

