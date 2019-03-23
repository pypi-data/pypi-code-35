"""
Author: Benedikt Vollmerhaus
License: MIT
"""

import abc
import logging
import pathlib
import subprocess
import sys
from abc import abstractmethod
from typing import List, Optional

from blurwal import paths


class Backend(abc.ABC):
    """Abstract class to be implemented by individual backends."""

    def change_to(self, path: pathlib.Path) -> None:
        """
        Set the given image as the wallpaper via the commands returned
        by the backend's :meth:`get_wallpaper_set_cmds` implementation.

        :param path: The image to set as the wallpaper
        :return: None
        """
        logging.debug('Setting wallpaper to: %s', path)
        for cmd in self.get_wallpaper_set_cmds(path):
            subprocess.run(cmd)

    @abstractmethod
    def get_wallpaper_set_cmds(self, path: pathlib.Path) -> List[List[str]]:
        """
        Return a list of commands to be executed to set the wallpaper.

        Executing multiple commands may be required with some backends,
        e.g. to set the wallpaper on individual outputs or workspaces.

        :param path: The image to set as the wallpaper
        :return: A list of commands to be executed
        """

    @abstractmethod
    def get_current(self) -> Optional[pathlib.Path]:
        """
        Return the current wallpaper's path.

        This may be called rather frequently and also while the backend
        is setting the wallpaper, so keep the retrieval inexpensive and
        accommodate for empty or partially written configuration files,
        if applicable to the backend.

        :return: The current wallpaper's path or None if not retrievable
        """

    def restore_original(self) -> None:
        """
        Restore the original wallpaper.

        :return: None
        """
        try:
            original_path = paths.get_original()
            logging.info('Restoring original wallpaper: %s', original_path)
            self.change_to(original_path)
        except FileNotFoundError:
            logging.error('Could not restore original wallpaper, '
                          'please set it manually.')
            sys.exit(1)
