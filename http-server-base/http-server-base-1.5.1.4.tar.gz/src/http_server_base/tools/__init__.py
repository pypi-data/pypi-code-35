from http_server_base.tools.types import JsonSerializable, RegExpType
@property
def re_type():
    from warnings import warn
    warn("re_type is going to be deprecated. Use RegExpType instead", DeprecationWarning, 2)
    return RegExpType

from http_server_base.tools.config_loader import ConfigLoader
from http_server_base.tools.logging import setup_logging, logging_method, ExtendedLogger, RequestLogger, StyleAdapter
from http_server_base.tools.subrequest_classes import HttpSubrequest, HttpSubrequestResponse
from http_server_base.tools.errors import ServerError, SubrequestFailedError, SubrequestFailedErrorCodes
from http_server_base.tools.re_dict import ReDict
