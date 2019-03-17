from enum import Enum


class OptAcceptResultEnum(Enum):
    """
    Defines the outcome of parsing a single option from the command line. Also used
    by the custom validator in the CmdLine sub-class to return the results of the
    validation callback.
    """

    ACCEPTED = 1,
    """
    The option from the cmdline was processed successfully
    """
    IGNORED = 2,
    """
    The option from the cmdline didn't match the object's option,
    so it was ignored
    """
    ERROR = 3
    """
    The option from the cmdline matched the object's option but there
    was an error processing it
    """
