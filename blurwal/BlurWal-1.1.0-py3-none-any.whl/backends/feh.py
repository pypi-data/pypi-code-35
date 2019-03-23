"""
Author: Benedikt Vollmerhaus
License: MIT
"""

import logging
import pathlib
import re
import sys
from typing import List, Optional

from blurwal.backends import base


class FehBackend(base.Backend):
    """Wallpaper operations utilizing the feh backend."""

    FEHBG_FILE = pathlib.Path.home() / '.fehbg'

    def get_wallpaper_set_cmds(self, path: pathlib.Path) -> List[List[str]]:
        """
        Return a list of commands to be executed to set the wallpaper.

        :param path: The image to set as the wallpaper
        :return: A list of commands to be executed
        """
        return [['feh', '--bg-fill', str(path)]]

    def get_current(self) -> Optional[pathlib.Path]:
        """
        Return the current wallpaper's path from the ~/.fehbg file.

        :return: The current wallpaper's path or None if not retrievable
        """
        try:
            # Search for '-enclosed strings starting with / from back to front
            path = re.search(r"(?s:.*)'(/+.+)'", self.FEHBG_FILE.read_text())
            if not path:
                logging.warning('Could not extract current wallpaper from %s',
                                self.FEHBG_FILE.name)
                return None

            return pathlib.Path(path.group(1))
        except FileNotFoundError:
            logging.exception('Could not open %s', self.FEHBG_FILE.name)
            sys.exit(1)
