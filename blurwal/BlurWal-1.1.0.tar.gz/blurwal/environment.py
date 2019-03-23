"""
Functions for preparing the environment to run in.

Author: Benedikt Vollmerhaus
License: MIT
"""

import atexit
import logging
import os
import shutil
from typing import Dict, Optional, Tuple, Type

from blurwal import paths, utils
from blurwal.backends import base, feh, xfconf

#: Supported backend names with their implementation and binary
BACKENDS: Dict[str, Tuple[Type[base.Backend], str]] = {
    'feh': (feh.FehBackend, 'feh'),
    'xfce': (xfconf.XfconfBackend, 'xfconf-query')
}

#: A map of XDG_CURRENT_DESKTOP values to their respective backends
XDG_TO_BACKEND: Dict[str, str] = {'XFCE': 'xfce'}


def get_backend(name: Optional[str]) -> Optional[base.Backend]:
    """
    Return an instance of the wallpaper backend to use.

    The backend is selected with the following priority:
      1. The backend corresponding to the given name, if installed
      2. The backend assigned to the current desktop environment
         (retrieved from the XDG_CURRENT_DESKTOP env variable)
      3. The first installed backend if neither is available

    :param name: The name of the backend to use or None
    :return: A backend instance or None if none is available
    """
    if name:
        if shutil.which(BACKENDS[name][1]):
            utils.print_heading('Using supplied wallpaper backend: ')
            utils.print_info(name)
            return BACKENDS[name][0]()

        logging.error('The given backend is not installed, '
                      'falling back to auto-detection.')

    xdg_desktop: Optional[str] = os.environ.get('XDG_CURRENT_DESKTOP')
    detected_backend: Optional[str] = XDG_TO_BACKEND.get(xdg_desktop, None)
    if detected_backend is None:
        logging.info('XDG_CURRENT_DESKTOP not set or unsupported, '
                     'falling back to first available backend.')

        detected_backend = next((name for name, backend in BACKENDS.items()
                                 if shutil.which(backend[1])), None)
        if detected_backend is None:
            return None

    utils.print_heading('Auto-detected wallpaper backend: ')
    utils.print_info(detected_backend)

    return BACKENDS[detected_backend][0]()


def prepare(backend: base.Backend) -> None:
    """
    Create the required cache/temp directories if not already existing
    and register an exit handler for restoring the original wallpaper.

    :return: None
    """
    paths.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    paths.TEMP_DIR.mkdir(exist_ok=True)

    atexit.register(backend.restore_original)
