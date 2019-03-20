# vim: set fileencoding=utf-8 :

###################################################################################
#                                                                                 #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/               #
# Contact: beat.support@idiap.ch                                                  #
#                                                                                 #
# Redistribution and use in source and binary forms, with or without              #
# modification, are permitted provided that the following conditions are met:     #
#                                                                                 #
# 1. Redistributions of source code must retain the above copyright notice, this  #
# list of conditions and the following disclaimer.                                #
#                                                                                 #
# 2. Redistributions in binary form must reproduce the above copyright notice,    #
# this list of conditions and the following disclaimer in the documentation       #
# and/or other materials provided with the distribution.                          #
#                                                                                 #
# 3. Neither the name of the copyright holder nor the names of its contributors   #
# may be used to endorse or promote products derived from this software without   #
# specific prior written permission.                                              #
#                                                                                 #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED   #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE    #
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL      #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR      #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER      #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.            #
#                                                                                 #
###################################################################################


import logging
import click

from functools import wraps
from .log import set_verbosity_level

# This needs to be beat so that logger is configured for all beat packages.
logger = logging.getLogger('beat')


def verbosity_option(**kwargs):
    """Adds a -v/--verbose option to a click command.

    Parameters
    ----------
    **kwargs
        All kwargs are passed to click.option.

    Returns
    -------
    callable
        A decorator to be used for adding this option.
    """
    def custom_verbosity_option(f):
        def callback(ctx, param, value):
            ctx.meta['verbosity'] = value
            set_verbosity_level(logger, value)
            logger.debug("Logging of the `beat' logger was set to %d", value)
            return value
        return click.option(
            '-v', '--verbose', count=True,
            expose_value=False, default=2,
            help="Increase the verbosity level from 0 (only error messages) "
            "to 1 (warnings), 2 (log messages), 3 (debug information) by "
            "adding the --verbose option as often as desired "
            "(e.g. '-vvv' for debug).",
            callback=callback, **kwargs)(f)
    return custom_verbosity_option


def raise_on_error(view_func):
    """Raise a click exception if returned value is not zero.

    Click exits successfully if anything is returned, in order to exit properly
    when something went wrong an exception must be raised.
    """

    def _decorator(*args, **kwargs):
        value = view_func(*args, **kwargs)
        if value not in [None, 0]:
            exception = click.ClickException("Error occured")
            exception.exit_code = value
            raise exception
        return value
    return wraps(view_func)(_decorator)
