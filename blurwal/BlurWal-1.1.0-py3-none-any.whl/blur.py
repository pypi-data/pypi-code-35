"""
Author: Benedikt Vollmerhaus
License: MIT
"""

import argparse
import logging
import multiprocessing
import re
from typing import List, Optional, Tuple

from Xlib import X

from blurwal import frame, paths, utils, wallpaper, windows, x11
from blurwal.backends import base
from blurwal.transition import Transition


class Blur:
    """Window event listener with high-level blurring logic."""

    def __init__(self, args: argparse.Namespace,
                 backend: base.Backend) -> None:
        self._window_threshold: int = args.min
        self._transition_steps: int = args.steps
        self._max_sigma: int = args.blur
        self._ignored_classes: List[str] = args.ignore
        self._backend: base.Backend = backend

    def listen_for_events(self) -> None:
        """
        Listen for X11 events covering window creation and movement
        between workspaces and, upon receiving such an event, count
        the number of windows on the currently focused workspace.

        If the number of open windows is equal to or above the set
        threshold, initiate a blur, otherwise an unblur transition.

        The following events are monitored and should be enough to
        cover any situation in which a blur operation is necessary:

        MapNotify is sent when windows are drawn, e.g. a window
          - is opened on the current workspace
          - is moved to the current workspace
          - is shown by switching to the workspace it's on

        UnmapNotify is sent when windows are undrawn, e.g. a window
          - on the current workspace is closed
          - is moved to a different workspace
          - is hidden by switching to a different workspace

        :return: None
        """
        x_conn = x11.XConnection()
        x_conn.root_win.change_attributes(event_mask=X.SubstructureNotifyMask)

        utils.print_heading('Ready and waiting for events...\n')

        blur = Transition(0, 0, self._backend)
        unblur = Transition(0, 0, self._backend)

        while True:
            event = x_conn.display.next_event()
            if event.type not in (X.MapNotify, X.UnmapNotify):
                continue

            current_path = self._backend.get_current()
            if (current_path is not None and
                    wallpaper.changed_externally(current_path)):
                paths.set_original(current_path)

                if self.frames_are_outdated():
                    self.generate_transition_frames()

            window_count = windows.count_open(self._ignored_classes, x_conn)
            blur, unblur = self.init_transition(window_count, blur, unblur)

    def init_transition(self, window_count: int,
                        blur: Optional[Transition],
                        unblur: Optional[Transition]) -> Tuple:
        """
        Initiate a blur or unblur transition depending on the given
        number of windows on the current workspace, and only if the
        previously started transition was in the opposite direction.

        Transitions can only be started alternately, so an unblur
        one may only occur after a blur transition and vice versa,
        regardless of whether the previous transition is finished.

        :param window_count: The number of open windows
        :param blur: The previous blur transition or None
        :param unblur: The previous unblur transition or None
        :return: The current transition threads
        """
        # Blur
        if window_count >= self._window_threshold and unblur is not None:
            unblur.stop()
            blur = Transition(unblur.current_level, self._transition_steps,
                              self._backend)
            blur.start()
            unblur = None

        # Unblur
        if window_count < self._window_threshold and blur is not None:
            blur.stop()
            unblur = Transition(blur.current_level, 0, self._backend)
            unblur.start()
            blur = None

        return blur, unblur

    def frames_are_outdated(self) -> bool:
        """
        Check whether the transition frames need to be regenerated.

        This is the case if
          a) any transition step doesn't have a corresponding frame.
          b) the existing frame of some blur level differs from the
             expected one, the reference being generated on-the-fly
             from the current wallpaper.

        :return: Whether the transition frames need to be regenerated
        """
        utils.print_heading('Validating transition frames... ')

        found_frames = [f for f in paths.CACHE_DIR.iterdir()
                        if f.is_file() and re.match(r'frame-\d+\.\w+', f.name)]
        found_levels = [int(re.search(r'\d+', file.name).group(0))
                        for file in found_frames]

        if not set(range(self._transition_steps + 1)).issubset(found_levels):
            utils.print_warning('Outdated')
            logging.info('One or more frames are missing.')
            return True

        if frame.is_outdated(1, self._transition_steps, self._max_sigma):
            utils.print_warning('Outdated')
            logging.info('Wallpaper appears to have changed.')
            return True

        utils.print_success('Up-to-date')
        return False

    def generate_transition_frames(self) -> None:
        """
        Generate frames for the transition from the original wallpaper.

        Each frame will be blurred by an increasing blur level, so that
        setting them as the wallpaper in quick succession should result
        in a smooth-ish transition. The last frame will be blurred with
        the specified maximum blur sigma.

        :return: None
        """
        logging.info('Cache path for frames: %s', paths.CACHE_DIR)

        utils.print_subheading('Generating transition frames... ')
        utils.show_notification('Generating transition frames',
                                'This may take a few seconds.')

        jobs = [(paths.CACHE_DIR, level,
                 self._transition_steps, self._max_sigma)
                for level in range(self._transition_steps + 1)]

        with multiprocessing.Pool() as pool:
            pool.starmap(frame.generate, jobs)

        utils.print_success('Done')
        utils.show_notification('Transition frames generated',
                                'Ready for fancy blurring!')
