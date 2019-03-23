"""
X Gon' Give It to Ya.

Author: Benedikt Vollmerhaus
License: MIT
"""

import logging
from typing import Any, List

import Xlib
from Xlib import display, error
from Xlib.display import drawable


class XConnection:
    """A connection to the X server for retrieving properties."""

    def __init__(self) -> None:
        """Open a connection to X and retrieve the root window."""
        self.display = display.Display()
        self.root_win = self.display.screen().root

    def get_primary_output(self) -> str:
        """
        Return the primary output's name via the RandR extension.

        :return: The primary output's name
        """
        resources = self.root_win.xrandr_get_screen_resources()
        primary_output: int = self.root_win.xrandr_get_output_primary().output
        return self.display.xrandr_get_output_info(
            primary_output, resources.config_timestamp).name

    def get_windows_on_current_workspace(self) -> List[drawable.Window]:
        """
        Return a list of open windows on the current workspace.

        :return: A list of open windows on the current workspace
        """
        current_workspace = self._get_current_workspace()
        return [w for w in self._get_open_windows()
                if self._get_workspace_of_window(w) == current_workspace]

    def _get_current_workspace(self) -> int:
        """
        Return the currently focused workspace.

        :return: The currently focused workspace
        """
        return self._get_property('_NET_CURRENT_DESKTOP', self.root_win)[0]

    def _get_open_windows(self) -> List[drawable.Window]:
        """
        Return a list of open windows across all workspaces.

        :return: A list of open windows across all workspaces
        """
        windows = [self.display.create_resource_object('window', w_id) for w_id
                   in self._get_property('_NET_CLIENT_LIST', self.root_win)]
        return [w for w in windows if self._window_is_visible(w)]

    def _window_is_visible(self, window: drawable.Window) -> bool:
        """
        Check whether the given window is visible/not minimized.

        :param window: The window whose visibility to check
        :return: Whether the window is visible
        """
        state_atoms = self._get_property('_NET_WM_STATE', window) or []
        states = [self.display.get_atom_name(a) for a in state_atoms]
        return '_NET_WM_STATE_HIDDEN' not in states

    def _get_workspace_of_window(self, window: drawable.Window) -> int:
        """
        Return the given window's workspace number or -1 if it's
        invalid or missing the required _NET_WM_DESKTOP property.

        :param window: The window whose workspace number to get
        :return: The window's workspace number or -1 if missing
        """
        try:
            workspace = self._get_property('_NET_WM_DESKTOP', window)
            if workspace is not None:
                return workspace[0]

            logging.warning('Window (id: %s) has no workspace.', window.id)
        except error.BadWindow:
            logging.info('Bad window (id: %s)', window.id)

        return -1

    def _get_property(self, name: str, window: drawable.Window) -> Any:
        """
        Retrieve the value of a property on the given window.

        :param name: The name of the property to retrieve
        :param window: The window to retrieve the property from
        :raises error.BadWindow: if the given window is invalid
        :return: The property's value or None if missing
        """
        prop = window.get_full_property(self.display.get_atom(name),
                                        Xlib.X.AnyPropertyType)
        return prop.value if prop is not None else None
