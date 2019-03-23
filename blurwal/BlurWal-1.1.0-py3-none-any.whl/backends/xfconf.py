"""
Author: Benedikt Vollmerhaus
License: MIT
"""

import logging
import pathlib
import subprocess
import sys
from typing import List, Optional

from blurwal import x11
from blurwal.backends import base


def find_wallpaper_properties() -> List[str]:
    """
    Return a list of xfconf-query wallpaper properties to set.

    :return: A list of xfconf-query wallpaper properties to set
    """
    property_list = subprocess.check_output(['xfconf-query',
                                             '-c', 'xfce4-desktop',
                                             '--list'])
    properties = property_list.strip().decode().splitlines()
    return [p for p in properties if p.endswith('last-image')]


class XfconfBackend(base.Backend):
    """Wallpaper operations utilizing Xfce's xfconf-query backend."""

    def __init__(self):
        x_conn = x11.XConnection()
        self._primary_screen = x_conn.get_primary_output()
        self._properties = find_wallpaper_properties()

    def get_wallpaper_set_cmds(self, path: pathlib.Path) -> List[List[str]]:
        """
        Return a list of commands to be executed to set the wallpaper.

        xfconf-query exposes individual configuration properties per
        output and workspace and thus requires multiple set commands.

        :param path: The image to set as the wallpaper
        :return: A list of commands to be executed
        """
        return [['xfconf-query',
                 '-c', 'xfce4-desktop',
                 '-p', prop,
                 '-s', str(path)]
                for prop in self._properties]

    def get_current(self) -> Optional[pathlib.Path]:
        """
        Return the current wallpaper's path from xfconf-query.

        :return: The current wallpaper's path or None if not retrievable
        """
        try:
            prop = (f'/backdrop/screen0/monitor{self._primary_screen}'
                    f'/workspace0/last-image')
            process = subprocess.check_output(['xfconf-query',
                                               '-c', 'xfce4-desktop',
                                               '-p', prop])

            return pathlib.Path(process.strip().decode())
        except subprocess.CalledProcessError:
            logging.exception('Could not retrieve current wallpaper, call to '
                              'xfconf-query returned a non-zero exit status.')
            sys.exit(1)
