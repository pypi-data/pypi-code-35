#!/usr/bin/env python3

"""
Main entry point with CLI argument parsing and startup.

Author: Benedikt Vollmerhaus
License: MIT
"""

import argparse
import logging
import sys
from typing import List

from blurwal import environment, paths, utils, wallpaper
from blurwal._version import __version__
from blurwal.blur import Blur


def parse_args(arg_list: List) -> argparse.Namespace:
    """
    Parse and return any provided command line arguments.

    :return: A namespace holding the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Smoothly blurs the wallpaper when windows are opened.',
        epilog="The transition's speed is based on the chosen number of "
               "steps in combination with how quickly the backend can "
               "update the wallpaper on your hardware. This cannot be "
               "changed, as the backend's performance is the limiting "
               "upper factor. To vary the transition speed you should "
               "thus change the number of steps (-s).")

    parser.add_argument('-v', '--version',
                        action='version', version=f'%(prog)s {__version__}')

    parser.add_argument('-m', '--min',
                        type=int, metavar='N', default=2,
                        help='the minimum number of windows to blur the '
                             'wallpaper (default: %(default)d)')

    parser.add_argument('-s', '--steps',
                        type=int, metavar='N', default=10,
                        help='the number of steps in a blur transition; '
                             'see below (default: %(default)d, min: 2)')

    parser.add_argument('-b', '--blur',
                        type=int, metavar='N', default=10,
                        help='the blur strength (sigma) to use when '
                             'fully blurred (default: %(default)d)')

    parser.add_argument('-i', '--ignore',
                        nargs='*', metavar='class', default=[],
                        help='a space-separated list of window classes '
                             'to exclude when counting the number of '
                             'open windows')

    parser.add_argument('--backend',
                        type=str, metavar='name',
                        choices=environment.BACKENDS,
                        help='the wallpaper backend to enable; supported '
                             'ones are: [%(choices)s]')

    parser.add_argument('--verbose',
                        action='store_true',
                        help='print additional information')

    parser.add_argument('--debug',
                        action='store_true',
                        help='print detailed debug output')

    args = parser.parse_args(arg_list)

    if args.steps < 2:
        parser.error('The transition must have at least 2 steps.')

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    return args


def main() -> None:
    """
    Retrieve the backend to use, set or restore the original
    wallpaper if necessary, and get ready for fancy blurring!

    :return: None
    """
    logging.basicConfig(format='%(levelname)s: %(message)s')

    args = parse_args(sys.argv[1:])

    backend = environment.get_backend(args.backend)
    if backend is None:
        logging.error('Could not find a compatible backend to use.')
        sys.exit(1)

    environment.prepare(backend)

    current_path = backend.get_current()
    if wallpaper.is_transition(current_path):
        # If the script terminated unexpectedly and a transition
        # frame got stuck as the wallpaper, restore the original.
        backend.restore_original()
    elif current_path is not None:
        utils.print_subheading('Current wallpaper: ')
        utils.print_info(str(current_path))
        paths.set_original(current_path)

    if args.ignore:
        print(f':: Ignoring window classes: {", ".join(args.ignore)}')

    try:
        blur = Blur(args, backend)
        if blur.frames_are_outdated():
            blur.generate_transition_frames()

        blur.listen_for_events()
    except KeyboardInterrupt:
        print('\nBye!')
        sys.exit(0)


if __name__ == '__main__':
    main()
