"""
Window and workspace operations using Xlib.

Author: Benedikt Vollmerhaus
License: MIT
"""

import logging
from typing import List

from Xlib import error

from blurwal import x11


def count_open(ignored_classes: List[str], x_conn: x11.XConnection) -> int:
    """
    Count the number of open windows on the focused workspace.

    Windows with a class in the given ignored list, bad windows,
    or ones missing a workspace number property are not counted.

    :param ignored_classes: A list of window classes to ignore
    :param x_conn: A connection to X for window retrieval
    :return: The number of open windows on the workspace
    """
    window_count = 0

    for window in x_conn.get_windows_on_current_workspace():
        try:
            window_class = window.get_wm_class()
        except error.BadWindow:
            logging.info('Ignoring bad window (id: %s)', window.id)
            continue

        if window_class is not None and window_class[1] in ignored_classes:
            logging.info("Ignoring window with class '%s'.", window_class[1])
            continue

        window_count += 1

    return window_count
