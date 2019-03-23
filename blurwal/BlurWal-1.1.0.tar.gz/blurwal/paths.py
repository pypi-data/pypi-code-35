"""
Path constants used in other modules.

Author: Benedikt Vollmerhaus
License: MIT
"""

import pathlib
import tempfile

#: The cache directory to save transition frames in
CACHE_DIR = pathlib.Path.home() / '.cache/blurwal'

#: The temporary directory to save comparison frames in
TEMP_DIR = pathlib.Path(tempfile.gettempdir()) / 'blurwal'

#: The flat file for storing the original wallpaper's path
ORIGINAL_PATH = CACHE_DIR / 'original-path'


def get_original() -> pathlib.Path:
    """
    Return the original wallpaper's path from the path storage file.

    :return: The original wallpaper's path
    """
    with ORIGINAL_PATH.open() as file:
        return pathlib.Path(file.readline().strip())


def set_original(path: pathlib.Path) -> None:
    """
    Save the given original wallpaper's path in the path storage file.

    :param path: The path to save
    :return: None
    """
    ORIGINAL_PATH.write_text(str(path))
