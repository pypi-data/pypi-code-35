import threading

from stackifyapm.instrumentation import register

_lock = threading.Lock()


def instrument():
    """
    Instruments all registered methods/functions
    """
    with _lock:
        for obj in register.get_instrumentation_objects():
            obj.instrument()


def uninstrument():
    """
    If instrumentation is present, remove it and replaces it with the original method/function
    """
    with _lock:
        for obj in register.get_instrumentation_objects():
            obj.uninstrument()
