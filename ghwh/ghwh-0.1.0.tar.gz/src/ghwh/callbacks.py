_callbacks = {}


class NoCallbackError(Exception):
    pass


def register(event, func):
    _callbacks[event] = func


def deregister(event, func):
    del _callbacks[event]


def run(event, headers, payload):
    func = _callbacks.get(event)
    if func is None:
        raise NoCallbackError(f"No callback registered for {event}")
    return func(headers, payload)
