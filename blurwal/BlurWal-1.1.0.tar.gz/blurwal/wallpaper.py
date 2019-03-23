"""
Functions for checking the wallpaper's status.

Author: Benedikt Vollmerhaus
License: MIT
"""

import pathlib
import re
from typing import Optional

from blurwal import paths


def changed_externally(current_path: pathlib.Path) -> bool:
    """
    Check whether the wallpaper has been changed externally.

    :param current_path: The current wallpaper's path
    :return: Whether the wallpaper has been changed externally
    """
    return (not is_transition(current_path) and
            current_path.resolve() != paths.get_original().resolve())


def is_transition(current_path: Optional[pathlib.Path]) -> bool:
    """
    Check whether the current wallpaper is a transition frame.

    If the given path is None, i.e. the current wallpaper could not be
    retrieved, it is assumed to be a transition to avoid regeneration.

    :param current_path: The current wallpaper's path
    :return: Whether the current wallpaper is a transition frame
    """
    if current_path is None:
        return True

    if current_path.parent.resolve() != paths.CACHE_DIR.resolve():
        return False

    return re.match(r'frame-\d+', current_path.name) is not None
