#  Copyright (c) 2016, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import sys

import click


allow_assume_yes = click.option(
    "assume_yes", "-y", "--yes", default=False, is_flag=True,
    help=("If given, always assume yes to every prompt, "
          "and run non-interactively."),
)


def request_confirmation(msg, default=False):
    """ Request confirmation from the user.
    """
    if not click.confirm(msg, default=default):
        sys.exit(0)
