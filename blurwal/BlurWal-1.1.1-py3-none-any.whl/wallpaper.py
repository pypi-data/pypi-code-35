"""
Functions for checking the wallpaper's status.

Author: Benedikt Vollmerhaus
License: MIT
"""

import pathlib
import re

from blurwal import paths


def changed_externally(current_path: pathlib.Path) -> bool:
    """
    Check whether the wallpaper has been changed externally.

    :param current_path: The current wallpaper's path
    :return: Whether the wallpaper has been changed externally
    """
    return (not is_transition(current_path) and
            current_path.resolve() != paths.get_original().resolve())


def is_transition(path: pathlib.Path) -> bool:
    """
    Check whether the given wallpaper is a transition frame.

    :param path: The path of the wallpaper to check
    :return: Whether the given wallpaper is a transition frame
    """
    if path.parent.resolve() != paths.CACHE_DIR.resolve():
        return False

    return re.match(r'frame-\d+', path.name) is not None
