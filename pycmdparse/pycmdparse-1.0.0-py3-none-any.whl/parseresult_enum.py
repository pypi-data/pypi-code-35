from enum import Enum


class ParseResultEnum(Enum):
    """
    Defines the overall results of parsing the entire command line
    """

    SUCCESS = 1,
    """Command line parsed correctly"""
    PARSE_ERROR = 2,
    """Command line parsing failed"""
    SHOW_USAGE = 3
    """The -h, or the --help option was provided on the command line"""
    MISSING_MANDATORY_ARG = 4
    """A mandatory option was not provided on the command line"""
