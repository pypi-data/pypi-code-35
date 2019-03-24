from typing import (
    Type,
    TYPE_CHECKING,
    Callable,
)

from .emitter import EventEmitter
from .event import BaseEvent

if TYPE_CHECKING:
    from .subscription import Subscription


def event_listener(emitter: EventEmitter, event_type: Type[BaseEvent]) -> Callable[[Callable], "Subscription"]:
    """
    A decorator factory for creating easy inline event listeners.

    ::
        my_emitter = EventEmitter()
        MyEvent = type("MyEvent", (BaseEvent, ), {})

        @event_listener(my_emitter, MyEvent)
        def my_event_subscription(event):
            print("Got MyEvent!")

        # Prints "Got MyEvent!" on next iteration of event loop.
        my_emitter.emit(MyEvent())

        # Unsubscribe from future events.
        my_event_subscription.unsubscribe()

    :param emitter:
    :param event_type:
    :return:
    """
    def decorator(method) -> "Subscription":
        return emitter.listen(event_type, method)
    return decorator
