"""
Provides BaseEvent ABC.
"""

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .emitter import EventEmitter


# pylint: disable=too-few-public-methods
class BaseEvent:
    """
    ABC for events.

    :ivar target: The source of the event; this should **always** refer to the
        :class:`EventEmitter` that the event was emitted from.
    """

    def __init__(self, *, target: "EventEmitter" = None):
        self.target = target

    target: "EventEmitter"
