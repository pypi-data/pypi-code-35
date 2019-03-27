from typing import Optional

from attr import attrs

from cortex.profile.utils.attr_utils import describableAttrib

__all__ = [
    'MessageResponse',
    'ErrorResponse',
]

@attrs(frozen=True)
class MessageResponse(object):
    message = describableAttrib(type=str, description="What is the status of the version increment request?")
    version = describableAttrib(type=Optional[int], default=None, description="What is the current version of the resource?")


@attrs(frozen=True)
class ErrorResponse(object):
    error = describableAttrib(type=str, description="What is the error message associated with the request?")
