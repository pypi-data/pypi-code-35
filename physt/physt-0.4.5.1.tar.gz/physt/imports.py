import logging
import os


__all__ = []


def _try_import(name: str):
    code = f"""if os.environ.get("PHYST_DISABLE_{name.upper()}"):
    logging.debug("{name} support disable because of the PHYST_DISABLE_{name.upper()} env. variable.")
else:
    global {name}
    global {name.upper()}_ENABLED
    try:
        import {name}
        {name.upper()}_ENABLED = True
        logging.debug("{name} support enabled.")
        __all__.append("{name}")
    except:
        {name.upper()}_ENABLED = False
        logging.debug("{name} support disable, impossible to load the library.")
    __all__.append("{name.upper()}_ENABLED")
"""
    exec(code)


_try_import("pandas")
_try_import("matplotlib")
_try_import("seaborn")
