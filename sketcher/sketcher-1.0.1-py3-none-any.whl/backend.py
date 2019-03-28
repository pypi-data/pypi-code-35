class NoBackend(BaseException):
    def __init__(self):
        super().__init__(
            "There is no supported graphical backend installed or"
            " the backend you specified is not available.\n"
            "Try to install one of those:\n" +
            "\n".join("- " + back for back in supported_backends)
        )


supported_backends = [
    "pyglet",
    "tkinter",
]

try:
    import pyglet
    have_pyglet = True
except ImportError:
    have_pyglet = False


try:
    import tkinter
    have_tk = True
except ImportError:
    have_tk = False


def get_backend(use='auto'):
    if use == 'auto':
        if have_pyglet:
            use = 'pyglet'
        elif have_tk:
            use = 'tkinter'
        else:
            use = 'nothing'

    if use == 'pyglet':
        from .backend_pyglet import Backend
    elif use == 'tkinter':
        from .backend_tk import Backend
    else:
        raise NoBackend()
    return Backend
